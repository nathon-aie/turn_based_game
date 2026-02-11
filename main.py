from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import StringProperty
from kivy.event import EventDispatcher


class TitleScreen(Screen):
    def play_button(self):
        self.manager.transition.direction = "left"
        self.manager.current = "battle"


class WorldScreen(Screen):
    pass


class BackpackPopup(Popup):
    def __init__(self, item_list, callback_func, **kwargs):
        super().__init__(**kwargs)
        self.callback_func = callback_func
        grid = self.ids.item_grid_layout
        for item_name in item_list:
            btn = Factory.ItemButton(text=f"{item_name} x{item_list[item_name]}")
            btn.bind(on_release=lambda instance, x=item_name: self.on_item_click(x))
            grid.add_widget(btn)

    def on_item_click(self, item_name):
        self.callback_func(item_name)
        self.dismiss()


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
        items = {"Item 1": 10, "Item 2": 20, "Item 3": 30}
        p = BackpackPopup(item_list=items, callback_func=self.update_selection)
        p.open()

    def update_selection(self, selected_item):
        self.ids.result_label.text = f"Select: {selected_item}"

    def run_button(self):
        self.manager.transition.direction = "right"
        self.manager.current = "title"


class TurnBasedApp(App):
    def quit_button(self):
        self.stop()

    def build(self):
        Window.size = (720, 480)
        # sm = ScreenManager()
        # sm.add_widget(TitleScreen(name="title"))
        # sm.add_widget(BattleScreen(name="battle"))
        # return sm
        return WorldScreen()


if __name__ == "__main__":
    TurnBasedApp().run()
