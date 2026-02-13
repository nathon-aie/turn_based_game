from kivy.uix.screenmanager import Screen
from widgets.backpack import BackpackPopup
from kivy.lang import Builder
import random
import time

Builder.load_file("screens/battle_screen.kv")


class Enemy:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp


class Hero:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp


class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_enemy = None

    def on_enter(self):
        self.spawn_hero()
        self.spawn_enemy()
        self.update_ui()

    def spawn_hero(self):
        self.hero = Hero("Mambo", 100)

    def spawn_enemy(self):
        possible_enemies = [
            Enemy("Noob Slayer", 50),
            Enemy("Goblin Slayer", 80),
            Enemy("God Slayer", 30),
        ]
        self.current_enemy = random.choice(possible_enemies)

    def update_ui(self):
        if self.current_enemy:
            display_text = f"{self.current_enemy.name}\nHP: {self.current_enemy.hp}"
            self.ids.enemy_stat_label.text = display_text
        if self.hero:
            display_text = f"{self.hero.name}\nHP: {self.hero.hp}"
            self.ids.hero_stat_label.text = display_text

    def check_enemy_status(self):
        if self.current_enemy.hp <= 0:
            self.current_enemy.hp = 0
            self.ids.result_label.text = f"Victory! {self.current_enemy.name} defeated."

    def skill_1_button(self):
        # skill testing
        if self.current_enemy and self.current_enemy.hp > 0:
            damage = 15
            self.current_enemy.hp -= damage
            self.check_enemy_status()
            self.update_ui()

    def skill_2_button(self):
        # skill testing
        if self.current_enemy and self.current_enemy.hp > 0:
            damage = 10
            self.current_enemy.hp -= damage
            self.check_enemy_status()
            self.update_ui()

    def skill_3_button(self):
        # skill testing
        if self.current_enemy and self.current_enemy.hp > 0:
            damage = 20
            self.current_enemy.hp -= damage
            self.check_enemy_status()
            self.update_ui()

    def skill_4_button(self):
        # skill testing
        max_hp = self.hero.hp
        if self.hero.hp < max_hp:
            heal = 20
            self.hero.hp += heal
            if self.hero.hp > max_hp:
                self.hero.hp = max_hp
            self.check_enemy_status()
            self.update_ui()

    def backpack_button(self):
        items = {"Item 1": 10, "Item 2": 20, "Item 3": 30}
        p = BackpackPopup(item_list=items, callback_func=self.update_selection)
        p.open()

    def update_selection(self, selected_item):
        self.ids.result_label.text = f"Select: {selected_item}"

    def run_button(self):
        self.manager.transition.direction = "right"
        self.manager.current = "world"
