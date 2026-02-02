from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen


class BattleScreen(Screen):
    pass


class TurnBasedApp(App):
    def build(self):
        Window.size = (720, 480)
        return BattleScreen()


if __name__ == "__main__":
    TurnBasedApp().run()
