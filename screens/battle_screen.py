from kivy.uix.screenmanager import Screen
from widgets.backpack import BackpackPopup
from kivy.lang import Builder

Builder.load_file("screens/battle_screen.kv")


class BattleScreen(Screen):
    def skill_1_button(self):
        pass

    def skill_2_button(self):
        pass

    def skill_3_button(self):
        pass

    def skill_4_button(self):
        pass

    def backpack_button(self):
        items = {"Item 1": 10, "Item 2": 20, "Item 3": 30}
        p = BackpackPopup(item_list=items, callback_func=self.update_selection)
        p.open()

    def update_selection(self, selected_item):
        self.ids.result_label.text = f"Select: {selected_item}"

    def run_button(self):
        self.manager.transition.direction = "right"
        self.manager.current = "title"
