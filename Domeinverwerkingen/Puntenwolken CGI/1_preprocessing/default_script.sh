#!/bin/bash
xvfb-run CloudCompare -SILENT -AUTO_SAVE OFF -O $1 -SS SPATIAL 0.05 -SOR 6 1 -OCTREE_NORMALS auto -C_EXPORT_FMT PLY -SAVE_CLOUDS FILE ${1%.*}output.ply