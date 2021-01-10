import copy
import random
import itertools
import time
import math

global_counter = itertools.count(10000)

class Vertex:
    def __init__(self, x, y, z, faces = None, id = None):
        self.x = x
        self.y = y
        self.z = z
        self.faces = faces if faces else []
        self.id = id or next(global_counter)

    def copy(self, id=None):
        return Vertex(self.x, self.y, self.z, [], id)

    def __str__(self): return f"{self.id}:({round(self.x,2)},{round(self.y,2)},{round(self.z,2)})"

    def dist(self, other): return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**(1/2)

    def __add__(self, other):
        return Vertex(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Vertex(-self.x, -self.y, -self.z)

    def __sub__(self, other):
        return Vertex(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, num):
        return Vertex(num * self.x, num * self.y, num * self.z)

    def __truediv__(self, num):
        return self * (1/num)

    def midpoint(self, other):
        return (self + other) * 1/2

    def repair_faces_order(self):
        if self.faces == []: return

        if len(self.faces) != len(list(set(self.faces))): raise Exception("Bad structure detected (mesh probably has redundant faces)")

        faces = copy.copy(self.faces)
        result = [faces.pop(0)]

        counter = itertools.count()

        limit = len(self.faces)**2

        while faces:
            face = faces.pop(0)
            if face in result[-1].get_neighbours():
                result.append(face)
            else:
                faces.append(face)
                if next(counter) == limit:
                    result.reverse()
                if next(counter) == 2 * limit:
                    print(*self.faces)
                    return
                if next(counter) == 1000:
                    print(*self.faces)
                    raise Exception(f"Bad structure detected (faces around vertex {self} aren't consistent)")

        self.faces = result

    def get_neighbours(self):
        result = set()

        for face in self.faces:
            idx = face.vertices.index(self)
            result.add(face.vertices[idx - 1])
            result.add(face.vertices[(idx + 1) % len(face.vertices)])

        return list(result)

    def __hash__(self) -> int:
        return self.id

class Face:
    def __init__(self, vertices = None):
        self.vertices = vertices if vertices else []
        for v in self.vertices:
            v.faces.append(self)
        if self.vertices:
            self.center = Vertex(sum([v.x for v in self.vertices]), sum([v.y for v in self.vertices]), sum([v.z for v in self.vertices])) * (1/len(self.vertices))
        self.inside_points = {}
        self.midpoints = {}
        self.neighbours = []

    def __str__(self): return "[" + " ".join(list(map(lambda v: str(v.id), self.vertices))) + "]"

    def get_neighbours(self):
        if self.neighbours != []:
            return self.neighbours
        else:
            result = []
            for v1, v2 in zip(self.vertices, self.vertices[1:] + self.vertices[:1]):
                tmp = set().union(v1.faces).intersection(v2.faces).difference([self])
                if tmp != set():
                    result.append(tmp.pop())

            self.neighbours = result
            return result

    def get_inside_points(self):
        if self.inside_points != {}:
            return self.inside_points
        else:
            result = {}
            for v1, v2, v3 in zip(self.vertices, self.vertices[1:] + self.vertices[:1], self.vertices[2:] + self.vertices[:2]):
                result[v2] = ((v1+v3)/2 + v2 * 2 + self.center)/4
            self.inside_points = result
            return result

    def get_midpoints(self):
        if self.midpoints != {}:
            return self.midpoints
        else:
            result = {(v1, v2): v1.midpoint(v2) for v1,v2 in zip(self.vertices, self.vertices[1:] + self.vertices[:1])}
            self.midpoints = result
            return result

    def get_neighbour(self, v1, v2):
        for neighbour in self.get_neighbours():
            if v1 in neighbour.vertices and v2 in neighbour.vertices:
                return neighbour
        return None

    def get_edge(self, other):
        return tuple(set(self.vertices).intersection(other.vertices))

class Mesh:
    def __init__(self, *, vertices = None, faces = None, filename = None, triangular=False):
        if vertices is None and faces is None:
            self.vertices = []
            self.faces = []
        if vertices or faces:
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
                if c != 3 and triangular:
                    vs = list(map(lambda num: vertices[num], vs))
                    main = vs.pop(0)
                    for v1, v2 in zip(vs, vs[1:]):
                        self.faces.append(Face([main, v1, v2]))
                else:
                    self.faces.append(Face(list(map(lambda num: vertices[num], vs))))
                # for v in vs: vertices[v].faces.append(f)

            self.vertices += vertices.values()
        
        # self.vertices = list(filter(lambda v: len(v.faces) > 0, self.vertices))
        # self.faces = list(filter(lambda f: len(f.vertices) > 0, self.faces))


    def __str__(self):
        return f"vertices:\n{list(map(str, self.vertices))}\nfaces:\n{list(map(lambda f: list(map(lambda v: v.id, f.vertices)), self.faces))}"

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

    def save_faces_separately(self):
        for i, face in enumerate(self.faces):
            Mesh(vertices=face.vertices, faces=[face]).save(f"tmp/face{i}.off")

    def subdivision_DS(self):
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

    def subdivision_CC(self):

        edge_points = {}
        vertex_points = {}

        for face in self.faces:
            for v1, v2 in zip(face.vertices, face.vertices[1:] + face.vertices[:1]):
                if (v1, v2) in edge_points.keys() or (v2, v1) in edge_points.keys(): continue
                neighbour = face.get_neighbour(v1,v2) #or face.get_neighbour(v2,v1)
                if neighbour:
                    v = (v1 + v2 + face.center + neighbour.center)/4
                    edge_points[(v1,v2)] = v  
                else:
                    v = (v1 + v2 + face.center)/3
                    edge_points[(v1,v2)] = v 

        for v in self.vertices:
            # esc = Face([(edge_points.get((v1,v), None) or edge_points.get((v,v1), None) or print(v, v1)) for v1 in v.get_neighbours()]).center
            # fsc = Face([face.center for face in v.faces]).center
            esc = sum([(v + v1) / 2 for v1 in v.get_neighbours()], Vertex(0,0,0)) / (len(v.get_neighbours()))
            fsc = sum([face.center for face in v.faces], Vertex(0,0,0)) / (len(v.faces))
            n = len(v.faces)#?
            vertex_points[v] = ((v * (n-3)) + (esc * 2) + fsc) / n
            # print(n, "    ", esc, "    ", fsc, "    ", ((v * (n-3)) + (esc * 2) + fsc) / n)

        new_faces = []
        new_vertices = set()

        for face in self.faces:
            fc = face.center.copy()
            new_vertices.add(fc)
            for v1, v2, v3 in zip(face.vertices, face.vertices[1:] + face.vertices[:1], face.vertices[2:] + face.vertices[:2]):
                ec1 = (edge_points.get((v1,v2), None) or edge_points.get((v2,v1), None))
                ec2 = (edge_points.get((v2,v3), None) or edge_points.get((v3,v2), None))
                v = vertex_points[v2]
                new_faces.append(Face([ec1, v, ec2, fc]))

        new_vertices.update(edge_points.values())
        new_vertices.update(vertex_points.values())
        
        new_vertices = list(new_vertices)

        for i, v in enumerate(new_vertices): v.id = i

        return Mesh(vertices=new_vertices, faces=new_faces)

    def subdivision_LOOP(self):

        def alphas(n):
            if alphas.d.get(n, None): return alphas.d.get(n)
            else:
                a = 3/8 + (3/8 + math.cos(2*math.pi / n)/4)**2
                alphas.d[n]=a
                return a
        alphas.d = {}

        edge_points = {}
        vertex_points = {}

        for face in self.faces:
            for v1, v2 in zip(face.vertices, face.vertices[1:] + face.vertices[:1]):
                if (v1, v2) in edge_points.keys() or (v2, v1) in edge_points.keys(): continue
                neighbour = face.get_neighbour(v1,v2) #or face.get_neighbour(v2,v1)
                if neighbour:
                    v = ((v1 + v2)*(1/8) + (face.center + neighbour.center)*(3/8))
                    edge_points[(v1,v2)] = v  
                else:
                    v = (v1 + v2)/2
                    edge_points[(v1,v2)] = v 

        for v in self.vertices:
            n = len(v.get_neighbours())
            esc = sum([v1 for v1 in v.get_neighbours()], Vertex(0,0,0)) / n
            vertex_points[v] = v*alphas(n) + esc * (1-alphas(n))
            # print(n, "    ", esc, "    ", fsc, "    ", ((v * (n-3)) + (esc * 2) + fsc) / n)

        new_faces = []
        new_vertices = set()

        for face in self.faces:
            new_faces.append(Face([edge_points.get((v1,v2), None) or edge_points.get((v2,v1), None) for v1,v2 in zip(face.vertices, face.vertices[1:] + face.vertices[:1])]))
            for v1, v2, v3 in zip(face.vertices, face.vertices[1:] + face.vertices[:1], face.vertices[2:] + face.vertices[:2]):
                ec1 = (edge_points.get((v1,v2), None) or edge_points.get((v2,v1), None))
                ec2 = (edge_points.get((v2,v3), None) or edge_points.get((v3,v2), None))
                v = vertex_points[v2]
                new_faces.append(Face([ec1, v, ec2]))

        new_vertices.update(edge_points.values())
        new_vertices.update(vertex_points.values())
        
        new_vertices = list(new_vertices)

        for i, v in enumerate(new_vertices): v.id = i

        return Mesh(vertices=new_vertices, faces=new_faces)

    def subdivision_PR(self):

        edge_points = {}
        new_vertices = []
        new_faces = []

        for face in self.faces:
            for v1, v2 in zip(face.vertices, face.vertices[1:] + face.vertices[:1]):
                if (v1, v2) in edge_points.keys() or (v2, v1) in edge_points.keys(): continue
                v = (v1 + v2)/2
                edge_points[(v1,v2)] = v
                new_vertices.append(v)

        for face in self.faces:
            new_faces.append(Face([edge_points.get((v1,v2), None) or edge_points.get((v2,v1), None) for v1,v2 in zip(face.vertices, face.vertices[1:] + face.vertices[:1])]))
        
        for v in self.vertices:
            v.repair_faces_order()
            tmp = []
            for face1, face2 in zip(v.faces, v.faces[1:] + v.faces[:1]):
                v1, v2 = face1.get_edge(face2)
                tmp.append(edge_points.get((v1,v2), None) or edge_points.get((v2,v1), None))
            new_faces.append(Face(tmp))

        for i, v in enumerate(new_vertices): v.id = i

        return Mesh(vertices=new_vertices, faces=new_faces)


    def subdivision_mixed(self):
        return self.subdivision_CC() if random.randint(0,1) == 0 else self.subdivision_DS()


def choose_subdivision_algorithm(string_name):
    if string_name == "CathmulClark": return lambda m: m.subdivision_CC()
    if string_name == "DooSabin": return lambda m: m.subdivision_DS()
    if string_name == "Loop": return lambda m: m.subdivision_LOOP()
    return lambda m: m.subdivision_CC()

def subdivision(filename_input, filename_output, iterations_count, algorithm_name):
    subdivision_algorithm = choose_subdivision_algorithm(algorithm_name)
    mesh = Mesh(filename = filename_input)
    for i in range(iterations_count):
        mesh = subdivision_algorithm(mesh)
    mesh.save(filename_output)
        

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
    #     print(f'| mesh after {i} subdivision_DSs<br />vertices: {len(mesh.vertices)}<br />faces: {len(mesh.faces)}<br />time to compute: {time_str} | <img src="photos/photo00_L0{i}.png" alt="drawing" width="50%"/> |')
        
    #     if i == 7 : break
    #     t1 = time.time()
    #     mesh = mesh.subdivision_DS()
    #     t2 = time.time()
    #     total_time += t2-t1

    
    # mesh = Mesh(filename="best_meshes/suzanne.off")
    # for i in range(3):
    #     mesh = mesh.subdivision_LOOP()
    #     mesh.save(f"suzanne_smooth_{i+1}.off")

    # mesh = Mesh(filename="cube.off")
    # mesh.subdivision_CC().save("cube1.off")
    # print("\n\n\n\n\n\n")
    # mesh = Mesh(filename="cube1.off")
    # mesh.subdivision_CC().save("cube2.off")
    # print("\n\n\n\n\n\n")
    # mesh = Mesh(filename="cube2.off")
    # mesh.subdivision_CC().save("cube3.off")
    # mesh.subdivision_CC().subdivision_CC().save("cube2.off")
    # mesh.subdivision_CC().subdivision_CC().subdivision_CC().save("cube3.off")
    # mesh.subdivision_CC().subdivision_CC().subdivision_CC().subdivision_CC().save("cube4.off")

    # mesh = Mesh(filename = "cube.off")
    # mesh.save("cube1.off")
    # mesh.subdivision_LOOP().save("cube2.off")
    # mesh.subdivision_LOOP().subdivision_LOOP().save("cube3.off")
    # mesh.subdivision_LOOP().subdivision_LOOP().subdivision_LOOP().save("cube4.off")

    # mesh_DS = Mesh(filename = "suzanne.off")
    # mesh_CC = Mesh(filename = "suzanne.off")
    # mesh_LOOP = Mesh(filename = "suzanne.off", triangular=True)

    # DS_list = []
    # CC_list = []
    # LOOP_list = []

    # n = 6

    # total_time = 0
    # for i in range(n):
    #     mesh_DS.save(f"cube_DS{i}.off")

    #     if total_time < 0.001:
    #         time_str = str(round(total_time * 1000, 5)) + " ms"
    #     elif total_time < 0.1:
    #         time_str = str(round(total_time * 1000, 2)) + " ms"
    #     else: time_str = str(round(total_time, 2)) + " s"
    #     DS_list.append(f'![img](photos/group_photo01_L{(str(i+n) if i+n>=10 else "0"+str(i+n))}.png) <br/> {len(mesh_DS.vertices)} \| {len(mesh_DS.faces)} \| {time_str}')
        
    #     if i == n-1 : break
    #     t1 = time.time()
    #     mesh_DS = mesh_DS.subdivision_DS()
    #     t2 = time.time()
    #     total_time += t2-t1

    # total_time = 0
    # for i in range(n):
    #     mesh_CC.save(f"cube_CC{i}.off")

    #     if total_time < 0.001:
    #         time_str = str(round(total_time * 1000, 5)) + " ms"
    #     elif total_time < 0.1:
    #         time_str = str(round(total_time * 1000, 2)) + " ms"
    #     else: time_str = str(round(total_time, 2)) + " s"
    #     CC_list.append(f'![img](photos/group_photo01_L{(str(i) if i>=10 else "0"+str(i))}.png) <br/> {len(mesh_CC.vertices)} \| {len(mesh_CC.faces)} \| {time_str}')
        
    #     if i == n-1 : break
    #     t1 = time.time()
    #     mesh_CC = mesh_CC.subdivision_CC()
    #     t2 = time.time()
    #     total_time += t2-t1

    # total_time = 0
    # for i in range(n):
    #     mesh_LOOP.save(f"cube_LOOP{i}.off")

    #     if total_time < 0.001:
    #         time_str = str(round(total_time * 1000, 5)) + " ms"
    #     elif total_time < 0.1:
    #         time_str = str(round(total_time * 1000, 2)) + " ms"
    #     else: time_str = str(round(total_time, 2)) + " s"
    #     LOOP_list.append(f'![img](photos/group_photo01_L{(str(i+n+n) if i+n+n>=10 else "0"+str(i+n+n))}.png) <br/> {len(mesh_LOOP.vertices)} \| {len(mesh_LOOP.faces)} \| {time_str}')
        
    #     if i == n-1 : break
    #     t1 = time.time()
    #     mesh_LOOP = mesh_LOOP.subdivision_LOOP()
    #     t2 = time.time()
    #     total_time += t2-t1

    # for e1, e2, e3 in zip(DS_list, CC_list, LOOP_list):
    #     print("|",e1,"|",e2,"|",e3,"|")

    mesh = Mesh(filename = "cube.off")
    mesh2 = mesh.subdivision_DS().subdivision_DS()
    mesh2.save("cube_6.off") 


    


