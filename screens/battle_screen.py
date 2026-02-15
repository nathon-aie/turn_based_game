from kivy.uix.screenmanager import Screen
from widgets.backpack import BackpackPopup
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
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
        self.spawn_hero()  # สร้าง hero เมื่อเริ่มต้นหน้าต่อสู้
        self.inventory = {
            "Potion": 10,
            "Bomb": 10,
            "Super Potion": 5,
        }  # บอกจำนวนไอเทมในกระเป๋า
        self.bgm = SoundLoader.load("audio/helios_rap.mp3")

    # ปิดการทำงานของปุ่มทั้งหมด
    def button_disabled(self, *args):
        self.ids.skill_1.disabled = True
        self.ids.skill_2.disabled = True
        self.ids.skill_3.disabled = True
        self.ids.skill_4.disabled = True
        self.ids.backpack.disabled = True
        self.ids.run.disabled = True

    # เปิดการทำงานของปุ่มทั้งหมด
    def button_enabled(self, *args):
        self.ids.skill_1.disabled = False
        self.ids.skill_2.disabled = False
        self.ids.skill_3.disabled = False
        self.ids.skill_4.disabled = False
        self.ids.backpack.disabled = False
        self.ids.run.disabled = False

    # เมื่อเข้าหน้าต่อสู้
    def on_enter(self):
        self.spawn_enemy()  # สุ่มศัตรูใหม่ทุกครั้งที่เข้าหน้าต่อสู้
        self.update_ui()  # อัพเดท UI แสดงข้อมูลของศัตรู
        Clock.schedule_once(self.enable_skills, 1)  # หน่วงเวลา 1 วินาทีก่อนเปิดปุ่ม
        self.button_disabled()  # ปิดปุ่ม
        self.ids.result_label.text = (
            f"{self.current_enemy.name} appears!"  # อัพเดทข้อความแสดงผลเป็นชื่อศัตรูที่ปรากฏ
        )
        # เริ่มเล่น BGM
        if self.bgm:
            self.bgm.loop = True
            self.bgm.play()

    # เมื่อออกจากหน้าต่อสู้ จะปิด BGM
    def on_leave(self):
        if self.bgm:
            self.bgm.stop()

    # เปิดใช้งานปุ่มหลังจากหน่วงเวลา
    def enable_skills(self, dt):
        self.button_enabled()
        self.ids.result_label.text = "Fight!"  # อัพเดทข้อความแสดงผลเป็น Fight
        self.ids.run.text = "Run"  # เปลี่ยนข้อความปุ่ม run กลับเป็น Run
        self.start_player_turn()  # เริ่มต้นเทิร์นผู้เล่น

    # สร้าง Hero
    def spawn_hero(self):
        self.hero = Hero("Mambo")  # สร้าง Hero จาก gamedata.py
        self.update_skill_buttons()  # อัพเดทปุ่มสกิลตามสกิลที่ Hero มีจาก gamedata.py

    # สุ่มศัตรูใหม่
    def spawn_enemy(self):
        enemy_list = list(gamedata.ENEMIES.keys())  # ดึงรายชื่อศัตรูจาก gamedata.py
        enemy_name = random.choice(enemy_list)  # สุ่มชื่อศัตรู
        self.current_enemy = Enemy(enemy_name)  # สร้างศัตรูใหม่จากที่สุ่ม
        # ใส่รูปศัตรู
        enemy_image_map = {
            "Anuthin": "pics/character/auntin.png",
            "Anuthin Slayer": "pics/character/ptae.jpg",
            "Noob Slayer": "pics/character/noob.jpg",
            "Goblin Slayer": "pics/character/spiki.jpg",
            "God Slayer": "pics/character/cj.jpg",
            "P'tae": "pics/character/tae007.jpg",
        }
        self.ids.enemy_character.source = enemy_image_map.get(enemy_name, "")
        self.ids.enemy_character.reload()

    # อัพเดทปุ่มสกิล
    def update_skill_buttons(self):
        buttons = [
            self.ids.skill_1,
            self.ids.skill_2,
            self.ids.skill_3,
            self.ids.skill_4,
        ]
        # loop ใส่สกิลที่ Hero มีลงในปุ่ม ถ้าไม่มีสกิลใส่ "-" และปิดการใช้งานปุ่มน
        for i, button in enumerate(buttons):
            if i < len(self.hero.skills):
                skill_name = self.hero.skills[i]  # ดึงชื่อสกิลจาก Hero
                button.text = skill_name  # ใส่ชื่อสกิล
                button.disabled = False  # เปิดการใช้งานปุ่ม
            else:
                button.text = "-"
                button.disabled = True

    # เมื่อกดปุ่มสกิล
    def on_skill_press(self, button_instance):
        if not self.is_player_turn:
            return
        skill_name = button_instance.text
        self.execute_skill(self.hero, self.current_enemy, skill_name)

    # คำนวณผลของสกิล
    def execute_skill(self, hero, enemy, skill_name):
        skill_info = gamedata.SKILLS[skill_name]
        multiplier = skill_info["value"]
        # ค่าสุดท้ายจากการคำนวณ
        final_value = int(hero.atk * hero.atk_buff + multiplier)
        # สกิลประเภท attack
        if skill_info["type"] == "attack":
            enemy.hp -= final_value
            self.ids.result_label.text = f"Used {skill_name}! {final_value} Dmg."
        # สกิลประเภท heal
        elif skill_info["type"] == "heal":
            hero.hp += final_value
            # ถ้า heal เกิน ให้ค่าเท่ากับ max_hp
            if hero.hp > hero.max_hp:
                hero.hp = hero.max_hp
            self.ids.result_label.text = f"Used {skill_name}! Healed {final_value}."
        self.update_ui()
        # ตรวจสอบสถานะของศัตรูหลังใช้สกิล ถ้าศัตรูยังไม่ตายให้จบเทิร์นผู้เล่น
        if not self.check_enemy_status():
            self.end_player_turn()

    # เข้าเทิร์นของ Enemy
    def enemy_turn(self, dt):
        # คำนวณดาเมจของศัตรู
        enemy_damage = random.randint(
            int(self.current_enemy.atk * 0.8), int(self.current_enemy.atk * 1.2)
        )
        self.hero.hp -= enemy_damage
        self.update_ui()
        if not self.check_hero_status():
            self.start_player_turn()

    # อัพเดท UI ให้เลือดไม่ต่ำกว่า 0
    def update_ui(self):
        if self.current_enemy:
            if self.current_enemy.hp < 0:
                self.current_enemy.hp = 0
            self.ids.enemy_stat_label.text = (
                f"{self.current_enemy.name}\nHP: {self.current_enemy.hp}"
            )
        if self.hero:
            if self.hero.hp < 0:
                self.hero.hp = 0
            self.ids.hero_stat_label.text = f"{self.hero.name}\nHP: {self.hero.hp}"

    # ตรวจสอบสถานะของศัตรู
    def check_enemy_status(self):
        # เลือดเต่ำกว่า 0
        if self.current_enemy.hp <= 0:
            self.ids.result_label.text = (
                f"Victory! {self.current_enemy.name} defeated."  # อัพเดทข้อความแสดงผล
            )
            self.current_enemy = None  # เคลียร์ศัตรูที่ตายแล้วออกจากหน้าต่อสู้
            self.ids.run.text = "Exit"  # เปลี่ยนข้อความปุ่ม run เป็น Exit
            self.button_disabled()  # ปิดปุ่ม
            self.ids.run.disabled = False  # เปิดปุ่ม run เพื่อให้ออกจากหน้าต่อสู้ได้
            return True
        # เลือดยังไม่ต่ำกว่า 0
        return False

    # ตรวจสอบสถานะของ Hero
    def check_hero_status(self):
        # เลือดเต่ำกว่า 0
        if self.hero.hp <= 0:
            self.ids.result_label.text = "Game Over"  # อัพเดทข้อความแสดงผล
            self.button_disabled()  # ปิดปุ่ม
            self.ids.run.text = "Exit"  # เปลี่ยนข้อความปุ่ม run เป็น Exit
            self.ids.run.disabled = False  # เปิดปุ่ม run เพื่อให้ออกจากหน้าต่อสู้ได้
            return True
        return False

    # จบเทิร์นของ Hero
    def end_player_turn(self):
        self.is_player_turn = False
        self.button_disabled()  # ปิดปุ่ม
        Clock.schedule_once(self.enemy_turn, 1.5)  # หน่วงเวลา 1.5 วิก่อนเข้าเทิร์นศัตรู

    # เริ่มเทิร์นของ Hero
    def start_player_turn(self):
        self.is_player_turn = True
        self.ids.result_label.text = "Your Turn!"
        self.button_enabled()

    # ปุ่มใช้ไอเทม
    def backpack_button(self):
        # เปิด Popup แสดงไอเทมในกระเป๋า และส่งฟังก์ชัน callback สำหรับใช้ไอเทม
        p = BackpackPopup(item_list=self.inventory, callback_func=self.use_item)
        p.open()  # เปิด Popup

    def use_item(self, item_name):
        # ดึงข้อมูลไอเทมจาก gamedata.py ตามชื่อไอเทมที่เลือก
        item_data = gamedata.ITEMS.get(item_name)
        item_type = item_data["type"]
        value = item_data["value"]
        used_successfully = False  # ตรวจว่าใช้ไอเทมมั้ย
        # ไอเทมประเภท Heal
        if item_type == "heal":
            self.hero.hp += value
            if self.hero.hp > self.hero.max_hp:
                self.hero.hp = self.hero.max_hp
            self.ids.result_label.text = f"Used {item_name}! Healed {value} HP."
            used_successfully = True
        # ไอเทมประเภท Attack
        elif item_type == "attack":
            self.current_enemy.hp -= value
            self.ids.result_label.text = f"Used {item_name}! Dealt {value} damage!"
            used_successfully = True
        # ถ้าใช้ไอเทม
        if used_successfully:
            # ลดจำนวนทีละ 1
            self.inventory[item_name] -= 1
            # ถ้าไอเทมหมด ให้ลบออกจากกระเป๋า
            if self.inventory[item_name] == 0:
                del self.inventory[item_name]
            self.update_ui()
            if not self.check_enemy_status():
                self.end_player_turn()

    # ปุ่มหนี
    def run_button(self):
        self.manager.transition.direction = "right"
        self.manager.current = "world"
