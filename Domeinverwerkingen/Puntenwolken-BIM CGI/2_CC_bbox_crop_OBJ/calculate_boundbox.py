import pandas as pd
import numpy as np
import laspy
import os
import argparse
import subprocess


def read_pc(f):
    with laspy.open(f) as f:

        las = f.read()

        X = las.points["X"] * las.header.scale[0] + las.header.offset[0]
        Y = las.points["Y"] * las.header.scale[1] + las.header.offset[1]
        Z = las.points["Z"] * las.header.scale[2] + las.header.offset[2]

        pts = np.stack((X, Y, Z), axis=1)
        pts = pd.DataFrame(pts)

        return pts


def export_minmax(df):

    Xmin = df[0].min()
    Xmax = df[0].max()
    Ymin = df[1].min()
    Ymax = df[1].max()
    Zmin = df[2].min()
    Zmax = df[2].max()
    minmax = [Xmin, Ymin, Zmin, Xmax, Ymax, Zmax]

    return minmax


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crop OBJ")
    parser.add_argument("--pcfile", type=str, metavar="N")
    parser.add_argument("--objfile", type=str, metavar="N")
    parser.add_argument(
        "--ccpath", type=str, default="/opt/CloudCompare/bin/CloudCompare", metavar="N"
    )
    args = parser.parse_args()

    outpath = os.path.dirname(args.objfile)
    outname = os.path.basename(args.pcfile).split(".")[0]
    outlasfile = os.path.join(outpath, outname) + ".las"

    # create command string for CC to export PC as LAS
    cmd = "xvfb-run " + args.ccpath + " -SILENT"
    cmd = cmd + ' -O "' + str(args.pcfile)

    cmd = (
        cmd
        + '" -AUTO_SAVE OFF -SS SPATIAL 0.01 -C_EXPORT_FMT LAS '
        + "-SAVE_CLOUDS FILE "
        + outlasfile
    )
    # run CC
    subprocess.run(cmd, shell=True)

    # read the las file and calculate bbox
    df = read_pc(outlasfile)
    minmax = export_minmax(df)
    minmax = list(map(str, minmax))

    # create command string for CC to crop OBJ
    cmd = "xvfb-run " + args.ccpath + " -SILENT"
    cmd = cmd + ' -O "' + str(args.objfile)

    outobjfile = os.path.join(outpath, outname) + ".obj"

    cmd = (
        cmd
        + '" -AUTO_SAVE OFF -M_EXPORT_FMT OBJ -CROP '
        + ":".join(minmax)
        + " -SAVE_MESHES FILE "
        + outobjfile
    )
    # run CC
    subprocess.run(cmd, shell=True)

    print("Finished cropping and exporting to OBJ")
