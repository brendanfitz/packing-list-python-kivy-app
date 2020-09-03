from packing_list import PackingList, PackingItem
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

class PackingListScreen(Screen):

    def update_layout(self, filename):
        packing_list = PackingList.read_yaml(filename)

        popup = PackingListItemPopUp(title="Create Packing List Item")
        btn = self.ids.create_item_btn
        btn.on_press = popup.open
        
        popup.ids.cancel_btn.bind(on_press=popup.dismiss)
        submit_args = [btn, packing_list, filename, popup]
        popup.ids.submit_btn.bind(
            on_press=lambda btn: self.create_packing_list_item(*submit_args),
            on_release=popup.dismiss,
        )

    def create_packing_list_item(self, btn, packing_list, filename, popup):
        item_name = popup.ids.item_name.text
        count = popup.ids.count.text
        packed = PackingItem.process_packed_status(popup.ids.packed.text)
        packing_list.append(PackingItem(item_name, count, packed))
        packing_list.write_yaml()
        self.ids.dataview.update_layout(filename)
    
    def update_packing_list_item(self):
        pass

    def delete_packing_list_item(self):
        pass

    
class PackingListItemPopUp(Popup):
    pass

