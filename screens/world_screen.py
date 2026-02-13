from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder
import random

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
        map_area = self.ids.map_area
        step = 100
        cur_x = player.pos[0]
        cur_y = player.pos[1]
        if text == "w":
            cur_y += step
        elif text == "d":
            cur_x += step
        elif text == "a":
            cur_x -= step
        elif text == "s":
            cur_y -= step
        else:
            return
        # Boundary checks
        if cur_x < 0:
            cur_x = 0
        right_boundary = map_area.width - player.width
        if cur_x > right_boundary:
            cur_x = right_boundary
            cur_x = right_boundary
        if cur_y < 0:
            cur_y = 0
        top_boundary = map_area.height - player.height
        if cur_y > top_boundary:
            cur_y = top_boundary
        player.pos = (cur_x, cur_y)

        grass = self.ids.grass_area
        if player.collide_widget(grass):
            if random.randint(1, 100) <= 20:  # โอกาส 20%
                self.manager.transition.direction = "left"
                self.manager.current = "battle"
