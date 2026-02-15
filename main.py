from kivy.config import Config

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "720")
Config.set("graphics", "height", "480")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.title_screen import TitleScreen
from screens.battle_screen import BattleScreen
from screens.world_screen import WorldScreen


class TurnBasedApp(App):
    def quit_button(self):
        self.stop()

    def build(self):
        # Window.size = (720, 480)
        sm = ScreenManager()
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(BattleScreen(name="battle"))
        sm.add_widget(WorldScreen(name="world"))
        return sm


if __name__ == "__main__":
    TurnBasedApp().run()
