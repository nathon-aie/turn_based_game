from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

Builder.load_file("screens/title_screen.kv")


class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bgm = SoundLoader.load("audio/bgm.mp3")
        self.bgm.loop = True  # ให้เพลงเล่นตลอดเวลา
        self.music_enabled = True  # เริ่มต้นให้เพลงเปิดอยู่

    # เมื่อเข้าสู่หน้าจอ TitleScreen ให้เริ่มเล่นเพลง
    def on_enter(self):
        self.bgm.play()

    # เมื่อออกจากหน้าจอ TitleScreen ให้หยุดเล่นเพลง
    def on_leave(self):
        self.bgm.stop()

    # ปุ่มเปิด/ปิดเพลง
    def toggle_music(self):
        if self.music_enabled:
            self.bgm.stop()
            self.music_enabled = False
        else:
            self.bgm.play()
            self.music_enabled = True
        self.ids.music_btn.text = f"Music: {'ON' if self.music_enabled else 'OFF'}"

    # ปุ่มเล่น
    def play_button(self):
        self.manager.transition.direction = "left"
        self.manager.current = "world"
