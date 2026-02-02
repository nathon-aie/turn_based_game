from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen


class TitleScreen(Screen):
    pass


class BattleScreen(Screen):
    pass


class TurnBasedApp(App):
    def build(self):
        Window.size = (720, 480)
        sm = ScreenManager()
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(BattleScreen(name="battle"))
        return sm


if __name__ == "__main__":
    TurnBasedApp().run()
