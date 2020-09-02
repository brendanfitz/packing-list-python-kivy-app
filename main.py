from packing_list import PackingList, PackingItem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from packing_list_table_widgets import TextInputPopup, SelectableRecycleGridLayout, RV, SelectableButton

Builder.load_file('design.kv')

class HomeScreen(Screen):
    def create_packing_list_screen(self):
        self.manager.current = "create_packing_list_screen"
    
    def select_packing_list_screen(self):
        self.manager.current = "select_packing_list_screen"
    
    def packing_list_screen(self):
        self.manager.current = "packing_list_screen"


class CreatePackingListScreen(Screen):
    def create_packing_list(self, trip_name, start_date, end_date):
        try:
            global packing_list
            packing_list = PackingList(trip_name.text, start_date.text, end_date.text)
            packing_list.write_yaml()
            print("Creating..." + str(packing_list)
                  + '...and writing to filename test_austin.yaml')
            self.manager.current = "packing_list_screen"
        except ValueError:
            self.ids.input_error.text = "Date Input must be in 'YYYY-MM-DD' form. Please try again."


class SelectPackingListScreen(Screen):

    def __init__(self, **kwargs):
        super(SelectPackingListScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=1) 
        filenames = PackingList.list_packing_lists()
        for filename in filenames:
            btn = Button(text=filename, on_press=self.packing_list_screen)
            layout.add_widget(btn)
        self.add_widget(layout)
    
    def packing_list_screen(self, btn):
        rv = self.manager.get_screen('packing_list_screen').ids.dataview
        rv.current_packing_list_filename = btn.text + '.yaml'
        rv.get_packing_list()
        self.manager.current = "packing_list_screen"


class PackingListScreen(Screen):

    def select_packing_list_screen(self):
        self.manager.current = "select_packing_list_screen"
    

class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()