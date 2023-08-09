from modules import physic

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

class body(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get("id")
        self.body =physic.body(id=self.id,m=kwargs.get("m",0),Q=kwargs.get("Q",0))

        self.center_pos = self.body.pos.values
        

class physicEditor(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ambient = physic.ambient()
        self.ambient.G = kwargs.get("G",physic.G)
        self.ambient.K = kwargs.get("K",physic.K)

        

        with self.canvas:
            Color(68/255, 71/255, 90/255, 1.0)
            self.background = Rectangle()

        self.bind(pos=self.update, size=self.update)

    def update(self,*args):
        self.background.pos = self.pos
        self.background.size = self.size