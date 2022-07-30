from bpa import BPA
import numpy as np
import time

if __name__ == "__main__":
    start=time.time()
    r=0.0015
    bpa = BPA(path='bunny_with_normals.txt', radius=r)
    triangles=bpa.create_mesh()
    end=time.time()
    print("Radius of pivoting ball: "+str(r))
    print("Running time: " + str(end-start))

    vertices=[]
    v2index={}
    index_counter=0
    faces=[]
    for t in triangles:
        out = []
        for vertex in t.vertices:
            cord=[vertex.x,vertex.y,vertex.z]
            v = tuple(cord)
            if v2index.get(v):
                out.append(v2index[v])
            else:
                v2index[v] = index_counter
                index_counter += 1
                out.append(v2index[v])
                vertices.append(v)
        faces.append(out)

    f = open("output.ply", "w")

    f.write('ply\n')
    f.write('format ascii 1.0\n')
    f.write('element vertex ' + str(len(vertices)) + '\n')
    f.write('property float32 x\n')
    f.write('property float32 y\n')
    f.write('property float32 z\n')
    f.write('element face ' + str(len(faces)) + '\n')
    f.write('property list uint8 int32 vertex_indices\n')
    f.write('end_header\n')

    for v in vertices:
        f.write(str(v[0]) + " " + str(v[1]) + " " + str(v[2]) + "\n")
    for face in faces:
        f.write('3 ' + str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + "\n")
    f.close()



