from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import ObjectProperty


class TitleScreen(Screen):
    def play_button(self):
        self.manager.transition.direction = "left"
        self.manager.current = "battle"


class WorldScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        player = self.ids.player_character
        step = 100
        cur_x = player.pos[0]
        cur_y = player.pos[1]
        if text == "w":
            cur_y += step
        if text == "d":
            cur_x += step
        if text == "a":
            cur_x -= step
        if text == "s":
            cur_y -= step
        player.pos = (cur_x, cur_y)


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
        return WorldScreen()


if __name__ == "__main__":
    TurnBasedApp().run()
