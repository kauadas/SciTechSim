from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.graphics import Color,Rectangle, Line, Ellipse, Triangle, PushMatrix,PopMatrix, Rotate
from kivy.graphics.transformation import Matrix
from kivy.clock import Clock
from kivy.properties import NumericProperty
from modules import eletronic
import math

wires = 0
# classe pai dos componentes qualquer modificação aqui altera todos os componentes tambem.

class Component(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.circuit_pos = kwargs.get('pos',(0,0))
        
        self.size_hint = (None, None)
        
        self.component = None
        
        self.angle = 0

        self.bind(pos=self.update, size=self.update)

        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate(origin=self.center,angle=self.angle)
        
        with self.canvas.after:
            PopMatrix()


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

    def rotate(self,angle):
        if angle == 360:
            self.angle = 0

        self.angle = angle
        self.rot.angle = angle

    def update_pos(self):
        self.rot.origin = self.center
        self.rot.angle = self.angle

        p = self.parent
        if p:
            if self.x < p.x:
                self.x = p.x

            elif self.x > p.right:
                self.x = p.right-self.width

            

            if self.y < p.y:
                self.y = p.y

            elif self.y > p.top:
                self.y = p.top-self.height



# multimetro    
class Multimeter(Component):
    def __init__(self,name: str = None,**kwargs):
        super().__init__(**kwargs)

        self.angle = 0

        name = name
        self.component = eletronic.Multimeter(name=name)
        self.component.callback = self.run
        self.type = "multimeter"
        self.text = Label(text="V: 0 I: 0 Hz: 0",size_hint=(None,None),font_size=10,size=(100,100))

        with self.text.canvas:
            self.rot2 = Rotate()
            self.rot2.angle = self.angle
            self.rot2.origin = self.center
        self.add_widget(self.text)

        with self.canvas.before:
            Color(248/255, 255/255, 0,1)
            self.rect1 = Rectangle(pos=self.pos,size=self.size)
            Color(0.5, 0.5, 0.5,1)
            self.rect2 = Rectangle(pos=(self.x,self.y*0.6),size=(self.size[0]*0.8,self.size[1]*0.2))
            Color(0,0,0,1)
            self.terminal1 = Rectangle(pos=(self.x*0.1,self.y),size=(self.width*0.1,self.height*0.1))
            self.terminal2 = Rectangle(pos=(self.x*0.9,self.y),size=(self.width*0.1,self.height*0.1))

    def update(self,*args):
        self.update_pos()
        self.rot2.angle = self.angle
        self.rot2.origin = self.center
        self.rect1.pos = self.pos
        self.rect1.size = self.size
        self.rect2.pos = (self.x+self.size[0]*0.1,self.y+self.size[1]*0.6)
        self.rect2.size = (self.size[0]*0.8,self.size[1]*0.2)
        self.text.pos = self.rect2.pos
        self.text.size = self.rect2.size
        self.font_size = self.rect2.size[0]/10
        self.text.font_size = self.rect2.size[0]*0.1
        self.terminal1.pos = (self.x+self.size[0]*0.1,self.y)
        self.terminal1.size = (self.width*0.1,self.height*0.1)
        self.terminal2.pos = (self.x+self.size[0]*0.8,self.y)
        self.terminal2.size = (self.width*0.1,self.height*0.1)

    def run(self):
        
        v = self.component.V
        i = self.component.i
        hz = self.component.hz
        self.text.text = F"V: {v} I: {i} Hz: {hz}"

    def reset(self):
        self.text.text = F"V: 0 I: 0 Hz: 0"


# objeto resistor
class Resistor(Component):
    def __init__(self,name: str = None,**kwargs):
        super().__init__(**kwargs)

        self.angle = 0

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
        name = name
        self.type = "resistor"
        self.component = eletronic.Resistor(name=name)

    def update(self,*args):
        
        self.update_pos()
        self.rect1.pos = self.pos
        self.rect1.size = (self.width,self.height*0.5)
        self.terminal1.size = (self.width*0.5,self.height*0.1)
        self.terminal1.pos = (self.x-self.terminal1.size[0],self.y+self.rect1.size[1]*0.4)
        self.terminal2.size = (self.width*0.5,self.height*0.1)
        self.terminal2.pos = (self.x+self.terminal2.size[0]*2,self.y+self.rect1.size[1]*0.4)
 

# fonte
class Source(Component):
    def __init__(self,name: str = None,**kwargs):
        super().__init__(**kwargs)

        self.angle = 0

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

        name = name
        self.type = "source"
        self.component = eletronic.source(name=name)


    def update(self,*args):
        
        self.update_pos()
        self.rect1.pos = self.pos
        self.rect1.size = (self.width,self.height*0.6)
        self.terminal1.size = (self.width*0.1,self.height*0.1)
        self.terminal1.pos = (self.x,self.y+self.rect1.size[1])
        self.terminal2.size = (self.width*0.1,self.height*0.1)
        self.terminal2.pos = (self.x+self.rect1.size[0]-self.terminal2.size[0],self.y+self.rect1.size[1])

#led

class Led(Component):
    def __init__(self,name: str = "led",**kwargs):
        super().__init__(**kwargs)

        self.component = eletronic.Led(name=name)
        self.component.callback = self.run
        self.type = "led"

        with self.canvas:
            self.color1 = Color(*[i/255 for i in self.component.off_color])
            self.circle1 = Ellipse(angle_start=-90,angle_end=90)
            self.rect1 = Rectangle(pos=self.circuit_pos,size=(self.width*0.4,self.height))
            self.rect2 = Rectangle(pos=self.circuit_pos,size=(self.width*0.6,self.height))
            Color(0.5,0.5,0.5,1)
            self.terminal1 = Rectangle(pos=self.circuit_pos,size=(self.width*0.1,self.height*0.1))
            self.terminal2 = Rectangle(pos=self.circuit_pos,size=(self.width*0.1,self.height*0.1))
            Color(0,0,0,1)

        self.terminals = {
            "-": self.terminal1,
            "+": self.terminal2
        }


    def run(self):
        
        self.color1.rgba = [i/255 for i in self.component.light_color]
        
    def reset(self):
        self.color1.rgba = [i/255 for i in self.component.off_color]

    def update(self,*args):
        
        self.update_pos()

        self.rect2.size = (self.width,self.height*0.1)
        self.rect2.pos = (self.x-self.rect2.size[0]*0.1,self.y)

        self.rect1.size = (self.width*0.8,self.height*0.7)
        self.rect1.pos = (self.x,self.y+self.rect2.size[1])
        
        

        self.circle1.size = self.rect1.size
        self.circle1.pos = (self.x,self.rect1.pos[1]+self.rect1.size[1]-self.circle1.size[1]/2)

        self.terminal1.size = (self.width*0.1,self.height*0.2)
        self.terminal1.pos = (self.x+self.rect1.size[0]*0.1,self.y-self.terminal2.size[1])
        self.terminal2.size = (self.width*0.1,self.height*0.2)
        self.terminal2.pos = (self.x+self.rect1.size[0]*0.9-self.terminal2.size[0],self.y-self.terminal2.size[1])

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


        components = ["resistor","multimeter","source","led"]

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


        elif self.comp_type == "led":
            led = Led(self.name.text)

            self.widget.add_component(led)
            led.pos = self.widget.pos
            led.circuit_pos = (0,0)
            size = float(self.Size.text)
            led.size = (size,size)

            
            
                   
        self.dismiss()

# configurador de componentes
class config_component(Popup):
    def __init__(self,component: Component,**kwargs):
        super().__init__(**kwargs)

        self.component = component
        layout = StackLayout(orientation='lr-tb')
        self.R = TextInput(hint_text="Resistance in ohms",multiline=False,size_hint_y=None,height=40)
        self.V = TextInput(hint_text="voltage",multiline=False,size_hint_y=None,height=40)
        self.I = TextInput(hint_text="current",multiline=False,size_hint_y=None,height=40)
        self.Hz = TextInput(hint_text="frequency in hz",multiline=False,size_hint_y=None,height=40)
        self.status = Label(text=f'is break? {self.component.component.is_break}',size_hint_y=None,
        height=40)


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
            
        layout.add_widget(self.status)
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

# criar conexões entre os componentes
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

        self.dismiss()


class ChooseCircuit(Popup):
    def __init__(self,circuit_editor,**kwargs):
        super().__init__(**kwargs)
        self.title = "choose circuit"
        self.layout = StackLayout(orientation="lr-tb")
        self.circuits = DropDown()
        self.Open = Button(text="select",on_press = 
        lambda *args: self.layout.add_widget(self.circuits),size_hint=(1,None),height=40)

        for i in circuit_editor.pcbs.keys():
            print(i)
            opt = Button(text=i,on_press=
            lambda *args,d=i: self.circuits.select(d),size_hint_y=None,height=40)

            self.circuits.add_widget(opt)

        new = Button(text="new",on_press=
        lambda *args: self.circuits.select("new"),size_hint_y=None,height=40)

        self.circuits.add_widget(new)

        

        self.circuits.on_select = self.select
        self.layout.add_widget(self.Open)
        self.add_widget(self.layout)

        self.circuit = circuit_editor

    def select(self,data):
        print(data)
        if data != "new":
            self.circuit.save()
            self.circuit.atual_pcb = data
            self.circuit.load_project()
            

        else:
            x = str(int(list(self.circuit.pcbs.keys())[-1])+1)
            self.circuit.pcbs[x] = {}
            self.circuit.save()
            self.circuit.atual_pcb = x
            self.circuit.load_project()
            

        self.circuit.set_circuit.text = self.circuit.atual_pcb
        self.dismiss()


# widget editor de circuito
class CircuitEditor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.project = kwargs.get("project")
        self.select = None
        self.size_hint = (None,None)
        self.atual_pcb = "0"
        self.components = {}
        self.reload_all = True
        self.running = None


        self.buttons = GridLayout(cols=1,size_hint=(None,None),size=(100,self.height))
        self.set_circuit = Button(text=self.atual_pcb,size=(100,50),
        font_size=10)
        self.set_circuit.on_press = self.on_set_circuit
        self.buttons.add_widget(self.set_circuit)

        self.Button1 = Button(text="add component",size=(100,50),
        font_size=10)
        self.Button1.on_press = self.on_btn1
        self.buttons.add_widget(self.Button1)

        self.Button2 = Button(text="remove component",size=(100,50),
        font_size=10)
        self.Button2.on_press = self.remove_component
        self.buttons.add_widget(self.Button2)

        self.Button3 = Button(text="config component",size=(100,50),
        font_size=10)
        self.Button3.on_press = self.config_component

        self.buttons.add_widget(self.Button3)

        self.Button4 = Button(text="run",size=(100,50),
        font_size=10)
        self.Button4.on_press = self.on_run
        self.buttons.add_widget(self.Button4)

        self.Button5 = Button(text="rotate component",size=(100,50),
        font_size=10)
        self.Button5.on_press = self.rotate_btn
        self.buttons.add_widget(self.Button5)

        self.Button6 = Button(text="save",size=(100,50),
        font_size=10)
        self.Button6.on_press = self.save
        self.buttons.add_widget(self.Button6)

        self.Button7 = Button(text="load",size=(100,50),
        font_size=10)
        self.Button7.on_press = self.load_project
        self.buttons.add_widget(self.Button7)
        
        self.add_widget(self.buttons)
        with self.canvas.before:
            Color(68/255, 71/255, 90/255, 1.0)
            self.rect = Rectangle(pos=self.pos,size=self.size)

        
        self.bind(pos=self.update, size=self.update)
        self.load_project()

    def save(self):
        self.pcbs[self.atual_pcb] = pcb_to_json(self.components)

        if self.project:
            self.project["circuits"] = self.pcbs

        print(self.project)
    
    def load_project(self):
        
        for i in self.components.copy().keys():
            self.remove_widget(self.components.get(i))
            self.components.pop(i)

        if self.project:
            self.pcbs = self.project.get("circuits")
            print(self.pcbs)
            for c in json_to_pcb(self.pcbs[self.atual_pcb]).values():
                self.add_component(c)
            
            
        else:
            self.pcbs = {"0": {}}
            self.components = {}
            self.atual_pcb = "0"

        self.update()

    def update(self, *args):
        self.rect.pos = self.pos

        self.rect.size = self.size

        self.buttons.x = self.x-self.buttons.width
        self.buttons.y = self.y
        self.buttons.size = (100,self.height)

        


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
            self.remove_widget(self.components.get(self.select))
            self.components.pop(self.select)
            self.select = None

    def rotate_btn(self,*args):
        if self.select:
            print(self.select)
            cmpt = self.components.get(self.select)
            cmpt.rotate(cmpt.angle+45)


            
    def on_btn1(self,*args):
        newComponent(widget=self).open()
    
    def run(self,*args):
        
        for i in self.components.values():
            i.component.upgrade()

    def on_run(self,*args):
        if self.running:
            
            self.running.cancel()
            self.running = None

            for i in self.components.values():
                i.component.reset()

                if hasattr(i,"reset"):
                    i.reset()
                

            

        else:
            
            self.running = Clock.schedule_interval(self.run, 0.1)

    def on_set_circuit(self,*args):
        ChooseCircuit(circuit_editor=self).open()


def pcb_to_json(pcb: dict):
    components = {}
    for name,component in pcb.items():
        
        components[name] = {}
        

        if component.component.type == "resistor":
            components[name] = {
                "r": component.component.r
            }

        elif component.component.type == "source":
            components[name] = {
                "V": component.component.V,
                "I": component.component.I
            }

        elif component.component.type == "led":
            components[name] = {
                "r": component.component.r,
                "color": component.component.light_color,
                "off_color": component.component.off_color,
                "volts": component.component.volts,
                "current": component.component.current
            }

        components[name]["type"] = component.component.type
        connections = {}
        for k,i in component.component.terminals.items():
            connections[k] = []
            for n,c in i.out.items():
                connections[k] = [n,c[1]]

        components[name]["connections"] = connections
        components[name]['pos'] = component.circuit_pos
        components[name]['angle'] = component.angle
        components[name]['size'] = component.width

    print(components)
    return components


def json_to_pcb(json: dict):
    x = {}
    for name, component in json.items():
        print(name)
        if component["type"] == "resistor":
            
            obj = Resistor(name=name,pos=[0,0],size=[0,0])
            obj.component.r = component["r"]
            x[name] = obj

        elif component["type"] == "source":
            
            
            obj = Source(name=name)
            obj.component.V = component["V"]
            obj.component.I = component["I"]
            x[name] = obj

        elif component["type"] == "led":
            
            obj = Led(name=name,pos=[0,0],size=[0,0])
            obj.component.r = component["r"]
            obj.component.color = component["color"]
            obj.component.off_color = component["off_color"]
            obj.component.volts = component["volts"]
            obj.component.current = component["current"]
            x[name] = obj

        elif component["type"] == "multimeter":
            
            obj = Multimeter(name=name,pos=[0,0],size=[0,0])
            x[name] = obj

        size = component["size"]
        obj.circuit_pos = component["pos"]
        obj.size= size,size
        obj.rotate(component['angle'])

    for name, component in json.items():
        c1 = x[name].component
        for n,c in component["connections"].items():
            print(n,c)
            if len(c) > 0:
                c1.add_connection(x[c[0]].component, n, c[1])
                
    print(x)
    return x