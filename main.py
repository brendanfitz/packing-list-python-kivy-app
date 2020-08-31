from packing_list import PackingList, PackingItem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('design.kv')

class HomeScreen(Screen):
    def create_packing_list_screen(self):
        self.manager.current = "create_packing_list_screen"
    
    def packing_list_screen(self):
        self.manager.current = "packing_list_screen"

class CreatePackingListScreen(Screen):
    def create_packing_list(self, trip_name, start_date, end_date):
        try:
            global packing_list
            packing_list = PackingList(trip_name.text, start_date.text, end_date.text)
            packing_list.write_yaml('austin_test.yaml')
            print("Creating..." + str(packing_list)
                  + '...and writing to filename test_austin.yaml')
            self.manager.current = "packing_list_screen"
        except ValueError:
            self.ids.input_error.text = "Date Input must be in 'YYYY-MM-DD' form. Please try again."


class PackingListScreen(Screen):

    def __init__(self, **kwargs):
        print("initializing packing list screen")
        super(PackingListScreen, self).__init__(**kwargs)
        self.get_item_list()
    
    def get_item_list(self):
        layout = GridLayout(cols=3)
        self.add_widget(layout) 
        import pdb; pdb.set_trace()
        packing_list = PackingList.read_yaml('austin.yaml')
        for item in packing_list.item_list:
            for data in item:
                label = Label(text=str(data))
                layout.add_widget(label)
    

class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()