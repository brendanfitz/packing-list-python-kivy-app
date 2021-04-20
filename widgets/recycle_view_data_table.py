from packing_list import PackingList
from kivy.properties import ListProperty 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.popup import Popup
from screens.packing_list_screen import PackingListScreen

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class RecycleViewDataTable(BoxLayout):
    data_items = ListProperty([])
    no_packing_items_msg = 'No items have been added yet. Create below'

    def __init__(self, **kwargs):
        super(RecycleViewDataTable, self).__init__(**kwargs)

    def update_layout(self):
        packing_list = PackingListScreen.current_packing_list
        filename = packing_list.filename

        self.data_items.clear()

        if packing_list is None:
            self.data_items.append(('', '', RecycleViewDataTable.no_packing_items_msg))
        else:
            for item in packing_list:
                self.data_items.append((filename, item.item_name, item.item_name))
                self.data_items.append((filename, item.item_name, item.count))
                self.data_items.append((filename, item.item_name, item.packed_yesno())) 