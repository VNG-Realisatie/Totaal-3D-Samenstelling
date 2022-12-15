import argparse
import numpy as np
from scipy import signal
import open3d as o3d
import os


def histogram_analysis(pcd):
    z_bins = np.asarray(pcd.points).shape[0] // 1000
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


def detect_splits(values):
    if len(values) == 3:
        values = np.insert(
            values, 1, values[1]
        )  # if there is 3 peaks, the middle one will be duplicated
    if len(values) == 5:
        values[1] = values[2]
        values[3] = values[
            2
        ]  # if there is 5 peaks the middle one will replace the 2nd and 4th value
        values = np.delete(values, 2)
    for i in range(0, len(values), 2):
        top = values[i + 1]
        floor = values[i]
        if top - floor < 2.1:
            values = np.delete(values, np.where(values == floor)[0][0])
            values = np.delete(values, np.where(values == top)[0][0])
        if (i + 2) > (len(values) - 1):
            break

    values[::2] -= 0.1  # buffer to include the whole lower floor
    values[1::2] += 0.1  # buffer to include the whole upper floor

    splits = [values[i : i + 2] for i in range(0, len(values), 2)]
    return splits


def split_and_write_floors(pc, splits, output_dir, inputname):
    for i in range(len(splits)):
        lowerbound_floor = splits[i].min()
        upperbound_roof = splits[i].max()
        floor_points = np.asarray(pc.points)
        floor = floor_points[floor_points[:, 2] > lowerbound_floor]
        floor = floor[floor[:, 2] < upperbound_roof]
        o3d.io.write_point_cloud(
            output_dir + inputname + "_floor" + str(i + 1) + ".ply",
            o3d.geometry.PointCloud(o3d.utility.Vector3dVector(floor)),
        )
        print("writing floor " + str(i + 1))
        print("height of the floor is", upperbound_roof - lowerbound_floor)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split floors of pointcloud")
    parser.add_argument(
        "--infile",
        type=str,
        default="data/CaseStudy2/PointCloud_cs2_dec_x-y-z-unixtime12precision_features_pcl5filter.ply",
        metavar="N",
    )
    parser.add_argument("--outpath", type=str, default="data/planeto3d/", metavar="N")
    args = parser.parse_args()
    output_dir = args.outpath
    if not os.path.exists(output_dir):
            os.mkdir(output_dir)
    pcd = o3d.io.read_point_cloud(args.infile)
    inputname = os.path.basename(args.infile).split(".ply")[0]

    z_split_values = histogram_analysis(pcd)
    print(z_split_values)
    points = np.asarray(pcd.points)
    splits = detect_splits(z_split_values)
    print("number of floors is " + str(len(splits)))
    split_and_write_floors(pcd, splits, output_dir, inputname)
    print("done")
