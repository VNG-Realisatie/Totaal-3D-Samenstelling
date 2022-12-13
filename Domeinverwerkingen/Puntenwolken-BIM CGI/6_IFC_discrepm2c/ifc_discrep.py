import os
import numpy as np
import open3d as o3d
import multiprocessing
import ifcopenshell
from ifcopenshell import geom
import trimesh
import argparse
import subprocess


def compute_ifc_disc(input_pc, input_ifc, outpath):
    # Point cloud
    pcd = o3d.io.read_point_cloud(input_pc)
    pcd.estimate_normals()

    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 1.5 * avg_dist
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector([radius, radius * 2])
    )
    pc_mesh = trimesh.Trimesh(
        np.asarray(mesh.vertices),
        np.asarray(mesh.triangles),
        vertex_normals=np.asarray(mesh.vertex_normals),
    )

    pc = np.asarray(pcd.points)
    pc_bb = [
        min(pc[:, 0]),
        min(pc[:, 1]),
        min(pc[:, 2]),
        max(pc[:, 0]),
        max(pc[:, 1]),
        max(pc[:, 2]),
    ]

    # IFC
    ifc = ifcopenshell.open(input_ifc)

    # Discrepancies
    settings = geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)
    iterator = geom.iterator(settings, ifc, multiprocessing.cpu_count())
    if iterator.initialize():
        while iterator.next():
            shape = iterator.get()
            element = ifc.by_guid(shape.guid)
            verts = shape.geometry.verts
            faces = shape.geometry.faces
            grouped_verts = np.array(
                [verts[i : i + 3] for i in range(0, len(verts), 3)]
            )
            grouped_faces = np.array(
                [faces[i : i + 3] for i in range(0, len(faces), 3)]
            )

            x = [x[0] for x in grouped_verts]
            y = [y[1] for y in grouped_verts]
            z = [z[2] for z in grouped_verts]
            element_bb = [min(x), min(y), min(z), max(x), max(y), max(z)]

            if not (
                pc_bb[0] <= element_bb[3]
                and pc_bb[3] >= element_bb[0]
                and pc_bb[1] <= element_bb[4]
                and pc_bb[4] >= element_bb[1]
                and pc_bb[2] <= element_bb[5]
                and pc_bb[5] >= element_bb[2]
            ):
                ifc.remove(element)

            else:
                element_mesh = trimesh.Trimesh(
                    faces=grouped_faces, vertices=grouped_verts
                )

                if trimesh.boolean.intersection([element_mesh, pc_mesh]).is_empty:
                    ifc.remove(element)

                else:
                    distances = trimesh.proximity.signed_distance(element_mesh, pc)
                    pointsinmesh = np.sum(np.array(distances) >= 0)
                    min_nopoints = 1

                    if pointsinmesh > min_nopoints:
                        ifc.remove(element)

    for space in ifc.by_type("ifcspace"):
        ifc.remove(space)

    # Export IFC discrepancies
    outfilename = os.path.basename(input_pc).split(".")[0] + "_m2cdiscrep.ifc"
    ifc.write(os.path.join(outpath, outfilename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IFC Discrepancies")
    parser.add_argument("--pcfile", type=str, metavar="N")
    parser.add_argument("--ifcfile", type=str, metavar="N")
    parser.add_argument("--outpath", type=str, default=None, metavar="N")
    parser.add_argument(
        "--ccpath", type=str, default="/opt/CloudCompare/bin/CloudCompare", metavar="N"
    )
    args = parser.parse_args()

    if args.outpath == None:
        args.outpath = os.path.dirname(args.pcfile)

    # create command string for CC
    cmd = "xvfb-run " + args.ccpath + " -SILENT"
    cmd = cmd + ' -O "' + str(args.pcfile)

    cmd = (
        cmd
        + '" -AUTO_SAVE OFF -C_EXPORT_FMT PLY -SS SPATIAL 0.1 '
        + "-SAVE_CLOUDS FILE "
        + args.pcfile[:-4]
        + ".ply"
    )
    # run CC
    subprocess.run(cmd, shell=True)

    compute_ifc_disc(args.pcfile[:-4] + ".ply", args.ifcfile, args.outpath)

    os.remove(args.pcfile[:-4] + ".ply")

    print("Finished computing and exporting IFC discrepancies")

