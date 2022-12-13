import FreeCAD as App
import Mesh
import Part
import Draft
import exportIFC
import os
import argparse


def convert_objtoifc(input_obj, outpath):
    doc = App.newDocument()
    mesh = Mesh.Mesh()
    mesh.read(input_obj)
    
    doc.addObject("Part::Feature", "Shape")
    shape = Part.Shape()
    shape.makeShapeFromMesh(mesh.Topology, 0.1)
    doc.getObject("Shape").Shape = shape
    doc.getObject("Shape").purgeTouched()
    objs = []
    objs.append(doc.getObject("Shape"))
    for obj in objs:
       Draft.scale(obj, App.Vector(1000,1000,1000))
    
    outfilename = os.path.basename(input_obj).split(".")[0] + ".ifc"
    exportIFC.export(objs, os.path.join(outpath, outfilename))

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert OBJ to IFC")
    parser.add_argument("--objfile", type=str, metavar="N")
    parser.add_argument("--outpath", type=str, default=None, metavar="N")
    args = parser.parse_args()

    if args.outpath == None:
        args.outpath = os.path.dirname(args.objfile)

    convert_objtoifc(args.objfile, args.outpath)

    print("Finished converting OBJ to IFC")