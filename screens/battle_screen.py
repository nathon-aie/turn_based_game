from kivy.uix.screenmanager import Screen
from widgets.backpack import BackpackPopup
from kivy.lang import Builder
from kivy.clock import Clock
from objects.hero import Hero
from objects.enemy import Enemy
import random
import gamedata

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
        self.hero = Hero("Tanker")
        self.update_skill_buttons()

    def spawn_enemy(self):
        enemy_list = list(gamedata.ENEMIES.keys())
        enemy_name = random.choice(enemy_list)
        self.current_enemy = Enemy(enemy_name)

    def update_skill_buttons(self):
        buttons = [
            self.ids.skill_1,
            self.ids.skill_2,
            self.ids.skill_3,
            self.ids.skill_4,
        ]
        for i, btn in enumerate(buttons):
            if i < len(self.hero.skills):
                skill_name = self.hero.skills[i]
                btn.text = skill_name
                btn.disabled = False
                btn.unbind(on_release=self.on_skill_press)
            else:
                btn.text = "-"
                btn.disabled = True

    def on_skill_press(self, button_instance):
        if not self.is_player_turn:
            return
        skill_name = button_instance.text
        self.execute_skill(self.hero, self.current_enemy, skill_name)

    def execute_skill(self, attacker, defender, skill_name):
        if skill_name not in gamedata.SKILLS:
            return
        skill_info = gamedata.SKILLS[skill_name]
        multiplier = skill_info["value"]
        final_value = int(attacker.atk * attacker.atk_buff + multiplier)
        if skill_info["type"] == "attack":
            if defender and defender.hp > 0:
                defender.hp -= final_value
                self.ids.result_label.text = f"Used {skill_name}! {final_value} Dmg."
        elif skill_info["type"] == "heal":
            attacker.hp += final_value
            if attacker.hp > attacker.max_hp:
                attacker.hp = attacker.max_hp
            self.ids.result_label.text = f"Used {skill_name}! Healed {final_value}."
        self.update_ui()
        if not self.check_enemy_status():
            self.end_player_turn()

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
