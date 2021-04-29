from os import path, remove
from packing import PackingList, PackingItem, PackingDateValueError
from kivy.uix.screenmanager import Screen
from packing.widgets.popups import PackingListItemPopUp, UpdatePackingListPopup

class PackingListScreen(Screen):
    current_filename = None
    current_packing_list = None

    def update_layout(self):
        packing_list = PackingListScreen.current_packing_list

        self.ids.dataview.update_layout()

        filename = packing_list.filename

        popup = PackingListItemPopUp(title="Create Packing List Item")
        btn = self.ids.create_item_btn
        btn.on_press = popup.open
        
        popup.ids.cancel_btn.bind(on_press=popup.dismiss)
        submit_args = [btn, packing_list, filename, popup]
        popup.ids.submit_btn.bind(
            on_press=lambda btn: self.create_packing_list_item(*submit_args),
            on_release=popup.dismiss,
        )

        popup = self.create_update_packing_list_popup()
        btn = self.ids.update_packing_list_btn
        btn.on_press = popup.open

    def create_packing_list_item(self, btn, packing_list, filename, popup):
        packing_list_item_inputs = popup.ids.packing_list_item_inputs

        item_name = packing_list_item_inputs.ids.item_name.text
        count = packing_list_item_inputs.ids.count.text
        packed = packing_list_item_inputs.ids.packed.active

        try:
            packing_list.append(PackingItem(item_name, count, packed))
        except ValueError:
            # TODO: add popup here
            pass
        else:
            packing_list.toJSON()
            self.update_layout()
    
    def update_packing_list(self, btn, popup):
        packing_list = PackingListScreen.current_packing_list
        former_filename = packing_list.filename

        # update packing list from TextInputs
        form_data = popup.ids.packing_list_inputs
        packing_list.trip_name = form_data.ids.trip_name.text
        packing_list.start_date = form_data.ids.start_date.text
        try:
            packing_list.end_date = form_data.ids.end_date.text
        except PackingDateValueError:
            popup.ids.input_error.text = "Trip End Date is before the Start Date. Please try again."
            return

        packing_list.toJSON()

        # remove old json file if user changed data
        if former_filename != packing_list.filename:
            filepath = path.join(PackingList.PACKING_LIST_DIR, former_filename)
            remove(filepath)

        self.update_layout()
        popup.dismiss()
    
    def create_update_packing_list_popup(self):
        packing_list = PackingListScreen.current_packing_list

        popup = UpdatePackingListPopup(title="Update Packing List", auto_dismiss=False)

        packing_list_inputs = popup.ids.packing_list_inputs
        packing_list_inputs.ids.trip_name.text = packing_list.trip_name
        packing_list_inputs.ids.start_date.text = packing_list.start_date.packing_strftime()
        packing_list_inputs.ids.end_date.text = packing_list.end_date.packing_strftime()

        popup.ids.submit_btn.bind(
            on_press=lambda btn: self.update_packing_list(btn, popup),
        )
        popup.ids.cancel_btn.bind(on_press=popup.dismiss)

        return popup

    def delete_packing_list(self):
        packing_list = PackingListScreen.current_packing_list

        filename = packing_list.filename
        filepath = path.join(PackingList.PACKING_LIST_DIR, filename)
        remove(filepath)

        self.manager.current = 'home_screen'
