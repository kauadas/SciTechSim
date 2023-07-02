from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rotate


class RotationApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Cria um botão
        button = Button(text='Exemplo de rotação', size_hint=(None, None), size=(200, 100))
        layout.add_widget(button)

        # Define o ângulo de rotação do botão
        button.angle = 0  # Ângulo inicial

        # Cria um objeto Rotate para aplicar a rotação
        rotation = Rotate(angle=button.angle, origin=button.center)

        # Adiciona o objeto Rotate ao canvas do botão
        button.canvas.before.add(rotation)

        # Função para girar o botão
        def rotate_button(dt):
            button.angle += 1  # Aumenta o ângulo em 1 grau a cada chamada
            button.angle %= 360  # Mantém o ângulo no intervalo de 0 a 359 graus
            rotation.angle = button.angle  # Atualiza o ângulo de rotação

        # Adiciona a função de atualização de rotação ao Clock do Kivy
        from kivy.clock import Clock
        Clock.schedule_interval(rotate_button, 1 / 60.0)  # Atualiza a rotação a cada 1/60 segundos

        return layout


if __name__ == '__main__':
    RotationApp().run()
