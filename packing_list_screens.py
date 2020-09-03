from packing_list import PackingList, PackingItem
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput 
import os

class CreatePackingListScreen(Screen):
    def create_packing_list(self, trip_name, start_date, end_date):
        try:
            packing_list = PackingList(trip_name.text, start_date.text, end_date.text)
            packing_list.write_yaml()
            self.manager.current = "packing_list_screen"
        except ValueError:
            self.ids.input_error.text = "Date Input must be in 'YYYY-MM-DD' form. Please try again."

class SelectPackingListScreen(Screen):

    def update_layout(self):
        grid = self.ids.grid
        grid.clear_widgets()
        filenames = PackingList.list_packing_lists()
        for filename in filenames:
            btn = Button(text=filename, on_press=self.packing_list_screen)
            grid.add_widget(btn)

    def packing_list_screen(self, btn):
        screen = self.manager.get_screen('packing_list_screen')
        filename = btn.text
        screen.ids.dataview.update_layout(filename)
        screen.update_layout(filename)
        self.manager.current = "packing_list_screen"


class DeletePackingListScreen(Screen):

    def update_layout(self):
        grid = self.ids.grid
        grid.clear_widgets()
        filenames = PackingList.list_packing_lists()
        for filename in filenames:
            btn = Button(text=filename, on_press=self.delete_packing_list)
            grid.add_widget(btn)
    
    def delete_packing_list(self, btn):
        filename = btn.text + '.yaml'
        filepath = os.path.join(PackingList.PACKING_LIST_DIR, filename)
        os.remove(filepath)
        self.manager.current = 'home_screen'


class UpdatePackingListScreen(Screen):
    def update_layout(self):
        grid = self.ids.grid
        grid.clear_widgets()
        filenames = PackingList.list_packing_lists()
        for filename in filenames:
            popup = self.create_popup(filename)
            btn = Button(text=filename, on_press=popup.open)
            grid.add_widget(btn)
    
    def create_popup(self, filename):
        packing_list = PackingList.read_yaml(filename)

        popup = PackingListPopup(auto_dismiss=False)

        popup.ids.trip_name.text = packing_list.trip_name
        popup.ids.start_date.text = packing_list.start_date_tostring()
        popup.ids.end_date.text = packing_list.end_date_tostring()

        popup.ids.submit_btn.bind(
            on_press=lambda btn: self.update_packing_list(
                btn, packing_list, popup, filename
            ),
            on_release=popup.dismiss,
        )
        popup.ids.cancel_btn.bind(on_press=popup.dismiss)

        return popup
    
    def update_packing_list(self, btn, packing_list, popup, old_filename):
        # finish update behavior
        packing_list.trip_name = popup.ids.trip_name.text
        packing_list.start_date = PackingList.check_date(popup.ids.start_date.text)
        packing_list.end_date = PackingList.check_date(popup.ids.end_date.text)
        packing_list.write_yaml()

        # remove old filename
        old_filepath = os.path.join(
            PackingList.PACKING_LIST_DIR,
            old_filename
        )
        os.remove(old_filepath + '.yaml')

        self.update_layout()

class PackingListPopup(Popup):
    pass
    
    