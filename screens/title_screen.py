from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("screens/title_screen.kv")


class TitleScreen(Screen):
    def play_button(self):
        self.manager.transition.direction = "left"
        self.manager.current = "battle"
