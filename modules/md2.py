import json

def to_tuple(X: str):

    if "(" in X:
        X = X.replace("(","").replace(")","")
        X = X.split(",")
        Y = []
        for i in X:
            Y.append(float(i))

        return Y
    
    else:
        return float(X)


class Model:
    def __init__(self,faces = 6,facemap: dict = {}) -> None:
        self.objs = [[] for i in range(faces)]
        self.facemap = facemap

    def Circle(self,pos: tuple,radius: int, color: tuple,face: int = 0) -> None: 
        face = int(face)
        self.objs[face].append({
            "type": "Circle",
            "pos": pos,
            "radius": radius,
            "color": color,
            "face": face
        })


    def Line(self,pos: tuple,pos2: tuple, color: tuple,face: int = 0) -> None:
        face = int(face)
        self.objs[face].append({
            "type": "Line",
            "pos": pos,
            "pos2": pos2,
            "color": color,
            "face": face
        })

    def Rectangle(self,pos: tuple,size: tuple, color: tuple,face: int = 0) -> None:
        face = int(face)
        self.objs[face].append({
            "type": "Rectangle",
            "pos": pos,
            "size": size,
            "color": color,
            "face": face
        })

    

    def save(self,file: str):
        data = ""

        for i in self.objs:
            for c in i:
                data += "!".join(list([str(i) for i in c.values()])) + "\n"

        with open(file+".md2","w") as save:
            save.write(f"{len(self.objs)}!{self.facemap} \n"+data)
            save.close()

    def load(self,file: str):
        with open(file) as data:
            txt = data.read()
            data.close()

        txt = txt.split("\n")
        line0 = txt[0].split("!")
        self.objs = [[] for i in range(int(line0[0]))]
        self.facemap = json.loads(line0[1])
        for i in txt[1::]:
            line = i.split("!")

            if line[0] == 'Line':
                self.Line(*[to_tuple(x) for x in line[1::]])

            if line[0] == 'Circle':
                self.Circle(*[to_tuple(x) for x in line[1::]])

            if line[0] == 'Rectangle':
                self.Rectangle(*[to_tuple(x) for x in line[1::]])
