from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file("widgets/stats.kv")


class StatusPopup(Popup):
    stats_text = StringProperty("")

    def __init__(self, character, **kwargs):
        super().__init__(**kwargs)
        self.stats_text = (
            f"[b]Name:[/b] {character.name}\n"
            f"[b]HP:[/b] {character.hp}\n"
            f"[b]ATK:[/b] {character.atk}\n"
        )
