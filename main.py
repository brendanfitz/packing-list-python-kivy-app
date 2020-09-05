from packing_list import PackingList, PackingItem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from datepicker import DatePicker
from packing_list_screens import SelectPackingListScreen
from packing_list_item_screens import PackingListScreen
from packing_list_table_widgets import RV

Builder.load_file('design.kv')

class HomeScreen(Screen):
    def create_packing_list(self, trip_name, start_date, end_date):
        try:
            packing_list = PackingList(trip_name.text, start_date.text, end_date.text)
            packing_list.write_yaml()
            filename = packing_list.create_filename()
            PackingListScreen.current_filename = filename
            PackingListScreen.current_packing_list = PackingList.read_yaml(filename)

            screen = self.manager.get_screen('packing_list_screen')
            screen.ids.dataview.update_layout(filename)
            screen.update_layout(filename)
            self.manager.current = "packing_list_screen"
        except ValueError:
            self.ids.input_error.text = "Date Input must be in 'YYYY-MM-DD' form. Please try again."
    
    def select_packing_list_screen(self):
        screen_name ='select_packing_list_screen'
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