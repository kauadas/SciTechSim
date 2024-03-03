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
from kivy.graphics.transformation import Matrix
from math import degrees,atan
from modules.md2 import Model



class body(Widget):
    def __init__(self,obj_json,md2: str,**kwargs):
        super().__init__(**kwargs)
        self.json = obj_json
        self.id = obj_json.get("id")

        self.axis_render = 0
        self.matrix_json = obj_json.get("matrix",{})
        self.md = Model()
        self.md.load(md2)
        self.canvas_list = []
        self.matrix = {}
        
        self.body = physic.body(id=self.id,m=obj_json.get("m",0),Q=obj_json.get("Q",0),pos=obj_json.get("pos"),
        matrix=self.matrix_json)
        
        self.pos = self.body.pos.values[:2]

        self.scale = 1-((5/200)*self.body.pos.values[2])

        self.size = [i*self.scale for i in obj_json.get("size")[:2]]

        with self.canvas:
            self.draw()


    def draw(self):
        for i in self.md.objs[0]:
            if i.get('type') == 'Circle':
                Color(*[x/255 for x in i.get('color')])
                x=Ellipse(size=(i.get('radius')*self.scale,i.get('radius')*self.scale),pos=[x+y for x,y in zip(i.get('pos'),self.pos)])
                self.canvas_list.append((x,i))



    

    
    def update(self):
        
        print("0,0",self.parent.pos)
        self.x = self.body.pos.values[0] + self.parent.x
        self.y = self.body.pos.values[1] + self.parent.y
        print("x",self.x)

        for i in self.canvas_list:
            i[0].pos = [x+y for x,y in zip(i[1].get('pos'),self.pos)]
            i[0].size = (i[1].get('radius')*self.scale,i[1].get('radius')*self.scale)

        

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

        self.ok = Button(text="OK",size_hint=(None,None),size=(50,50))
        self.ok.on_press = self.dismiss
        self.mainLayout.add_widget(self.ok)

    def on_dismiss(self):
        self.ambient.G = eval(self.G.text)
        self.ambient.K = eval(self.k.text)


class createBody(Popup):
    def __init__(self,editor,**kwargs):
        super().__init__(**kwargs)

        self.ambient = editor.ambient

        self.editor = editor
        self.title = "new body"
        self.size_hint = (None,None)
        self.size = (400,400)
        self.mainLayout = BoxLayout()
        self.inputs = GridLayout(cols=2,row_force_default=True, row_default_height=30)
        self.label_m = Label(text="mass = ",size_hint_x=None,width=100,font_size=10)
        self.m = TextInput(multiline=False,size_hint_x=None,width=100,text=str(0),font_size=10,halign="center")
        self.label_name = Label(text="name = ",size_hint_x=None,width=100,font_size=10)
        self.name = TextInput(multiline=False,size_hint_x=None,width=100,text=str(0),font_size=10,halign="center")
        self.label_q = Label(text="charge =",size_hint_x=None,width=100,font_size=12.5)
        self.q = TextInput(multiline=False,size_hint_x=None,width=100,text=str(0),font_size=10,halign="center")
        self.label_size = Label(text="size =",size_hint_x=None,width=100,font_size=12.5)
        self.nsize = TextInput(multiline=False,size_hint_x=None,width=100,text=str((10,10,10)),font_size=10,halign="center")
        self.label_pos = Label(text="pos =",size_hint_x=None,width=100,font_size=12.5)
        self.npos = TextInput(multiline=False,size_hint_x=None,width=100,text=str((0,0,0)),font_size=10,halign="center")
        self.label_md2 = Label(text="md2_file = ",size_hint_x=None,width=100,font_size=10)
        self.md2 = TextInput(multiline=False,size_hint_x=None,width=100,text=str(0),font_size=10,halign="center")
        
        self.add_widget(self.mainLayout)
        self.mainLayout.add_widget(self.inputs)
        self.inputs.add_widget(self.label_m)
        self.inputs.add_widget(self.m)
        self.inputs.add_widget(self.label_q)
        self.inputs.add_widget(self.q)
        self.inputs.add_widget(self.label_size)
        self.inputs.add_widget(self.nsize)
        self.inputs.add_widget(self.label_pos)
        self.inputs.add_widget(self.npos)
        self.inputs.add_widget(self.label_md2)
        self.inputs.add_widget(self.md2)
        self.ok = Button(text="OK",size_hint=(None,None),size=(50,50))
        self.ok.on_press = self.dismiss
        self.mainLayout.add_widget(self.ok)

    def on_dismiss(self):
        body_json = {
            "m": eval(self.m.text),
            "Q": eval(self.q.text),
            "size": eval(self.nsize.text),
            "pos": eval(self.npos.text)
        }
        body_var = body(body_json,self.md2.text)
        self.editor.add_body(body_var)


class PhysicEditor(Widget):
    def __init__(self,project,**kwargs):
        super().__init__(**kwargs)

        self.ambient = physic.ambient()
        self.project = project
        self.run_state = None
        self.load_project()
        self.buttons = GridLayout(cols=1,row_force_default=True, row_default_height=50)
        self.Button1 = Button(text="edit ambient",width=50,pos=self.pos,
        font_size=8)
        self.Button1.on_press = self.on_btn1
        self.buttons.add_widget(self.Button1)
        self.Button2 = Button(text="new body",width=50,pos=self.pos,
        font_size=8)
        self.Button2.on_press = self.on_btn2
        self.buttons.add_widget(self.Button2)
        self.buttons.size_hint_x = None
        self.buttons.width = 50
        self.add_widget(self.buttons)

        with self.canvas:
            Color(68/255, 71/255, 90/255, 1.0)
            self.background = Rectangle()

        self.bind(pos=self.update, size=self.update)
        

    def update(self,*args):
        
        self.background.pos = self.pos
        self.background.size = self.size
        self.buttons.pos = (self.x-50,(self.y+self.height)-100)
        
        
        print("pos",self.pos)
        for b in self.widgets.values():
            b.update()


    def on_btn1(self,*args):
        editAmbient(ambient=self.ambient).open()

    def on_btn2(self,*args):
        obj_creator = createBody(self)
        obj_creator.open()

    def add_body(self,body_: body):
        self.ambient.objects[body_.id] = body_.body
        self.widgets[body_.id] = body_
        self.add_widget(body_)

    def remove_body(self,body_: body):
        self.ambient.objects.pop(body_.id)
        self.widgets.pop(body_.id)
        self.remove_widget(body_)

    def load_project(self):
        
        for i in self.ambient.objects.copy().keys():
            self.remove_body(i)
        self.ambient = physic.ambient()
        
        

        self.widgets = {}

        if self.project != None:
            self.ambient_project = self.project.get("ambients")
            self.ambient.G = self.ambient_project.get("G",physic.G)
            self.ambient.K = self.ambient_project.get("K",physic.K)
            for b in self.ambient_project.get("bodys").values():
                nb = body(b)
                self.add_body(nb)

        else:
            self.ambient.G = physic.G
            self.ambient.K = physic.K

    def save_project(self):
        pass


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