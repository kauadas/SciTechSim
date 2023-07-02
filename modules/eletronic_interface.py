from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.graphics import Color,Rectangle, Line, Ellipse, Triangle

from modules import eletronic

wires = 0
# classe pai dos componentes qualquer modificação aqui altera todos os componentes tambem.
class Component(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.circuit_pos = kwargs.get('pos',(0,0))
        
        self.size_hint = (None, None)
        
        self.component = None
        

        self.bind(pos=self.update, size=self.update)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.parent.select = self.component.name
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

        for i in self.wires:
            i.update()


# multimetro    
class Multimeter(Component):
    def __init__(self,name: str = None,**kwargs):
        super().__init__(**kwargs)

        name = name or "MM1"
        self.component = eletronic.Multimeter(name=name)
        self.type = "multimeter"
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
        self.rect1.size = self.size
        self.rect2.pos = (self.pos[0]+self.size[0]*0.1,self.pos[1]+self.size[1]*0.6)
        self.rect2.size = (self.size[0]*0.8,self.size[1]*0.2)
        self.text.pos = self.rect2.pos
        self.text.size = self.rect2.size
        self.font_size = self.rect2.size[0]/10
        self.text.font_size = self.rect2.size[0]*0.1
        self.terminal1.pos = (self.pos[0]+self.size[0]*0.1,self.pos[1])
        self.terminal1.size = (self.width*0.1,self.height*0.1)
        self.terminal2.pos = (self.pos[0]+self.size[0]*0.8,self.pos[1])
        self.terminal2.size = (self.width*0.1,self.height*0.1)

# objeto resistor
class Resistor(Component):
    def __init__(self,name: str = None,**kwargs):
        super().__init__(**kwargs)



        with self.canvas:
            Color(139/255, 103/255, 0,1)
            self.rect1=Rectangle(pos=self.circuit_pos,size=(self.width,self.height*0.5))
            Color(0,0,0,1)
            self.terminal1 = Rectangle(pos=self.circuit_pos,size=(self.width*0.5,self.height*0.1))
            self.terminal2 = Rectangle(pos=self.circuit_pos,size=(self.width*0.5,self.height*0.1))

        self.terminals = {
            "1": self.terminal1,
            "2": self.terminal2
        }
        name = name or "R1"
        self.type = "resistor"
        self.component = eletronic.Resistor(name=name)


    def update(self,*args):
        
        self.update_pos()
        self.rect1.pos = self.pos
        self.rect1.size = (self.width,self.height*0.5)
        self.terminal1.size = (self.width*0.5,self.height*0.1)
        self.terminal1.pos = (self.pos[0]-self.terminal1.size[0],self.pos[1]+self.rect1.size[1]*0.4)
        self.terminal2.size = (self.width*0.5,self.height*0.1)
        self.terminal2.pos = (self.pos[0]+self.terminal2.size[0]*2,self.pos[1]+self.rect1.size[1]*0.4)
 
class Source(Component):
    def __init__(self,name: str = None,**kwargs):
        super().__init__(**kwargs)



        with self.canvas:
            Color(0.7, 0.7, 0,1)
            self.rect1=Rectangle(pos=self.circuit_pos,size=(self.width,self.height*0.6))
            Color(0.5,0.5,0.5,1)
            self.terminal1 = Rectangle(pos=self.circuit_pos,size=(self.width*0.1,self.height*0.1))
            self.terminal2 = Rectangle(pos=self.circuit_pos,size=(self.width*0.1,self.height*0.1))
            Color(0,0,0,1)


        self.terminals = {
            "-": self.terminal1,
            "+": self.terminal2
        }

        name = name or "Source"
        self.type = "source"
        self.component = eletronic.source(name=name)


    def update(self,*args):
        
        self.update_pos()
        self.rect1.pos = self.pos
        self.rect1.size = (self.width,self.height*0.6)
        self.terminal1.size = (self.width*0.1,self.height*0.1)
        self.terminal1.pos = (self.pos[0],self.pos[1]+self.rect1.size[1])
        self.terminal2.size = (self.width*0.1,self.height*0.1)
        self.terminal2.pos = (self.pos[0]+self.rect1.size[0]-self.terminal2.size[0],self.pos[1]+self.rect1.size[1])

# janela de criação de componentes
class newComponent(Popup):
    def __init__(self,widget,**kwargs):
        super().__init__(**kwargs)

        self.widget = widget

        self.layout = StackLayout(orientation='lr-tb')

        
        self.comp_type = None
        
        self.name = TextInput(hint_text="component name...",multiline=False,size_hint_y=None,height=40)
        self.Size = TextInput(hint_text="component size...",multiline=False,size_hint_y=None,height=40)
        self.Pos = TextInput(hint_text="component Pos in format x,y",multiline=False,size_hint_y=None,height=40)

        self.options = DropDown()

        self.select_type = Button(text="select a component...",size_hint_y=None,height=40)
        self.select_type.on_press = lambda *args: self.layout.add_widget(self.options)


        components = ["resistor","multimeter","source"]

        opts = []
        for i in components:
            opt = Button(text=i.capitalize(),size_hint_y=None,height=40)
            opt.on_press = lambda *args, c=i: self.options.select(c)
            opts.append(opt)
            self.options.add_widget(opt)

        self.create = Button(text="create",size_hint_y=None,height=40)
        self.create.on_press = self.on_create
        self.options.on_select = self.select

        self.add_widget(self.layout)
        self.layout.add_widget(self.select_type)
        self.layout.add_widget(self.name)
        
        self.layout.add_widget(self.Size)
        
    
    def select(self,_type: str):
        self.select_type.text = "type: " + _type
        if _type == "resistor" and self.comp_type != "resistor":
            
            self.comp_type = _type

        elif _type == "multimeter" and self.comp_type != "multimeter":
            
            self.comp_type = _type

        elif _type == "source" and self.comp_type != "source":
            
            self.comp_type = _type


        
        if _type != None:
            if self.create.parent != self.layout:
                self.layout.add_widget(self.create)

    def on_create(self,*args):
        if self.comp_type == "resistor":
            resistor = Resistor(self.name.text)

            self.widget.add_component(resistor)
            resistor.pos = self.widget.pos
            resistor.circuit_pos = (0,0)
            size = float(self.Size.text)
            resistor.size = (size,size)

        elif self.comp_type == "multimeter":
            multimeter = Multimeter(self.name.text)

            self.widget.add_component(multimeter)
            multimeter.pos = self.widget.pos
            multimeter.circuit_pos = (0,0)
            size = float(self.Size.text)
            multimeter.size = (size,size)
            
        elif self.comp_type == "source":
            source = Source(self.name.text)

            self.widget.add_component(source)
            source.pos = self.widget.pos
            source.circuit_pos = (0,0)
            size = float(self.Size.text)
            source.size = (size,size)

            
            
                   
        self.dismiss()

class config_component(Popup):
    def __init__(self,component: Component,**kwargs):
        super().__init__(**kwargs)

        self.component = component
        layout = StackLayout(orientation='lr-tb')
        self.R = TextInput(hint_text="Resistance in ohms",multiline=False,size_hint_y=None,height=40)
        self.V = TextInput(hint_text="voltage",multiline=False,size_hint_y=None,height=40)
        self.I = TextInput(hint_text="current",multiline=False,size_hint_y=None,height=40)
        self.Hz = TextInput(hint_text="frequency in hz",multiline=False,size_hint_y=None,height=40)


        self.ok = Button(text="ok",size_hint_y=None,height=40)
        self.ok.on_press = self.on_ok

        self.connect = Button(text="connect to....",size_hint_y=None,height=40)
        self.connect.on_press = lambda *args: config_connections(self.component)

        if component.type == "resistor":
            self.R.hint_text += f": {str(self.component.component.r)} ohms"
            layout.add_widget(self.R)

        elif component.type == "source":
            self.V.hint_text += f": {str(self.component.component.V)} volts"

            self.I.hint_text += f": {str(self.component.component.I)} amperes"

            self.Hz.hint_text += f": {str(self.component.component.Hz)} hz"
            
            layout.add_widget(self.V)
            layout.add_widget(self.I)
            layout.add_widget(self.Hz)

        layout.add_widget(self.ok)
        layout.add_widget(self.connect)

        self.add_widget(layout)
        self.open()

    def on_ok(self):
        if self.component.type == "resistor":
            r = self.R.text
            if r != "":
                self.component.component.r = float(r)

        if self.component.type == "source":
            V = self.V.text
            i = self.I.text
            hz = self.Hz.text
            if V != "":
                self.component.component.V = float(V)
            
            if i != "":
                self.component.component.I = float(i)
            
            if hz != "":
                self.component.component.Hz = float(hz)

        self.dismiss()

class config_connections(Popup):
    def __init__(self,component: Component,**kwargs):
        super().__init__(**kwargs)

        self.layout = StackLayout(orientation='lr-tb')
        self.terminals = DropDown()
        self.terminals2 = DropDown()
        self.comps = DropDown()
        self.terminal = None
        self.terminal2 = None
        self.name = component.component.name
        self.component = component
        self.component2 = None

        
        
        self.b1 = Button(text="select a terminal",size_hint_y=None,height=40)
        self.b1.on_press = lambda *args: self.layout.add_widget(self.terminals)
        
        for k,i in component.component.terminals.items():
            print(k)
            
            opt = Button(text=k,size_hint_y=None,height=40)
            opt.on_press = lambda *args,l=k, c=i: self.terminals.select((l,c))

            self.terminals.add_widget(opt)

        self.layout.add_widget(self.b1)

        self.b2 = Button(text="select a component",size_hint_y=None,height=40)
        self.b2.on_press = lambda *args: self.layout.add_widget(self.comps)
        for k,i in component.parent.components.items():
            print(k)
            if k != component.component.name:
                opt = Button(text=k,size_hint_y=None,height=40)
                opt.on_press = lambda *args,l=k ,c=i: self.comps.select((l,c))

                self.comps.add_widget(opt)

        self.layout.add_widget(self.b2)

        self.b3 = Button(text="select a terminal of ",size_hint_y=None,height=40)
        self.b3.on_press = lambda *args: self.layout.add_widget(self.terminals2)
        
        self.connect = Button(text="connect",size_hint_y=None,height=40)
        self.connect.on_press = self.on_connect

        self.comps.on_select = self.on_select
        self.terminals.on_select = self.on_select_terminal
        self.terminals2.on_select = self.on_select_terminal2
        self.add_widget(self.layout)
        self.open()

    def on_select(self,data):
        
        self.b2.text = "component: "+data[0]
        self.component2 = data[1]

        self.terminals2.clear_widgets()

        for k,i in self.component2.component.terminals.items():
            print(k)
            
            opt = Button(text=k,size_hint_y=None,height=40)
            opt.on_press = lambda *args,l=k, c=i: self.terminals2.select((l,c))

            self.terminals2.add_widget(opt)

        self.b3.text = "select a terminal of "+data[0]
        if not self.b3.parent:
            self.layout.add_widget(self.b3)


    def on_select_terminal(self,data):
        self.b1.text = "terminal: "+data[0]
        self.terminal = data[0]

    def on_select_terminal2(self,data):
        self.b3.text = "terminal: "+data[0]
        self.terminal2 = data[0]

        self.connect.text = f"connect {self.name} to {self.component2.component.name}"
        if not self.connect.parent:  
            self.layout.add_widget(self.connect)

    def on_connect(self):
        
        self.component.component.add_connection(self.component2.component,self.terminal,self.terminal2)

        t1 = self.component.terminals[self.terminal]

        t2 = self.component2.terminals[self.terminal2]


class CircuitEditor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.select = None

        self.size_hint = (None,None)
        self.components = {}
        self.Button1 = Button(text="add component",size=(100,50),pos=self.pos,
        font_size=10)
        self.Button1.on_press = self.on_btn1
        self.add_widget(self.Button1)
        self.Button2 = Button(text="remove component",size=(100,50),pos=self.pos,
        font_size=10)
        self.Button2.on_press = self.remove_component
        self.add_widget(self.Button2)
        self.Button3 = Button(text="config component",size=(100,50),pos=self.pos,
        font_size=10)
        self.Button3.on_press = self.config_component
        self.add_widget(self.Button3)
        
        with self.canvas.before:
            Color(68/255, 71/255, 90/255, 1.0)
            self.rect = Rectangle(pos=self.pos,size=self.size)

        
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.rect.pos = self.pos

        self.rect.size = self.size

        self.Button1.x = self.x-self.Button1.width
        self.Button1.y = self.y+self.height-self.Button1.height

        self.Button2.x = self.x-self.Button2.width
        self.Button2.y = self.y+self.height-self.Button2.height-50

        self.Button3.x = self.x-self.Button3.width
        self.Button3.y = self.y+self.height-self.Button3.height-100

        for i in self.components.values():
            i.x = self.x + i.circuit_pos[0]
            i.y = self.y + i.circuit_pos[1]
            i.update_pos()

    def config_component(self):
        if self.select:
            config_component(self.components.get(self.select))

    def add_component(self,component: Component):
        self.components[component.component.name] = component
        self.add_widget(component)

    def remove_component(self,*args):
        if self.select:
            for i in self.components.get(self.select).wires:
                self.remove_widget(i)
                self.components.pop(i.name)

            self.remove_widget(self.components.get(self.select))
            self.components.pop(self.select)
            self.select = None


            
    def on_btn1(self,*args):
        newComponent(widget=self).open()

