from packing_list import PackingList, PackingItem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from packing_list_screens import (
    CreatePackingListScreen, SelectPackingListScreen,
)
from packing_list_item_screens import PackingListScreen
from packing_list_table_widgets import RV

Builder.load_file('design.kv')

class HomeScreen(Screen):
    def create_packing_list_screen(self):
        self.manager.current = "create_packing_list_screen"
    
    def select_packing_list_screen(self):
        screen_name ='select_packing_list_screen'
        self.manager.get_screen(screen_name).update_layout()
        self.manager.current = screen_name

    def update_packing_list_screen(self):
        screen_name ='update_packing_list_screen'
        self.manager.get_screen(screen_name).update_layout()
        self.manager.current = screen_name

    def delete_packing_list_screen(self):
        screen_name ='delete_packing_list_screen'
        self.manager.get_screen(screen_name).update_layout()
        self.manager.current = screen_name


class RootWidget(ScreenManager):
    pass

class TopBar(GridLayout):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()