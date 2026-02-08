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
    def skill_1_button(self):
        pass

    def skill_2_button(self):
        pass

    def skill_3_button(self):
        pass

    def skill_4_button(self):
        pass

    def backpack_button(self):
        p = BackpackPopup()
        p.open()

    def run_button(self):
        self.manager.transition.direction = "right"
        self.manager.current = "title"


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
