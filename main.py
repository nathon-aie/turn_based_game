from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup


class TitleScreen(Screen):
    def play_button(self):
        self.manager.transition.direction = "left"
        self.manager.current = "battle"


class BackpackPopup(Popup):
    pass


class BattleScreen(Screen):
    pass


class TurnBasedApp(App):
    def quit_button(self):
        self.stop()

    def build(self):
        Window.size = (720, 480)
        sm = ScreenManager()
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(BattleScreen(name="battle"))
        return sm


if __name__ == "__main__":
    TurnBasedApp().run()
