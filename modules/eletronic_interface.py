from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color,Rectangle, Line, Ellipse, Triangle

from modules import eletronic

class Component(Widget):
    def __init__(self,sprite: str,terminals: dict, **kwargs):
        super().__init__(**kwargs)
        self.sprite = Image(allow_stretch=True,keep_ratio=False)
        self.sprite.source = sprite

        self.terminals = terminals

        self.size_hint = (None, None)
        self.size = (50, 50) 
        self.color = Color(1, 0, 0)  

        self.bind(pos=self.update, size=self.update)

        self.add_widget(self.sprite)

    def update(self, *args):
        self.sprite.pos = self.pos
        self.sprite.size = self.size

class Resistor(Component):
    def __init__(self):
        super().__init__("modules/assets/resistor.png", {
            "1": (-5,-5),
            "2": (5,5)})

class CircuitEditor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.components = {}
        
        with self.canvas:
            Color(1,1,1,1)
            self.rect = Rectangle(pos=self.pos,size=self.size)

        
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    