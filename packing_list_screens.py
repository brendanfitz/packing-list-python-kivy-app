from packing_list import PackingList, PackingItem
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput 
from packing_list_item_screens import PackingListScreen
import os

class CreatePackingListScreen(Screen):
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
        filename = btn.text + '.yaml'
        PackingListScreen.current_filename = filename
        PackingListScreen.current_packing_list = PackingList.read_yaml(filename)
        screen.ids.dataview.update_layout(filename)
        screen.update_layout(filename)
        self.manager.current = "packing_list_screen"