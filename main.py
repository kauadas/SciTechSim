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
from kivy.graphics import Color, Rectangle

from modules import project_file
from pathlib import Path

project = None


def load_project(_dir: list):
    print("loading project")
    project = project_file.project(_dir[0])

class screenManager0(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.add_widget(home())



class fileSelector(Popup):
    def __init__(self,_type: list = None,data: str = "",callback=None, **kwargs):
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
        if self.type != "":
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

        touch = App.get_running_app().root_window.mouse_pos
        ww, wh = App.get_running_app().root_window.size

        self.title=""
        self.size_hint=(None,None)
        self.size=(200,500)
        self.pos_hint={'x': touch[0]/ww,'top': touch[1]/wh}

        
        stack_layout.add_widget(open_)
        self.add_widget(stack_layout)

    def open_on_press(self,*args):
        
        file = fileSelector(_type=[".json"],callback=load_project)
        file.open()
        self.dismiss()

class home(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.actionbar = BoxLayout(size_hint=(1,None),height=20,pos=(2,2))
        
        self.project = Button(text="project",size_hint=(None,1),width=50,
                              background_color=(0,0,0,0))
        
        self.file = Button(text="file",size_hint=(None,1),width=50,
                           background_color=(0,0,0,0))
        
        self.project.on_press = self.project_pop_up
        self.file.on_press = self.file_pop_up
        
        self.actionbar.add_widget(self.project)
        self.actionbar.add_widget(self.file)

        with self.canvas.before:
           Color(40/255, 42/255, 54/255,1)
           self.rect0 = Rectangle(size=(50,50),pos=(0,0))
           Color(68/255, 71/255, 90/255, 1.0)
           self.rect1 = Rectangle(size=(9999,20),pos=(0,0))


        
        
        self.bind(size=self.on_resize)

        self.add_widget(self.actionbar)
        

    def on_resize(self,w,size):
        print(size)
        self.rect0.size = size
        self.rect1.size = (size[0],20)
        self.rect1.pos = (0,size[1]-20)

        self.actionbar.pos = (0,size[1]-20)
        
    def project_pop_up(self,**args):
        ProjectPopUp().open()

    

        

    

        
        

    
        



        

class SciTechSim(App):
    def build(self):
        
        return screenManager0()


SciTechSim().run()