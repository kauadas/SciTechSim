from modules import physic

from kivy.uix.widget import Widget
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

        


    

class PhysicEditor(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.run_state = None
        self.ambient = physic.ambient()
        self.widgets = {}
        self.ambient.G = kwargs.get("G",physic.G)
        self.ambient.K = kwargs.get("K",physic.K)
        
        with self.canvas:
            Color(68/255, 71/255, 90/255, 1.0)
            self.background = Rectangle()

        self.bind(pos=self.update, size=self.update)
        

    def update(self,*args):
        self.background.pos = self.pos
        self.background.size = self.size
        print("pos",self.pos)
        for b in self.widgets.values():
            b.update()

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