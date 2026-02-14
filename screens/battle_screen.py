from kivy.uix.screenmanager import Screen
from widgets.backpack import BackpackPopup
from kivy.lang import Builder
from kivy.clock import Clock
from character.hero import Hero
from character.enemy import Enemy
import random

Builder.load_file("screens/battle_screen.kv")


class BattleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_enemy = None
        self.is_player_turn = True
        self.inventory = {"Potion": 10, "Bomb": 10}

    def on_enter(self):
        self.spawn_hero()
        self.spawn_enemy()
        self.update_ui()
        Clock.schedule_once(self.enable_skills, 1.5)
        self.ids.skill_1.disabled = True
        self.ids.skill_2.disabled = True
        self.ids.skill_3.disabled = True
        self.ids.skill_4.disabled = True
        self.ids.backpack.disabled = True
        self.ids.run.disabled = True
        self.ids.result_label.text = f"{self.current_enemy.name} appears!"

    def enable_skills(self, dt):
        self.ids.skill_1.disabled = False
        self.ids.skill_2.disabled = False
        self.ids.skill_3.disabled = False
        self.ids.skill_4.disabled = False
        self.ids.backpack.disabled = False
        self.ids.run.disabled = False
        self.ids.result_label.text = "Fight!"
        self.ids.run.text = "Run"
        self.start_player_turn()

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
            if self.current_enemy.hp < 0:
                self.current_enemy.hp = 0
            display_text = f"{self.current_enemy.name}\nHP: {self.current_enemy.hp}"
            self.ids.enemy_stat_label.text = display_text
        if self.hero:
            if self.hero.hp < 0:
                self.hero.hp = 0
            display_text = f"{self.hero.name}\nHP: {self.hero.hp}"
            self.ids.hero_stat_label.text = display_text

    def check_enemy_status(self):
        if self.current_enemy.hp <= 0:
            self.current_enemy.hp = 0
            self.ids.result_label.text = f"Victory! {self.current_enemy.name} defeated."
            self.ids.run.text = "Exit"
            self.ids.skill_1.disabled = True
            self.ids.skill_2.disabled = True
            self.ids.skill_3.disabled = True
            self.ids.skill_4.disabled = True
            self.ids.backpack.disabled = True
            return True
        return False

    def skill_1_button(self):
        if not self.is_player_turn:
            return
        if self.current_enemy and self.current_enemy.hp > 0:
            damage = 15
            self.current_enemy.hp -= damage
            self.ids.result_label.text = f"Used Skill 1! Dmg: {damage}"
            self.update_ui()
            is_dead = self.check_enemy_status()
            if is_dead:
                pass
            else:
                self.end_player_turn()

    def skill_2_button(self):
        if not self.is_player_turn:
            return
        if self.current_enemy and self.current_enemy.hp > 0:
            damage = 10
            self.current_enemy.hp -= damage
            self.ids.result_label.text = f"Used Skill 1! Dmg: {damage}"
            self.update_ui()
            is_dead = self.check_enemy_status()

            if is_dead:
                pass
            else:
                self.end_player_turn()

    def skill_3_button(self):
        if not self.is_player_turn:
            return
        if self.current_enemy and self.current_enemy.hp > 0:
            damage = 20
            self.current_enemy.hp -= damage
            self.ids.result_label.text = f"Used Skill 1! Dmg: {damage}"
            self.update_ui()
            is_dead = self.check_enemy_status()

            if is_dead:
                pass
            else:
                self.end_player_turn()

    def skill_4_button(self):
        if not self.is_player_turn:
            return
        heal = 20
        self.hero.hp += heal
        if self.hero.hp > self.hero.max_hp:
            self.hero.hp = self.hero.max_hp
        self.ids.result_label.text = f"Healed {heal} HP!"
        self.update_ui()
        self.end_player_turn()

    def end_player_turn(self):
        self.is_player_turn = False
        self.ids.result_label.text += " (Enemy Turn...)"
        self.ids.skill_1.disabled = True
        self.ids.skill_2.disabled = True
        self.ids.skill_3.disabled = True
        self.ids.skill_4.disabled = True
        Clock.schedule_once(self.enemy_turn_logic, 1.5)

    def enemy_turn_logic(self, dt):
        if not self.current_enemy or self.current_enemy.hp <= 0:
            return
        enemy_damage = random.randint(5, 15)
        self.hero.hp -= enemy_damage
        self.ids.result_label.text = f"Enemy hits you for {enemy_damage}!"
        self.update_ui()
        if self.hero.hp <= 0:
            self.hero.hp = 0
            self.ids.result_label.text = "Game Over... You died."
            self.manager.transition.direction = "right"
            self.manager.current = "world"
        else:
            self.start_player_turn()

    def start_player_turn(self):
        self.is_player_turn = True
        self.ids.result_label.text = "Your Turn!"
        self.ids.skill_1.disabled = False
        self.ids.skill_2.disabled = False
        self.ids.skill_3.disabled = False
        self.ids.skill_4.disabled = False
        self.ids.backpack.disabled = False

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
