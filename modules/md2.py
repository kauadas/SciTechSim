from PIL import Image

class model:
    def __init__(self,texture: str = None,cuts: list = None):
        if texture:
            self.texture = texture

        if cuts:
            self.cuts = cuts

        if texture and cuts:
            self.load()

    def save(self,name):
        with open(name+".md2","w") as md2:
            data = self.texture + "\n"
            for i in self.cuts:
                data += ",".join([str(x) for x in i])+"\n"

            md2.write(data)
            md2.close()
                
    def load(self,file: str = None):
        if file:
            with open(file) as md2:
                file = md2.read()
                filef = file.split("\n")
                self.texture = filef[0]
                self.texture_img = Image.open(self.texture)
                self.faces = {}
                for i in filef[1:]:
                    if i != '':
                        x = [int(c) for c in i.split(",")]
                        face = self.texture_img.crop(x[4:])
                        self.faces[f"{x[0]}E{x[1]}"] = [x[2],x[4],face]

        else:
            self.texture_img = Image.open(self.texture)
            
            self.faces = {}
            if not len(self.cuts) >> 6:
                for i in self.cuts:
                    face = self.texture_img.crop(i[4:])
                    self.faces[f"{i[0]}E{i[1]}"] = face

 