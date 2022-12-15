import os
import glob
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import argparse
import subprocess


def ransac_dbscan_analysis(pcd, output_dir, min_points, cutoff_points):
    segments = {}
    d_threshold = 0.01
    rest = pcd
    i = 0
    j = 0
    k = 0
    segments_filtered = {}
    segments_filtered_medianz = np.array([])
    target_triangles = 50

    MIN_Z_STD = 0.1

    while True:
        colors = plt.get_cmap("tab20")(i)
        _, inliers = rest.segment_plane(
            distance_threshold=0.01, ransac_n=5, num_iterations=5000
        )
        segment = rest.select_by_index(inliers)
        labels = np.array(segment.cluster_dbscan(eps=d_threshold * 10, min_points=10))
        candidates = [len(np.where(labels == j)[0]) for j in np.unique(labels)]
        best_candidate = max(zip(np.unique(labels), candidates), key=lambda x: x[1])
        if best_candidate[1] < min_points:
            break
        best_candidate = best_candidate[0]
        rest = rest.select_by_index(inliers, invert=True) + segment.select_by_index(
            list(np.where(labels != best_candidate)[0])
        )
        segment = segment.select_by_index(list(np.where(labels == best_candidate)[0]))
        segment.paint_uniform_color(list(colors[:3]))
        segments[i] = segment
        i += 1
        if np.asarray(rest.points).shape[0] < cutoff_points:
            break
    num_extracted_planes = i

    # split horizontal and vertical planes
    for i in range(num_extracted_planes):
        seg = np.asarray(segments[i].points)
        seg_stdz = np.std(seg[:, 2])
        seg_medianz = np.median(seg[:, 2])

        if seg_stdz > MIN_Z_STD:
            pc = segments[i]

            mesh, lst = pc.compute_convex_hull()

            mesh_smp = mesh.simplify_quadric_decimation(
                target_number_of_triangles=target_triangles
            )

            o3d.io.write_triangle_mesh(
                os.path.join(output_dir, "pc_wall_" + str(j) + "_mesh.obj"), mesh_smp,
            )
            j = j + 1
        else:
            segments_filtered[k] = segments[i]
            segments_filtered_medianz = np.append(
                segments_filtered_medianz, seg_medianz
            )
            k = k + 1

    segs_medianz_sort = np.argsort(segments_filtered_medianz)

    for i in range(len(segments_filtered)):
        index = segs_medianz_sort[i]
        pc = segments_filtered[index]

        mesh, lst = pc.compute_convex_hull()

        mesh_smp = mesh.simplify_quadric_decimation(
            target_number_of_triangles=target_triangles
        )

        o3d.io.write_triangle_mesh(
            os.path.join(output_dir, "pc_floor_ceiling_" + str(i) + "_mesh.obj"),
            mesh_smp,
        )
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="c2m dist to planes")
    parser.add_argument("--pcfile", type=str, metavar="N")
    parser.add_argument("--outpath", default=None, type=str, metavar="N")
    parser.add_argument(
        "--ccpath", type=str, default="/opt/CloudCompare/bin/CloudCompare", metavar="N"
    )
    args = parser.parse_args()

    if args.outpath == None:
        args.outpath = os.path.dirname(args.pcfile)

    pcd = o3d.io.read_point_cloud(args.pcfile)
    points = np.asarray(pcd.points)
    numberofpoints = np.count_nonzero(points)

    minpoints = 1000
    cutoff = int(0.1 * numberofpoints)

    outpath_planes = os.path.join(args.outpath, "C2Mplanes")
    if not os.path.exists(outpath_planes):
        os.mkdir(outpath_planes)

    ransac_dbscan_analysis(pcd, outpath_planes, minpoints, cutoff)

    cmd = "xvfb-run " + args.ccpath + " -SILENT"
    for file in os.listdir(outpath_planes):
        if file.startswith(("pc_floor_ceiling_", "pc_wall_")):
            filename = os.path.join(outpath_planes, file)
            cmd = cmd + " -O '" + str(filename) + "'"

    outfilename = os.path.basename(args.pcfile).split(".")[0] + "_planes_merged.obj"
    outfile = os.path.join(args.outpath, outfilename)
    cmd = (
        cmd
        + " -AUTO_SAVE OFF -MERGE_MESHES -M_EXPORT_FMT OBJ -SAVE_MESHES FILE "
        + outfile
    )
    # run CC
    subprocess.run(cmd, shell=True)
    print("Finished computing and exporting ransac planes")
