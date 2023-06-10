from kivy.app import App

from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.layout import Layout
from kivy.graphics import Color, Rectangle, Line

from modules.eletronic_interface import Resistor,CircuitEditor

from modules import project_file
from pathlib import Path

project = None


def load_project(_dir: list):
    global project
    print("loading project",_dir)
    project = project_file.project(_dir[0])

class screenManager0(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.add_widget(home())
        self.add_widget(pcbEditor())



class fileSelector(Popup):
    def __init__(self,_type: list = [],data: str = "",callback=None, **kwargs):
        super().__init__(**kwargs)
        base = BoxLayout(orientation='vertical')
        
        self.callback = callback
        self.type = _type or ""
        self.data = data
        self.title = "select a file"
        self.size_hint = (None,None)
        self.size = (400,400)

        self.files = []

        file_chooser = FileChooserIconView()
        if len(self.type) > 0:
            file_chooser.filters = map(lambda x: "*"+x, self.type)
        
        file_chooser.rootpath = str(Path.home())
        
        btn_new = Button(text="new file")
        btn_new.size_hint = (None,None)
        btn_new.size = (50,30)
        btn_new.on_press = lambda *args: self.new_file(str(file_chooser.path))

        btn_ok = Button(text="ok")
        btn_ok.size_hint = (None,None)
        btn_ok.size = (50,30)
        btn_ok.on_press = lambda **args: self.on_ok_press(file_chooser.selection)

        self.add_widget(base)

        base.add_widget(file_chooser)
        buttons = BoxLayout(size_hint=(1,None),height=30)
        buttons.add_widget(btn_new)
        buttons.add_widget(btn_ok)

        base.add_widget(buttons)

    def new_file(self,_dir: str):
        self.popup0 = Popup(title="new file")
        self.popup0.size_hint = (None,None)
        self.popup0.size = (200,200)

        boxlayout = BoxLayout(orientation = 'vertical')
        filename = TextInput(hint_text='filename',multiline=False)

        btn_create = Button(text="create",size_hint=(1,None),height=30)
        btn_create.on_press = lambda **args: self.create(_dir+"/"+filename.text)
        
        boxlayout.add_widget(filename)
        boxlayout.add_widget(btn_create)
        self.popup0.add_widget(boxlayout)


        self.popup0.open()

    def on_ok_press(self,files: list):
        if self.callback:
            self.callback(files)
        self.dismiss()

    def create(self,_dir: str):
       with open(_dir,"x") as d:
           d.write(self.data)
           d.close()

       self.popup0.dismiss()



class ProjectPopUp(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        stack_layout = StackLayout(orientation='tb-lr')
        

        open_ = Button(text='open project',size_hint = (None,None),size=(100,30))
        open_.background_color = (0,0,0,0)

        open_.on_press = self.open_on_press

        save = Button(text='save project',size_hint = (None,None),size=(100,30))
        save.background_color = (0,0,0,0)

        save.on_press = self.save

         
        touch = App.get_running_app().root_window.mouse_pos
        ww, wh = App.get_running_app().root_window.size

        self.title=""
        self.size_hint=(None,None)
        self.size=(200,500)
        self.pos_hint={'x': touch[0]/ww,'top': touch[1]/wh}

        
        stack_layout.add_widget(open_)
        stack_layout.add_widget(save)
        self.add_widget(stack_layout)

    def save(self,*args):
        if project:
            project.save()
        
        message = Popup()
        message.title = ""
        message_text = Label(text="projeto salvo!!!")
        message.size_hint = (None,None)
        message.size = (200,200)
        message.add_widget(message_text)
        message.open()
        self.dismiss()
    def open_on_press(self,*args):
        
        file = fileSelector(_type=[".json"],callback=load_project)
        file.open()
        self.dismiss()

from kivy.uix.widget import Widget



class SimulationEditor(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas:
            Color(0,0,0,1)
            self.rect = Rectangle(pos=self.pos,size=self.size)

        
        self.bind(size=self.update_size,pos=self.update_pos)

    def update_size(self,w,size):
        self.rect.size = size

    def update_pos(self,w,pos):
        self.rect.pos = pos

class action_bar(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1,None)
        self.height = 20


        
        self.project = Button(text="project",size_hint=(None,1),width=50,
                              background_color=(0,0,0,0))
        
        self.home = Button(text="Home",size_hint=(None,1),width=50,
                           background_color=(0,0,0,0))
        self.home.on_press = lambda *args: self.trocar_tela("home")

        self.pcb = Button(text="Pcb Editor",size_hint=(None,1),width=70,
                           background_color=(0,0,0,0))
        self.pcb.on_press = lambda *args: self.trocar_tela("pcbeditor")
        
        self.project.on_press = self.project_pop_up
        
        
        
        self.add_widget(self.project)
        self.add_widget(self.home)
        self.add_widget(self.pcb)

        with self.canvas.before:
            Color(68/255, 71/255, 90/255, 1.0)
            self.rect = Rectangle(size=(9999,20),pos=(0,0))

        self.bind(size=self.update_size,pos=self.update_pos)

    def update_size(self,w,size):
        self.rect.size = size

    def update_pos(self,w,pos):
        self.rect.pos = pos


    def project_pop_up(self,**args):
        ProjectPopUp().open()

    def trocar_tela(self,tela):
        App.get_running_app().root.current = tela


class home(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.name = "home"

        self.actionbar = action_bar()
        
        with self.canvas.before:
           Color(40/255, 42/255, 54/255,1)
           self.rect0 = Rectangle(size=(50,50),pos=(0,0))
           

        self.rect1 = self.actionbar.rect
        
        
        self.bind(size=self.on_resize)

        self.add_widget(self.actionbar)
        

    def on_resize(self,w,size):
        
        self.rect0.size = size
        

        self.actionbar.pos = (0,size[1]-20)
        

class pcbEditor(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.name = "pcbeditor"

        self.actionbar = action_bar()

        self.circuit_editor = CircuitEditor()
        self.circuit_editor.size_hint = (0.5,0.6)
        self.circuit_editor.pos_hint = {
            "center_x": 0.5,
            "center_y": 0.5
        }
        
        self.R1 = Resistor(size=(100,100),pos=(200,100))
        self.circuit_editor.add_component(self.R1)
        
        
        with self.canvas.before:
           Color(40/255, 42/255, 54/255,1)
           self.rect0 = Rectangle(size=(50,50),pos=(0,0))
           

        self.rect1 = self.actionbar.rect
        
        
        self.bind(size=self.on_resize)

        self.add_widget(self.actionbar)
        self.add_widget(self.circuit_editor)
        

    def on_resize(self,w,size):
       
        self.rect0.size = size
        
        self.actionbar.pos = (0,size[1]-20)

        self.R1.pos = self.circuit_editor.pos
        
        

class GeneralEditor(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.name = "editor"

        self.actionbar = action_bar()
        
        with self.canvas.before:
           Color(40/255, 42/255, 54/255,1)
           self.rect0 = Rectangle(size=(50,50),pos=(0,0))
           

        self.rect1 = self.actionbar.rect
        
        
        self.bind(size=self.on_resize)

        self.add_widget(self.actionbar)
        

    def on_resize(self,w,size):
        print(size)
        self.rect0.size = size
        self.rect1.size = (size[0],20)
        self.rect1.pos = (0,size[1]-20)

        self.actionbar.pos = (0,size[1]-20)
        
class SciTechSim(App):
    def build(self):
        
        return screenManager0()

if __name__ == "__main__":
    SciTechSim().run()