from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_file("widgets/backpack.kv")


class BackpackPopup(Popup):
    def __init__(self, item_list, callback_func, **kwargs):
        super().__init__(**kwargs)
        self.callback_func = callback_func
        grid = self.ids.item_grid_layout
        for item_name in item_list:
            btn = Factory.ItemButton(text=f"{item_name} x{item_list[item_name]}")
            btn.bind(on_release=lambda instance, x=item_name: self.on_item_click(x))
            grid.add_widget(btn)

    def on_item_click(self, item_name):
        self.callback_func(item_name)
        self.dismiss()
