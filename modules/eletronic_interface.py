from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.graphics import Color,Rectangle, Line, Ellipse, Triangle

from modules import eletronic

class Component(Widget):
    def __init__(self,sprite: str,terminals: dict, **kwargs):
        super().__init__(**kwargs)
        self.sprite = Image(allow_stretch=True,size_hint=(None,None))
        self.sprite.width = (self.size[0]+self.size[1])/2
        self.sprite.source = sprite
        self.add_widget(self.sprite)

        self.circuit_pos = [0,0]

        self.terminals = terminals

        
        self.size_hint = (None, None)
         

        self.bind(pos=self.update, size=self.update)

        

    def update(self, *args):
        # Verificar os limites do CircuitEditor

        self.sprite.pos = self.pos

        self.sprite.size = self.size
        
        

class Resistor(Component):
    def __init__(self,**kwargs):
        super().__init__("modules/assets/resistor.png", {
            "1": (-5,-5),
            "2": (5,5)},**kwargs)

            

class CircuitEditor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None,None)
        self.components = []
        
        with self.canvas:
            Color(1,1,1,1)
            self.rect = Rectangle(pos=self.pos,size=self.size)

        
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

        for i in self.components:
            i.x = self.x + i.circuit_pos[0]
            i.y = self.y + i.circuit_pos[1]

    def add_component(self,component: Component):
        self.components.append(component)
        self.add_widget(component)


    