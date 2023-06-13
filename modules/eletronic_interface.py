from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
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

    def update_pos(self):
            p = self.parent
            
            if self.x < p.x:
                self.x = p.x

            elif self.x > p.right:
                self.x = p.right-self.width

            

            if self.y < p.y:
                self.y = p.y

            elif self.y > p.top:
                self.y = p.top-self.height
        
        
class Multimeter(Component):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.component = eletronic.Multimeter()
        self.text = Label(text="V: 0 I: 0 Hz: 0",size_hint=(None,None),font_size=10,size=(100,100))
        self.add_widget(self.text)

        with self.canvas.before:
            Color(248/255, 255/255, 0,1)
            self.rect1 = Rectangle(pos=self.pos,size=self.size)
            Color(0.5, 0.5, 0.5,1)
            self.rect2 = Rectangle(pos=(self.pos[0],self.pos[1]*0.6),size=(self.size[0]*0.8,self.size[1]*0.2))
            Color(0,0,0,1)
            self.terminal1 = Rectangle(pos=(self.pos[0]*0.1,self.pos[1]),size=(self.width*0.1,self.height*0.1))
            self.terminal2 = Rectangle(pos=(self.pos[0]*0.9,self.pos[1]),size=(self.width*0.1,self.height*0.1))

    def update(self,*args):
        self.update_pos()
        self.rect1.pos = self.pos
        self.rect2.pos = (self.pos[0]+self.size[0]*0.1,self.pos[1]+self.size[1]*0.6)
        self.text.pos = self.rect2.pos
        self.text.size = self.rect2.size
        self.text.font_size = self.rect2.size[0]*0.1
        self.terminal1.pos = (self.pos[0]+self.size[0]*0.1,self.pos[1])
        self.terminal2.pos = (self.pos[0]+self.size[0]*0.8,self.pos[1])
        

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


    def update(self,*args):
        
        self.update_pos()
        self.rect1.pos = self.pos
        self.terminal1.pos = (self.pos[0]-self.terminal1.size[0],self.pos[1]+self.rect1.size[1]*0.4)
        self.terminal2.pos = (self.pos[0]+self.terminal1.size[0]*2,self.pos[1]+self.rect1.size[1]*0.4)
        

            

class CircuitEditor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None,None)
        self.components = []
        self.Button1 = Button(text="add component",size=(100,50),pos=self.pos,
        font_size=10)
        self.add_widget(self.Button1)
        
        with self.canvas.before:
            Color(68/255, 71/255, 90/255, 1.0)
            self.rect = Rectangle(pos=self.pos,size=self.size)

        
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.rect.pos = self.pos

        self.rect.size = self.size

        self.Button1.x = self.x-self.Button1.width
        self.Button1.y = self.y+self.height-self.Button1.height

        for i in self.components:
            i.x = self.x + i.circuit_pos[0]
            i.y = self.y + i.circuit_pos[1]
            i.update_pos()


    def add_component(self,component: Component):
        self.components.append(component)
        self.add_widget(component)


