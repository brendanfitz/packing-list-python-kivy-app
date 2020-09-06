from packing_list import PackingList, PackingItem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from utils.datepicker import DatePicker
from screens.home_screen import HomeScreen 
from screens.load_packing_list_screen import LoadPackingListScreen
from screens.packing_list_screen import PackingListScreen
from screens.packing_list_table_widgets import RV

Builder.load_file('design.kv')

class RootWidget(ScreenManager):
    pass


class TopBar(GridLayout):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()