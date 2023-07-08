from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
import math

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=(100, 100))
            self.rotate(45)
        self.angle = 45  # Ângulo de rotação do widget (em graus)

    def on_touch_up(self, touch):
        dx = 1  # Deslocamento na coordenada X
        dy = 1  # Deslocamento na coordenada Y

        angle_rad = math.radians(self.angle)  # Converter o ângulo de graus para radianos

        # Aplicar correção na posição com base no ângulo
        corrected_dx = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
        corrected_dy = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)

        self.rect.pos = (self.rect.pos[0] + corrected_dx, self.rect.pos[1] + corrected_dy)  # Atualizar a posição do retângulo

class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()
