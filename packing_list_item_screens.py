from packing_list import PackingList, PackingItem
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

class PackingListScreen(Screen):

    def update_layout(self, filename):
        packing_list = PackingList.read_yaml(filename + '.yaml')

        popup = PackingListItemPopUp(title="Create Packing List Item")
        btn = self.ids.create_item_btn
        btn.on_press = popup.open
        
        popup.ids.cancel_btn.bind(on_press=popup.dismiss)
        popup.ids.submit_btn.bind(
            on_press=lambda btn: self.create_packing_list_item(
                btn, packing_list, filename
            ),
            on_release=popup.dismiss,
        )

    def create_packing_list_item(self, btn, packing_list, filename):
        layout = btn.parent.parent.children[1]
        item_name = layout.children[2].text
        count = layout.children[1].text
        packed = PackingItem.process_packed_status(layout.children[0].text)
        packing_list.append(PackingItem(item_name, count, packed))
        packing_list.write_yaml()
        self.ids.dataview.update_layout(filename)
    
    def update_packing_list_item(self):
        pass

    def delete_packing_list_item(self):
        pass

    
class PackingListItemPopUp(Popup):
    pass

