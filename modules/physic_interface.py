from modules import physic

from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics import *
from math import degrees,atan

class body(Widget):
    def __init__(self,obj_json,**kwargs):
        super().__init__(**kwargs)
        self.id = obj_json.get("id")

        self.axis_render = 0
        self.matrix_json = obj_json.get("matrix",{})
        self.matrix = {}
        
        self.body = physic.body(id=self.id,m=obj_json.get("m",0),Q=obj_json.get("Q",0),pos=obj_json.get("pos"),
        matrix=self.matrix_json)
        
        self.pos = self.body.pos.values[:2]

        self.scale = (0.175)/(self.body.pos[2]+0.175)
        self.rot = Rotate()
        self.rot.angle = 0
        self.canvas.add(self.rot)
        self.size = [x*self.scale for x in obj_json.get("size")[:2]]
        self.draw()


    def draw(self):
        
        for k,v in self.matrix_json.items():
            if v.get('type') == "ellipse":
                self.matrix[k] = Ellipse()
                self.matrix[k].angle_start = v.get('angle_start',0)
                self.matrix[k].angle_end = v.get('angle_end',360)
                pos = [x+y for x,y in zip(self.pos,v.get('pos',[0,0,0])[:2])]
                print(pos)
                self.matrix[k].pos = pos
                self.matrix[k].size = v.get("size",(5,5,5))[:2]
                
                print(self.matrix[k].pos)

            elif v.get('type') == "rectangle":
                self.matrix[k] = Rectangle()
                pos = [x+y for x,y in zip(self.pos,v.get('pos',[0,0,0])[:2])]
                print(pos)
                self.matrix[k].pos = pos
                self.matrix[k].size = v.get("size",(5,5,5))[:2]
                
                print(self.matrix[k].pos)

            self.canvas.add(Color(*v.get("color",[1,1,1,1])))
            self.canvas.add(self.matrix[k])
    

    
    def update(self):
        
        print("0,0",self.parent.pos)
        self.x = self.body.pos.values[0] + self.parent.x
        self.y = self.body.pos.values[1] + self.parent.y
        print("x",self.x)


        self.rot.origin = self.center
        self.rot.angle = self.body.angle[self.axis_render]
        for k,v in self.matrix.items():
            x,y,z = self.matrix_json[k].get('pos',[0,0,0])
            v.pos = self.x + x,self.y + y
            print(v)

        

class editAmbient(Popup):
    def __init__(self,ambient: physic.ambient,**kwargs):
        super().__init__(**kwargs)

        self.ambient = ambient

        self.title = "ambient edit"
        self.size_hint = (None,None)
        self.size = (400,400)
        self.mainLayout = BoxLayout()
        self.inputs = GridLayout(cols=2,row_force_default=True, row_default_height=30)
        self.label_g = Label(text="gravitacional constant = ",size_hint_x=None,width=100,font_size=10)
        self.G = TextInput(multiline=False,size_hint_x=None,width=100,text=str(ambient.G),font_size=10,halign="center")
        self.label_k = Label(text="electric constant =",size_hint_x=None,width=100,font_size=12.5)
        self.k = TextInput(multiline=False,size_hint_x=None,width=100,text=str(ambient.K),font_size=10,halign="center")

        self.add_widget(self.mainLayout)
        self.mainLayout.add_widget(self.inputs)
        self.inputs.add_widget(self.label_g)
        self.inputs.add_widget(self.G)
        self.inputs.add_widget(self.label_k)
        self.inputs.add_widget(self.k)

        self.ok = Button(text="OK",size_hint=(None,None),size=(50,100))
        self.ok.on_press = self.dismiss
        self.mainLayout.add_widget(self.ok)

    def on_dismiss(self):
        self.ambient.G = eval(self.G.text)
        self.ambient.K = eval(self.k.text)

class PhysicEditor(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.run_state = None
        self.ambient = physic.ambient()
        self.widgets = {}
        self.ambient.G = kwargs.get("G",physic.G)
        self.ambient.K = kwargs.get("K",physic.K)
        
        self.Button1 = Button(background_normal="./assets/config.png",size=(50,50),pos=self.pos,
        font_size=10)
        self.Button1.on_press = self.on_btn1
        with self.Button1.canvas.after:
            self.icon1 = Rectangle(size=self.Button1.size,source="./assets/config.png",pos=self.pos)
        self.add_widget(self.Button1)

        with self.canvas:
            Color(68/255, 71/255, 90/255, 1.0)
            self.background = Rectangle()

        self.bind(pos=self.update, size=self.update)
        

    def update(self,*args):
        
        self.background.pos = self.pos
        self.background.size = self.size
        self.Button1.pos = (self.x-50,(self.y+self.height)-50)
        self.icon1.pos = self.Button1.pos
        
        print("pos",self.pos)
        for b in self.widgets.values():
            b.update()


    def on_btn1(self,*args):
        editAmbient(ambient=self.ambient).open()

    def add_body(self,body_: body):
        self.ambient.objects[body_.id] = body_.body
        self.widgets[body_.id] = body_
        self.add_widget(body_)

    def remove_body(self,body_: body):
        self.ambient.objects.pop(body_.id)
        self.widgets.pop(body_.id)
        self.remove_widget(body_)

    def run(self,*args):
        self.ambient.upgrade()
        for i in self.widgets.values():
            i.update()

    def init(self,*args):
        if self.run_state == None:
            self.run_state = Clock.schedule_interval(self.run,0.15)

        else:
            self.run_state.cancel()
            self.run_state = None