from packing_list import PackingList, PackingItem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('design.kv')

class HomeScreen(Screen):
    def create_packing_list_screen(self):
        self.manager.current = "create_packing_list_screen"
    
    def packing_list_screen(self):
        self.manager.current = "packing_list_screen"

class CreatePackingListScreen(Screen):
    def create_packing_list(self, trip_name, start_date, end_date):
        print(trip_name.text, start_date.text, end_date.text)
        packing_list = PackingList(trip_name.text, start_date.text, end_date.text)

class PackingListScreen(Screen):
    pass

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()