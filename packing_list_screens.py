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
        packing_list = PackingList.read_yaml(filename + '.yaml')

        content = GridLayout(cols=1)
        popup = Popup(content=content, auto_dismiss=False)

        packing_list_layout = self.create_packing_list_layout(packing_list)
        content.add_widget(packing_list_layout)

        button_layout = GridLayout(cols=2)
        content.add_widget(button_layout)

        submit = Button(text='Submit')
        button_layout.add_widget(submit)

        cancel = Button(text='Cancel')
        button_layout.add_widget(cancel)

        submit.bind(
            on_press=lambda btn: self.submit_button_press(
                btn, packing_list, filename
            ),
            on_release=popup.dismiss,
        )
        cancel.bind(on_press=popup.dismiss)

        return popup
    
    def submit_button_press(self, btn, packing_list, old_filename):
        packing_list_layout = btn.parent.parent.children[1]
        end_date, start_date, trip_name = packing_list_layout.children

        # finish update behavior
        packing_list.trip_name = trip_name.text
        packing_list.start_date = PackingList.check_date(start_date.text)
        packing_list.end_date = PackingList.check_date(end_date.text)
        packing_list.write_yaml()

        # remove old filename
        old_filepath = os.path.join(
            PackingList.PACKING_LIST_DIR,
            old_filename + '.yaml'
        )
        os.remove(old_filepath)

        self.update_layout()

    def create_packing_list_layout(self, packing_list):
        packing_list_layout = GridLayout(id="packing_list_layout", cols=3)
        text_input = TextInput(
            id="trip_name",
            text=packing_list.trip_name,
            write_tab=False,
            hint_text="Trip Name"
        )
        packing_list_layout.add_widget(text_input)

        text_input = TextInput(
            id="start_date",
            text=str(packing_list.start_date),
            write_tab=False,
            hint_text="Start Date"
        )
        packing_list_layout.add_widget(text_input)

        text_input = TextInput(
            id="end_date",
            text=str(packing_list.end_date),
            write_tab=False,
            hint_text="End Date"
        )
        packing_list_layout.add_widget(text_input)
        
        return packing_list_layout

    
    