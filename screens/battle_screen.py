from kivy.uix.screenmanager import Screen
from widgets.backpack import BackpackPopup
from kivy.lang import Builder
from kivy.clock import Clock
from objects.hero import Hero
from objects.enemy import Enemy
import random

Builder.load_file("screens/battle_screen.kv")


class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_enemy = None
        self.is_player_turn = True
        self.spawn_hero()
        self.inventory = {"Potion": 10, "Bomb": 10}

    def button_disabled(self, *args):
        self.ids.skill_1.disabled = True
        self.ids.skill_2.disabled = True
        self.ids.skill_3.disabled = True
        self.ids.skill_4.disabled = True
        self.ids.backpack.disabled = True
        self.ids.run.disabled = True

    def button_enabled(self, *args):
        self.ids.skill_1.disabled = False
        self.ids.skill_2.disabled = False
        self.ids.skill_3.disabled = False
        self.ids.skill_4.disabled = False
        self.ids.backpack.disabled = False
        self.ids.run.disabled = False

    def on_enter(self):
        self.hero.atk_buff = 1
        self.spawn_enemy()
        self.update_ui()
        Clock.schedule_once(self.enable_skills, 1)
        self.button_disabled()
        self.ids.result_label.text = f"{self.current_enemy.name} appears!"

    def enable_skills(self, dt):
        self.button_enabled()
        self.ids.result_label.text = "Fight!"
        self.ids.run.text = "Run"
        self.start_player_turn()

    def spawn_hero(self):
        self.hero = Hero("Mambo", 100, 15)

    def spawn_enemy(self):
        possible_enemies = [
            Enemy("Noob Slayer", 30, 10),
            Enemy("Goblin Slayer", 50, 12),
            Enemy("God Slayer", 80, 18),
            Enemy("Anuthin", 100, 20),
            Enemy("Anuthin Slayer", 150, 25),
        ]
        self.current_enemy = random.choice(possible_enemies)

    def update_ui(self):
        if self.current_enemy:
            if self.current_enemy.hp < 0:
                self.current_enemy.hp = 0
            display_text = f"{self.current_enemy.name}\nHP: {self.current_enemy.hp}"
            self.ids.enemy_stat_label.text = display_text
        if self.hero:
            if self.hero.hp < 0:
                self.hero.hp = 0
            self.ids.hero_stat_label.text = f"{self.hero.name}\nHP: {self.hero.hp}"

    def check_enemy_status(self):
        if self.current_enemy.hp <= 0:
            self.current_enemy.hp = 0
            self.ids.result_label.text = f"Victory! {self.current_enemy.name} defeated."
            self.ids.run.text = "Exit"
            self.button_disabled()
            self.ids.run.disabled = False
            return True
        return False

    def check_hero_status(self):
        if self.hero.hp <= 0:
            self.hero.hp = 0
            self.ids.result_label.text = "Game Over... You died."
            self.button_disabled()
            self.ids.run.text = "Exit"
            self.ids.run.disabled = False
            return True
        return False

    def skill_1_button(self):
        if not self.is_player_turn:
            return
        if self.current_enemy and self.current_enemy.hp > 0:
            damage = random.randint(
                int(self.hero.atk * 0.8), int(self.hero.atk * 1.2 + 15)
            )
            self.current_enemy.hp -= damage
            self.ids.result_label.text = f"Used Skill 1! Dmg: {damage}"
            self.update_ui()
            if not self.check_enemy_status():
                self.end_player_turn()

    def skill_2_button(self):
        if not self.is_player_turn:
            return
        if self.current_enemy and self.current_enemy.hp > 0:
            self.hero.atk_buff *= 1.3
            damage = random.randint(
                int(self.hero.atk * self.hero.atk_buff * 0.8 + 10),
                int(self.hero.atk * self.hero.atk_buff * 1.2 + 10),
            )
            self.current_enemy.hp -= damage
            self.ids.result_label.text = f"Used Skill 2! Dmg: {damage}"
            self.update_ui()
            if not self.check_enemy_status():
                self.end_player_turn()

    def skill_3_button(self):
        if not self.is_player_turn:
            return
        if self.current_enemy and self.current_enemy.hp > 0:
            damage = random.randint(
                int(self.hero.atk * 0.8 + 20), int(self.hero.atk * 1.2 + 20)
            )
            self.current_enemy.hp -= damage
            self.ids.result_label.text = f"Used Skill 3! Dmg: {damage}"
            self.update_ui()
            if not self.check_enemy_status():
                self.end_player_turn()

    def skill_4_button(self):
        if not self.is_player_turn:
            return
        heal = random.randint(int(self.hero.atk * 1.2), int(self.hero.atk * 1.5))
        self.hero.hp += heal
        if self.hero.hp > self.hero.max_hp:
            self.hero.hp = self.hero.max_hp
        self.ids.result_label.text = f"Healed {heal} HP!"
        self.update_ui()
        self.end_player_turn()

    def end_player_turn(self):
        self.is_player_turn = False
        self.ids.result_label.text += " (Enemy Turn...)"
        self.button_disabled()
        Clock.schedule_once(self.enemy_turn, 1.5)

    def enemy_turn(self, dt):
        if not self.current_enemy or self.current_enemy.hp <= 0:
            return
        enemy_damage = random.randint(
            int(self.current_enemy.atk * 0.8), int(self.current_enemy.atk * 1.2)
        )
        self.hero.hp -= enemy_damage
        self.ids.result_label.text = f"Enemy hits you for {enemy_damage}!"
        self.update_ui()
        if not self.check_hero_status():
            self.start_player_turn()

    def start_player_turn(self):
        self.is_player_turn = True
        self.ids.result_label.text = "Your Turn!"
        self.button_enabled()

    def backpack_button(self):
        if not self.is_player_turn or (
            self.current_enemy and self.current_enemy.hp <= 0
        ):
            return
        p = BackpackPopup(item_list=self.inventory, callback_func=self.use_item)
        p.open()

    def use_item(self, item_name):
        if item_name not in self.inventory or self.inventory[item_name] <= 0:
            return
        used_successfully = False

        if item_name == "Potion":
            heal_amount = 50
            self.hero.hp += heal_amount
            if self.hero.hp > self.hero.max_hp:
                self.hero.hp = self.hero.max_hp
            self.ids.result_label.text = f"Used Potion! Healed {heal_amount} HP."
            used_successfully = True

        elif item_name == "Bomb":
            if self.current_enemy and self.current_enemy.hp > 0:
                damage = 30
                self.current_enemy.hp -= damage
                self.ids.result_label.text = f"Threw Bomb! Dealt {damage} damage!"
                used_successfully = True

        if used_successfully:
            self.inventory[item_name] -= 1
            if self.inventory[item_name] == 0:
                del self.inventory[item_name]
            self.update_ui()
            if not self.check_enemy_status():
                self.end_player_turn()

    def run_button(self):
        self.manager.transition.direction = "right"
        self.manager.current = "world"
