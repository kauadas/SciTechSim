from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.graphics import Color,Rectangle, Line, Ellipse, Triangle

from modules import eletronic

class Component(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.circuit_pos = kwargs.get('pos',(0,0))
        
        self.size_hint = (None, None)
    

        self.bind(pos=self.update, size=self.update)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.center = touch.pos
            self.circuit_pos  = [x - y for x,y in zip(self.pos,self.parent.pos)]

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)

    def update(self, *args):
        
        self.rect1.pos = self.pos
        self.terminal1.pos = (self.pos[0]-self.terminal1.size[0],self.pos[1]+self.rect1.size[1]*0.4)
        self.terminal2.pos = (self.pos[0]+self.terminal1.size[0]*2,self.pos[1]+self.rect1.size[1]*0.4)
        
        
        

class Resistor(Component):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            Color(139/255, 103/255, 0,1)
            self.rect1=Rectangle(pos=self.circuit_pos,size=(self.width,self.height*0.5))
            Color(0,0,0,1)
            self.terminal1 = Rectangle(pos=self.circuit_pos,size=(self.width*0.5,self.height*0.1))
            self.terminal2 = Rectangle(pos=self.circuit_pos,size=(self.width*0.5,self.height*0.1))

        self.component = eletronic.Resistor()

            

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


