from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_file("screens/world_screen.kv")


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
