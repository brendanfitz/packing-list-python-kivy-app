from packing_list import PackingList, PackingItem
from kivy.uix.screenmanager import Screen
from screens.packing_list_screen import PackingListScreen

class HomeScreen(Screen):
    def create_packing_list(self, trip_name, start_date, end_date):
        try:
            trip_name = trip_name.text
            start_date = start_date.text
            end_date = end_date.text

            if trip_name == '':
                self.ids.input_error.text = "Please enter a Trip Date"
                return
            elif start_date == '':
                self.ids.input_error.text = "Please enter a Start Date"
                return
            elif end_date == '':
                self.ids.input_error.text = "Please enter an End Date"
                return

            packing_list = PackingList(trip_name, start_date, end_date)
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
    
    def load_packing_list_screen(self):
        screen_name ='load_packing_list_screen'
        self.manager.get_screen(screen_name).update_layout()
        self.manager.current = screen_name