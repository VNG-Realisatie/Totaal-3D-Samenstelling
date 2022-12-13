import pymeshlab
import json
import argparse
import os

def get_area_volume(meshset, input_file, output_dir):
    meshset.merge_close_vertices()
    meshset.re_orient_all_faces_coherentely()
    
    geom = meshset.compute_geometric_measures()
    if 'mesh_volume' in geom.keys():
        volume = geom['mesh_volume']
    else:
        volume = 0
    print('volume is', volume)
    
    if volume<0:
        meshset.invert_faces_orientation()
        geom = meshset.compute_geometric_measures()
        volume = geom['mesh_volume']
        print('after inverting, volume is now', volume)
    
    meshset.save_current_mesh(os.path.join(output_dir, os.path.basename(input_file).split('.obj')[0]+'_repaired.obj'))
    
    statement = ('(fnz < -0.95)') 
    meshset.conditional_face_selection(condselect=statement)
    meshset.invert_selection(invfaces = True)
    meshset.delete_selected_faces()
    
    meshset.save_current_mesh(os.path.join(output_dir, os.path.basename(input_file).split('.obj')[0]+'_floor.obj'))
    
    geom2 = meshset.compute_geometric_measures()
    print('floor area is', geom2['surface_area'])
    
    floorarea = geom2['surface_area']
    
    return volume, floorarea

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get volume and area from mesh")
    parser.add_argument(
        "--inpath",
        type=str,
        default="../../data/splitrooms/cl24124c3b_alpierson-1_2021-10-06_15h55_00_064output_floor1",
        metavar="N",
    )
    parser.add_argument("--outpath", type=str, default="../../data/", metavar="N")
    args = parser.parse_args()
    output_dir = args.outpath
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    input_path = args.inpath
    
    outmetrics = []
    for filename in os.listdir(input_path):
        if 'result.obj' in filename:
            input_file = os.path.join(input_path,filename)
            try: 
                ms = pymeshlab.MeshSet()
                ms.load_new_mesh(input_file)
                volume, floorarea = get_area_volume(ms, input_file, output_dir)
                roomnumber = input_file.split('_')[1]
                result = 'The volume of room '+str(roomnumber)+' is '+str(volume)+' and the floorarea is '+str(floorarea)+'\n'
                outmetrics.append(result)
            except:
                print(input_file, 'metrics cannot be calculated')
    
    out_file = output_dir + 'metrics.txt'
    f=open(out_file,'w+')
    f.writelines(outmetrics)
    f.close()   

    print("done")