from modules import physic

from kivy.uix.widget import Widget


class physicEditor(widget):
    def __init__(self):
        self.ambient = physic.ambient()