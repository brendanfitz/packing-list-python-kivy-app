from packing_list import PackingList
from kivy.properties import BooleanProperty, ListProperty 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.popup import Popup
from widgets.popups import PackingListItemUpdatePopUp

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class RecycleViewDataTable(BoxLayout):
    data_items = ListProperty([])
    no_packing_items_msg = 'No items have been added yet. Create below'

    def __init__(self, **kwargs):
        super(RecycleViewDataTable, self).__init__(**kwargs)

    def update_layout(self, filename=None, packing_list=None):
        if filename is not None:
            packing_list = PackingList.read_yaml(filename)
        else:
            filename = packing_list.create_filename()[:-5]

        self.data_items.clear()

        if not packing_list:
            self.data_items.append(('', '', RecycleViewDataTable.no_packing_items_msg))
        else:
            for item in packing_list:
                self.data_items.append((filename, item.item_name, item.item_name))
                self.data_items.append((filename, item.item_name, item.count))
                self.data_items.append((filename, item.item_name, item.get_packed_status())) 

class ItemDataButton(Button):
    pass

class SelectableButton(RecycleDataViewBehavior, ItemDataButton):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        packing_list = PackingList.read_yaml(self.filename)
        packing_item = next(
            filter(lambda x: x.item_name == self.packing_item, packing_list)
        )
        popup = PackingListItemUpdatePopUp(self, title="Update Item")
        popup.ids.item_name.text = packing_item.item_name
        popup.ids.count.text = str(packing_item.count)
        popup.ids.packed.text = packing_item.get_packed_status()

        update_args = [
            packing_list,
            packing_item,
            popup
        ]
        popup.ids.popup_submit_btn.bind(
            on_press=lambda btn: self.update_packing_list_item(*update_args),
            on_release=popup.dismiss,
        )
        popup.ids.popup_delete_btn.bind(
            on_press=lambda btn: self.delete_packing_list_item(packing_list, packing_item),
            on_release=popup.dismiss,
        )
        popup.ids.popup_cancel_btn.bind(on_press=popup.dismiss)

        popup.open()
    
    def update_packing_list_item(self, packing_list, packing_item, popup):
        packing_item.item_name = popup.ids.item_name.text
        packing_item.count = int(popup.ids.count.text)
        packing_item.set_packed_status(popup.ids.packed.text)
        packing_list.write_yaml()
        self.parent.parent.parent.update_layout(packing_list=packing_list)

    def delete_packing_list_item(self, packing_list, packing_item):
        packing_list.remove(packing_item)
        packing_list.write_yaml()
        self.parent.parent.parent.update_layout(packing_list=packing_list)

    
    def update_changes(self, txt):
        self.text = txt
