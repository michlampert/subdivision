import copy
import random
import itertools
import time
import math

class Vertex:
    def __init__(self, x, y, z, faces = None, id = None):
        self.x = x
        self.y = y
        self.z = z
        self.faces = faces if faces else []
        self.id = id

    def __str__(self): return f"{self.id}:({self.x},{self.y},{self.z})"

    def dist(self, other): return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**(1/2)

    def __add__(self, other):
        return Vertex(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Vertex(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        return Vertex(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, num):
        return Vertex(num * self.x, num * self.y, num * self.z)

    def repair_faces_order(self):
        if self.faces == []: return

        if len(self.faces) != len(list(set(self.faces))): raise Exception("Bad structure detected")

        faces = copy.copy(self.faces)
        result = [faces.pop(0)]

        counter = itertools.count()
        while faces:
            face = faces.pop(0)
            if face in result[-1].neighbours():
                result.append(face)
            else:
                faces.append(face)
                if next(counter) == 1000:
                    result.reverse()
                if next(counter) == 2000:
                    print(*self.faces)
                    return
                if next(counter) == 2000:
                    print(*self.faces)
                    return
                    raise Exception("Bad structure detected in vertex:")


        self.faces = result

class Face:
    def __init__(self, vertices = None):
        self.vertices = vertices if vertices else []
        for v in self.vertices:
            v.faces.append(self)
        if self.vertices: self.center = Vertex(sum([v.x for v in self.vertices]), sum([v.y for v in self.vertices]), sum([v.z for v in self.vertices])) * (1/len(self.vertices))
        self.inside_points = {}

    def __str__(self): return "[" + " ".join(list(map(lambda v: str(v.id), self.vertices))) + "]"

    def neighbours(self):
        result = []
        for v1, v2 in zip(self.vertices, self.vertices[1:] + self.vertices[:1]):
            tmp = set().union(v1.faces).intersection(v2.faces).difference([self])
            if tmp != set():
                result.append(tmp.pop())

        return result

    def get_inside_points(self):
        if self.inside_points != {}:
            return self.inside_points
        else:
            result = {v: (v + self.center) * 0.5 for v in self.vertices}
            self.inside_points = result
            return result

class Mesh:
    def __init__(self, *, vertices = None, faces = None, filename = None):
        if vertices is None and faces is None:
            self.vertices = []
            self.faces = []
        if vertices and faces:
            self.vertices = vertices
            self.faces = faces
        if filename is not None:
            if filename.split(".")[-1] != "off": raise Exception("mesh support only .off files")
            
            with open(filename) as f:
                lines = f.readlines()

            vertices_count = 0
            edges_count = 0
            faces_count = 0

            import re
            while True:
                line = lines.pop(0)
                if re.compile(r" *\d+ +\d+ +\d+( +\d+)? *").search(line):
                    nums = [int(num) for num in line.strip().split(" ") if num]
                    vertices_count = nums[0]
                    faces_count = nums[-2]
                    if len(nums) > 3: edges_count = nums[1]
                    break

            vertices = {}

            for i in range(vertices_count):
                line = lines.pop(0)
                x, y, z, *sth = [float(num) for num in line.strip().split(" ") if num]
                vertices[i] = Vertex(x,y,z,id=i)

            for i in range(edges_count): lines.pop(0)

            for i in range(faces_count):
                line = lines.pop(0)
                c, *vs = [int(num) for num in line.strip().split(" ") if num]
                
                f = Face(list(map(lambda num: vertices[num], vs)))
                self.faces.append(f)
                # for v in vs: vertices[v].faces.append(f)

            self.vertices += vertices.values()


    def __str__(self):
        return f"vertices: {list(map(str, self.vertices))}\nfaces: {list(map(lambda f: list(map(lambda v: v.id, f.vertices)), self.faces))}"

    def save(self, filename):
        file = open(filename, "w+")
        print("OFF", file=file)
        print(len(self.vertices), len(self.faces), 0, file=file)
        mapping = {}
        for i, v in enumerate(sorted(self.vertices, key=lambda v: v.id)):
            mapping[v.id] = i
            print(v.x, v.y, v.z, file=file)
        
        for f in self.faces:
            print(len(f.vertices), *list(map(lambda v: mapping[v.id], f.vertices)), file=file)

    def subdivision(self):
        new_vertices = sum([list(face.get_inside_points().values()) for face in self.faces],[])
        counter = itertools.count()
        for v in new_vertices: v.id = next(counter)
        
        new_faces = []
        
        old_vertices = copy.copy(self.vertices)
        old_faces = copy.copy(self.faces)
        done_edges = set()

        for face in old_faces:
            new_faces.append(Face(list(face.get_inside_points().values())))
            for v1, v2 in zip(face.vertices, face.vertices[1:] + face.vertices[:1]):
                if (v1.id, v2.id) not in done_edges and (v2.id, v1.id) not in done_edges:
                    done_edges.add((v1.id, v2.id))
                    tmp = set().union(v1.faces).intersection(v2.faces).difference([face])
                    if tmp != set():
                        neighbour = tmp.pop()
                        new_faces.append(Face(
                            [face.get_inside_points()[v1],
                            face.get_inside_points()[v2],
                            neighbour.get_inside_points()[v2],
                            neighbour.get_inside_points()[v1],
                            ]))
        
        for vertice in old_vertices:
            if len(vertice.faces) < 3: continue
            vertice.repair_faces_order()
            new_faces.append(Face([face.get_inside_points()[vertice] for face in vertice.faces]))
                    

        return Mesh(vertices=new_vertices, faces=new_faces)

    def save_faces_separately(self):
        for i, face in enumerate(self.faces):
            Mesh(vertices=self.vertices, faces=[face]).save(f"tmp/face{i}.off")



if __name__ == "__main__":

    # mesh = Mesh(filename = "cube.off")

    # total_time = 0
    # for i in range(8):
    #     mesh.save(f"meshes/mesh_subdivided_{i}_times.off")

    #     if total_time < 0.001:
    #         time_str = str(round(total_time * 1000, 5)) + " ms"
    #     elif total_time < 0.1:
    #         time_str = str(round(total_time * 1000, 2)) + " ms"
    #     else: time_str = str(round(total_time, 2)) + " s"
    #     print(f'| mesh after {i} subdivisions<br />vertices: {len(mesh.vertices)}<br />faces: {len(mesh.faces)}<br />time to compute: {time_str} | <img src="photos/photo00_L0{i}.png" alt="drawing" width="50%"/> |')
        
    #     if i == 7 : break
    #     t1 = time.time()
    #     mesh = mesh.subdivision()
    #     t2 = time.time()
    #     total_time += t2-t1

    # for filename in ["boxtorus","dodecahedron","icosahedron"]:
    #     mesh = Mesh(filename=f"meshes/{filename}.off")
    #     sth = len(mesh.vertices)
    #     t1 = time.time()
    #     for i in range(6 - int(- 0.5 + math.log(len(mesh.vertices), 4))):
    #         mesh = mesh.subdivision()
    #     total_time = time.time() - t1
    #     if total_time < 0.001:
    #         time_str = str(round(total_time * 1000, 5)) + " ms"
    #     elif total_time < 0.1:
    #         time_str = str(round(total_time * 1000, 2)) + " ms"
    #     else: time_str = str(round(total_time, 2)) + " s"
    #     mesh.save(f"meshes/{filename}_smooth.off")
        # print(f'| file: {filename}<br />number of steps: {i+1}<br />faces before: {sth}<br />faces after: {len(mesh.faces)}<br />time to compute: {time_str} | <img src="photos/photo00_L0{2*i}.png" alt="drawing" width="50%"/> | <img src="photos/photo00_L0{2*i + 1}.png" alt="drawing" width="50%"/> |')

    # mesh = Mesh(filename = "meshes/heart.off")
    # mesh.subdivision().save("meshes/heart_smooth.off")

    # for filename in "boxtorus dodecahedron icosahedron m719 m724 m725 m747 m727 m746 m739 m757 m786 m804 m1600 m1813".split(" "):
    #     mesh = Mesh(filename=f"best_meshes/{filename}.off")
    #     # sth = len(mesh.vertices)
    #     # t1 = time.time()
    #     try:
    #         for i in range(6 - int(- 0.5 + math.log(len(mesh.vertices), 4))):
    #             mesh = mesh.subdivision()
    #         mesh.save(f"best_meshes/{filename}_smooth.off")
    #     except:
    #         print(filename+".off", end=" ")

        # total_time = time.time() - t1
        # if total_time < 0.001:
        #     time_str = str(round(total_time * 1000, 5)) + " ms"
        # elif total_time < 0.1:
        #     time_str = str(round(total_time * 1000, 2)) + " ms"
        # else: time_str = str(round(total_time, 2)) + " s"
        # print(f'| file: {filename}<br />number of steps: {i+1}<br />faces before: {sth}<br />faces after: {len(mesh.faces)}<br />time to compute: {time_str} | <img src="photos/photo00_L0{2*i}.png" alt="drawing" width="50%"/> | <img src="photos/photo00_L0{2*i + 1}.png" alt="drawing" width="50%"/> |')
    
    mesh = Mesh(filename="suzanne.off")
    for i in range(5):
        mesh = mesh.subdivision()
        mesh.save(f"suzanne_smooth_{i+1}.off")
    