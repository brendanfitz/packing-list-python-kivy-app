from packing_list import PackingList, PackingItem
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.uix.button import Button
import os

class CreatePackingListScreen(Screen):
    def create_packing_list(self, trip_name, start_date, end_date):
        try:
            packing_list = PackingList(trip_name.text, start_date.text, end_date.text)
            packing_list.write_yaml()
            print("Creating..." + str(packing_list)
                  + '...and writing to filename test_austin.yaml')

            self.manager.current = "packing_list_screen"
        except ValueError:
            self.ids.input_error.text = "Date Input must be in 'YYYY-MM-DD' form. Please try again."
    
    def update_layout(self):
        self.ids.grid.update_layout()
        self.manager.current = "select_packing_list_screen"

class SelectPackingListScreen(Screen):

    def packing_list_screen(self, btn):
        rv = self.manager.get_screen('packing_list_screen').ids.dataview
        rv.current_packing_list_filename = btn.text + '.yaml'
        rv.get_packing_list()
        self.manager.current = "packing_list_screen"

class SelectPackingListGrid(GridLayout):

    def update_layout(self):
        self.clear_widgets()
        filenames = PackingList.list_packing_lists()
        for filename in filenames:
            btn = Button(text=filename, on_press=self.parent.parent.packing_list_screen)
            self.add_widget(btn)


class DeletePackingListScreen(Screen):
    pass


class DeletePackingListGrid(GridLayout):

    def update_layout(self):
        self.clear_widgets()
        filenames = PackingList.list_packing_lists()
        for filename in filenames:
            btn = Button(text=filename, on_press=self.delete_packing_list)
            self.add_widget(btn)
    
    def delete_packing_list(self, btn):
        filename = btn.text + '.yaml'
        filepath = os.path.join(PackingList.PACKING_LIST_DIR, filename)
        os.remove(filepath)
        self.parent.parent.manager.current = 'home_screen'



class UpdatePackingListScreen(Screen):
    pass