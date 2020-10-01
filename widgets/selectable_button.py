from kivy.properties import BooleanProperty
from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from widgets.recycle_view_data_table import RecycleViewDataTable
from widgets.popups import PackingListItemUpdatePopUp
from screens.packing_list_screen import PackingListScreen

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
        if self.text == RecycleViewDataTable.no_packing_items_msg:
            return
        packing_list = PackingListScreen.current_packing_list
        packing_item = next(
            filter(lambda x: x.item_name == self.packing_item, packing_list)
        )
        popup = PackingListItemUpdatePopUp(self, title="Update Item")

        packing_list_item_inputs = popup.ids.packing_list_item_inputs

        packing_list_item_inputs.ids.item_name.text = packing_item.item_name
        packing_list_item_inputs.ids.count.text = str(packing_item.count)
        packing_list_item_inputs.ids.packed.active = packing_item.packed

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
        packing_list_item_inputs = popup.ids.packing_list_item_inputs

        packing_item.item_name = packing_list_item_inputs.ids.item_name.text
        packing_item.count = int(packing_list_item_inputs.ids.count.text)
        packing_item.packed = packing_list_item_inputs.ids.packed.active
        packing_list.write_yaml()
        self.parent.parent.parent.update_layout()

    def delete_packing_list_item(self, packing_list, packing_item):
        packing_list.remove(packing_item)
        packing_list.write_yaml()
        self.parent.parent.parent.update_layout()

    def update_changes(self, txt):
        self.text = txt