from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.lang import Builder
import gamedata

Builder.load_file("widgets/backpack.kv")


class BackpackPopup(Popup):
    def __init__(self, item_list, callback_func, **kwargs):
        super().__init__(**kwargs)
        self.item_list = item_list
        self.callback_func = callback_func
        self.selected_item = None
        # สร้างปุ่มสำหรับแต่ละไอเทมในรายการ
        grid = self.ids.item_grid_layout
        for item_name, count in item_list.items():
            btn = Factory.Button(
                text=f"{item_name} x{count}", size_hint_y=None, height=50
            )
            btn.bind(on_release=lambda instance, x=item_name: self.show_details(x))
            grid.add_widget(btn)
        if self.callback_func is None:
            self.ids.use_button.disabled = True

    # แสดงรายละเอียดของไอเทม
    def show_details(self, item_name):
        self.selected_item = item_name
        item_data = gamedata.ITEMS.get(item_name)
        desc = item_data.get("description")
        self.ids.description_label.text = f"[b]{item_name}[/b]\n\n{desc}"
        self.ids.description_label.markup = True

    # ยืนยันการใช้ไอเทม
    def confirm_use(self):
        if self.selected_item:
            self.callback_func(self.selected_item)
            self.dismiss()
