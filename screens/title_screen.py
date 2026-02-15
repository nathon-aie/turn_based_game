from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

Builder.load_file("screens/title_screen.kv")


class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bgm = SoundLoader.load("audio/bgm.mp3")
        if self.bgm:
            self.bgm.loop = True
        self.music_enabled = True

    def on_enter(self):
        if self.bgm and self.music_enabled:
            self.bgm.play()

    def on_leave(self):
        if self.bgm:
            self.bgm.stop()

    def toggle_music(self):
        if self.bgm:
            if self.music_enabled:
                self.bgm.stop()
                self.music_enabled = False
            else:
                self.bgm.play()
                self.music_enabled = True
        self.ids.music_btn.text = f"Music: {'ON' if self.music_enabled else 'OFF'}"

    def play_button(self):
        self.manager.transition.direction = "left"
        self.manager.current = "world"
