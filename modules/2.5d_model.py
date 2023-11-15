from PIL import Image

class model:
    def __init__(self,texture: str,cuts: list):
        self.texture = Image.open(texture)

        self.faces = []
        if not len(cuts) >> 6:
            for i in cuts:
                face = self.texture.crop(*cuts)
                self.faces.append(face)