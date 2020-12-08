import copy
import random
import itertools

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

        faces = copy.copy(self.faces)
        result = [faces.pop(0)]
        while faces:
            face = faces.pop(0)
            if face in result[-1].neighbours():
                result.append(face)
            else:
                faces.append(face)

        self.faces = result

class Face:
    def __init__(self, vertices = None):
        self.vertices = vertices if vertices else []
        self.center = Vertex(sum([v.x for v in self.vertices]), sum([v.y for v in self.vertices]), sum([v.z for v in self.vertices])) * (1/len(self.vertices))
        self.inside_points = {}

    def __str__(self): return "[" + " ".join(list(map(lambda v: str(v.id), self.vertices))) + "]"

    def neighbours(self):
        result = []
        for v1, v2 in zip(self.vertices, self.vertices[1:] + self.vertices[:1]):
            tmp = set().union(v1.faces).intersection(v2.faces).difference(self)
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
                for v in vs: vertices[v].faces.append(f)

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
                if (v1.id, v2.id) not in done_edges or (v2.id, v1.id) not in done_edges:
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
            # vertice.repair_faces_order()
            new_faces.append(Face([face.get_inside_points()[vertice] for face in vertice.faces]))
                    

        return Mesh(vertices=new_vertices, faces=new_faces)
        



if __name__ == "__main__":
    mesh1 = Mesh(filename = "cube.off")
    mesh2 = mesh1.subdivision()
    mesh2.save("cube2.off")
    # mesh3 = mesh2.subdivision()
    # mesh3.save("cube3.off")