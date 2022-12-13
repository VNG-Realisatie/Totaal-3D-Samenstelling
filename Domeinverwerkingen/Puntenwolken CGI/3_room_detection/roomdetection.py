import argparse
import open3d as o3d
import numpy as np
import cv2
from scipy import signal
import random as rng
import os


def histogram_analysis(pcd):
    z_bins = np.asarray(pcd.points).shape[0] // 500
    z_hist, z_vals = np.histogram(np.asarray(pcd.points)[:, 2], z_bins)
    z_signals = signal.find_peaks(
        z_hist,
        height=2500,
        threshold=250,
        distance=20,
        prominence=2,
        width=None,
        wlen=None,
        rel_height=0.5,
        plateau_size=0.1,
    )
    return z_vals[z_signals[0]]


def slice_floor(floorpoints, height, thickness=10):
    pointslice = floorpoints[floorpoints[:, 2] < height]
    pointslice = pointslice[pointslice[:, 2] > height - (thickness / 100)]
    return pointslice


def slice2d(slice):
    ## HOUGH
    points_x_y = np.delete(slice, 2, 1)  # remove z axis
    dimx = max(floorpoints[:, 0]) - min(floorpoints[:, 0])
    dimy = max(floorpoints[:, 1]) - min(floorpoints[:, 1])
    bins = [np.uint(dimx * 100), np.uint(dimy * 100)]
    range = [
        [min(floorpoints[:, 0]), max(floorpoints[:, 0])],
        [min(floorpoints[:, 1]), max(floorpoints[:, 1])],
    ]
    counts, xedges, yedges = np.histogram2d(
        points_x_y[:, 0], points_x_y[:, 1], range=range, bins=bins
    )
    counts = counts * 255
    return counts, xedges, yedges, bins


def square_kernel(size):
    return cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))


def morphological_preprocessing(img, thickness):
    blur = cv2.blur(img, ksize=(7, 7))
    blur = np.uint8(blur)

    low_threshold = thickness * 0.8  # this value is dependent on the chosen thickness
    high_threshold = np.amax(blur)

    edges = cv2.Canny(blur, low_threshold, high_threshold)
    # Then, use HoughLinesP to get the lines. You can adjust the parameters for better performance.

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 30  # minimum number of pixels making up a line
    max_line_gap = 30  # maximum gap in pixels between connectable line segments
    line_image = np.copy(blur) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(
        edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap
    )

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

    closing = cv2.morphologyEx(line_image, cv2.MORPH_CLOSE, square_kernel(5))

    final_inv = cv2.bitwise_not(np.uint8(closing))

    return final_inv


def find_rooms_disttrans(img):
    rng.seed(12345)
    # Perform the distance transform algorithm
    dist = cv2.distanceTransform(np.uint8(img), cv2.DIST_C, 3)
    disttrans = dist
    # Normalize the distance image for range = {0.0, 1.0}
    # so we can visualize and threshold it
    cv2.normalize(dist, dist, 0, 1, cv2.NORM_MINMAX)

    # Threshold to obtain the peaks
    # This will be the markers for the foreground objects
    minthreshold = np.median(dist)
    # minthreshold = 0.3
    _, dist = cv2.threshold(dist, minthreshold, 1.0, cv2.THRESH_BINARY)
    # Dilate a bit the dist image
    kernel1 = np.ones((3, 3), dtype=np.uint8)
    dist = cv2.dilate(dist, kernel1)

    dist_8u = dist.astype("uint8")
    # Create the cv2_8U version of the distance image
    # It is needed for findContours()
    dist_8u = dist.astype("uint8")
    # Find total markers
    contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Create the marker image for the watershed algorithm
    markers = np.zeros(dist.shape, dtype=np.int32)
    # Draw the foreground markers
    for i in range(len(contours)):
        cv2.drawContours(markers, contours, i, (i + 1), -1)

    # Perform the watershed algorithm
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    cv2.watershed(img, markers)
    # mark = np.zeros(markers.shape, dtype=np.uint8)
    mark = markers.astype("uint8")
    mark = cv2.bitwise_not(mark)
    # Generate random colors
    colors = []
    for contour in contours:
        colors.append((rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256)))

    # Create the result image
    result = np.zeros((markers.shape[0], markers.shape[1], 3), dtype=np.uint8)
    # Fill labeled objects with random colors
    for i in range(markers.shape[0]):
        for j in range(markers.shape[1]):
            index = markers[i, j]
            if index > 0 and index <= len(contours):
                result[i, j, :] = colors[index - 1]

    return result, disttrans


def splitpointcloudbyrooms(
    colored_house, floorpoints, xedges, yedges, bins, output_dir, minpoints=1000
):
    pointcloudbins = np.asarray(
        list(
            zip(
                floorpoints[:, 0],
                floorpoints[:, 1],
                floorpoints[:, 2],
                # https://stackoverflow.com/questions/40880624/binning-in-numpy
                np.fmin(np.digitize(floorpoints[:, 0], xedges), bins[0]),
                np.fmin(np.digitize(floorpoints[:, 1], yedges), bins[1]),
            )
        )
    )

    colors = []

    gray = cv2.cvtColor(colored_house, cv2.COLOR_RGB2GRAY)
    unique_colors = np.unique(gray)

    for i, col in enumerate(unique_colors):
        unique_color = np.where(gray == col, col, 0)

        input_gray = cv2.dilate(np.uint8(unique_color), square_kernel(20), iterations=3)
        input_rgb = cv2.cvtColor(input_gray, cv2.COLOR_GRAY2RGB)

        if len(unique_color[unique_color != 0]) < minpoints:
            print(
                "skipped color {} with len {}".format(
                    i, len(unique_color[unique_color != 0])
                )
            )
            continue
        colors = []
        for p in pointcloudbins:
            xval = int(p[3]) - 1
            yval = int(p[4]) - 1
            colorrow = input_rgb[xval, yval]
            colors.append(colorrow)

        colors = np.array(colors)
        pointcloudbins_new = np.concatenate(
            (pointcloudbins, np.asarray(colors)), axis=1
        )
        pcd = np.delete(pointcloudbins_new, [3, 4], axis=1)
        pc = o3d.geometry.PointCloud()
        pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pcd[:, 0:3]))
        pc.colors = o3d.utility.Vector3dVector(pcd[:, 3:])
        pc.estimate_normals()

        idx = np.where(np.asarray(pc.colors) == col)[0]
        colorpointcloud = pc.select_by_index(idx)
        o3d.io.write_point_cloud(output_dir + "room_{}.ply".format(i), colorpointcloud)

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seperate rooms of pointcloud")
    parser.add_argument(
        "--inpath",
        type=str,
        default="/usr/src/app/data",
        metavar="N",
    )
    parser.add_argument("--outpath", type=str, default="/usr/src/app/data", metavar="N")
    parser.add_argument("--thickness", type=str, default=20, metavar="N")
    args = parser.parse_args()
    input_path = args.inpath
    work = []
    if not os.path.exists(args.outpath):
            os.mkdir(args.outpath)
    for filename in os.listdir(input_path):
        if "floor" in filename:
            output_dir = args.outpath + "/" + filename.split("/")[-1][:-4] + "/"
            work.append((input_path + "/" + filename, output_dir))
    for (input_file, output_dir) in work:
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        floor = o3d.io.read_point_cloud(input_file)

        z_split_values = histogram_analysis(floor)

        floorpoints = np.asarray(floor.points)

        ceiling = z_split_values[-1] - 0.1
        thickness = args.thickness
        slice = slice_floor(floorpoints, ceiling, thickness)
        o3d.io.write_point_cloud(
            output_dir + "slice.ply",
            o3d.geometry.PointCloud(o3d.utility.Vector3dVector(slice)),
        )

        counts, xedges, yedges, bins = slice2d(slice)
        cv2.imwrite(output_dir + "orig.png", counts)
        preprocessed_img = morphological_preprocessing(counts, thickness)
        cv2.imwrite(output_dir + "INPUT.png", preprocessed_img)
        colored_house, dist = find_rooms_disttrans(preprocessed_img)
        cv2.imwrite(output_dir + "distancetransform.png", dist * 255)
        cv2.imwrite(output_dir + "RESULT_disttrans.png", colored_house)

        splitpointcloudbyrooms(
            colored_house, floorpoints, xedges, yedges, bins, output_dir
        )

    print("done")
