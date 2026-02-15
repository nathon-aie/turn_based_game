from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import random
import json
import os

from widgets.stats import StatusPopup
from widgets.backpack import BackpackPopup

Builder.load_file("screens/world_screen.kv")

# พื้นที่และข้อมูลแผนที่
TILE_SIZE = 60
SPAWN_POINT = (60, 60)
tile_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 1, 2, 2, 1],
    [1, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 1, 2, 2, 1],
    [1, 0, 2, 2, 0, 1, 1, 1, 1, 0, 0, 1, 2, 2, 1],
    [1, 0, 0, 0, 0, 1, 3, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 3, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class WorldScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        Clock.schedule_once(self.check_auto_load, 0)  # โหลดเซฟอัตโนมัติ
        self.bgm = SoundLoader.load("audio/mambo-matikanetannhauser.mp3")

    # เมื่อหน้าจอถูกปิดให้ยกเลิกการจับคีย์บอร์ด
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    # จัดการการเคลื่อนที่ของตัวละครและการตรวจสอบชนิดของพื้นผิว
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        player = self.ids.player_character
        cur_col = int(player.pos[0] / TILE_SIZE)
        cur_row = int(player.pos[1] / TILE_SIZE)
        next_col = cur_col
        next_row = cur_row
        if text == "w":
            next_row += 1
        elif text == "d":
            next_col += 1
        elif text == "a":
            next_col -= 1
        elif text == "s":
            next_row -= 1
        else:
            return
        if (
            next_row < 0
            or next_row >= len(tile_map)
            or next_col < 0
            or next_col >= len(tile_map[0])
        ):
            return
        target_tile = tile_map[next_row][next_col]
        if target_tile == 1:
            return
        if target_tile == 3:  # ตกน้ำ (วาร์ปกลับจุดเกิด)
            player.pos = SPAWN_POINT
            return
        player.pos = (next_col * TILE_SIZE, next_row * TILE_SIZE)
        if target_tile == 2:
            if random.randint(1, 100) <= 20:
                self.manager.transition.direction = "left"
                self.manager.current = "battle"

    # เมื่อเข้าหน้าจอให้วาดแผนที่
    def on_enter(self):
        self.draw_map()
        self.bgm.loop = True
        self.bgm.play()

    def on_leave(self):
        self.bgm.stop()

    # สร้างแผนที่จากข้อมูลใน tile_map และวาดบนหน้าจอ
    def draw_map(self):
        map_area = self.ids.map_area
        with map_area.canvas.before:
            for row_index, row_data in enumerate(tile_map):
                for col_index, tile_type in enumerate(row_data):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    if tile_type == 1:  # Wall
                        Color(0.5, 0.5, 0.5, 1)
                    elif tile_type == 2:  # Bush
                        Color(0, 0.5, 0, 1)
                    elif tile_type == 3:  # Water (ฟ้า)
                        Color(0, 0.4, 0.8, 1)
                    else:  # Ground (0)
                        Color(0.2, 0.8, 0.2, 1)
                    Rectangle(pos=(x, y), size=(TILE_SIZE, TILE_SIZE))

    # ปุ่มสถานะของ Hero
    def status_button(self):
        character = self.manager.get_screen("battle")  # ดึงข้อมูลจาก Battle Screen
        popup = StatusPopup(character.hero)
        popup.open()

    # ปุ่มไอเทมในกระเป๋า
    def backpack_button(self):
        backpack = self.manager.get_screen("battle")  # ดึงข้อมูลจาก Battle Screen
        popup = BackpackPopup(item_list=backpack.inventory, callback_func=None)
        popup.open()

    # ปุ่มออกจากเกมกลับไปหน้า Title Screen
    def exit_button(self):
        self.manager.transition.direction = "right"
        self.manager.current = "title"

    # ปุ่มเซฟเกม
    def save_game(self):
        battle_screen = self.manager.get_screen("battle")  # ดึงข้อมูลจาก Battle Screen
        # สร้างข้อมูลเซฟจาก Hero, Inventory, ตำแหน่งปัจจุบัน
        save_data = {
            "hero": battle_screen.hero.to_dict(),
            "inventory": battle_screen.inventory,
            "position": self.ids.player_character.pos,
        }
        # บันทึกข้อมูลลงไฟล์ JSON
        with open("savefile.json", "w") as f:
            json.dump(save_data, f, indent=4)
            print("Game saved successfully.")

    # โหลดเกม
    def load_game(self):
        # เปิดไฟล์ JSON และโหลดข้อมูลกลับมาใช้ในเกม
        with open("savefile.json", "r") as f:
            data = json.load(f)
        battle_screen = self.manager.get_screen("battle")
        if not battle_screen.hero:
            battle_screen.spawn_hero()
        hero_data = data.get("hero")
        if hero_data:
            battle_screen.hero.load_from_dict(hero_data)
        inventory_data = data.get("inventory")
        if inventory_data:
            battle_screen.inventory = inventory_data
        pos_data = data.get("position")
        if pos_data:
            self.ids.player_character.pos = tuple(pos_data)
        print("Game Loaded Successfully!")

    # โหลดเซฟอัตโนมัติ
    def check_auto_load(self, dt):
        if os.path.exists("savefile.json"):
            self.load_game()
