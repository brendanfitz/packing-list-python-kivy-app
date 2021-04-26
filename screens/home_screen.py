from packing import PackingList, PackingItem, PackingDateValueError
from kivy.uix.screenmanager import Screen
from screens.packing_list_screen import PackingListScreen

class HomeScreen(Screen):
    def create_packing_list(self):
        packing_list_inputs = self.ids.packing_list_inputs
        trip_name = packing_list_inputs.ids.trip_name.text
        start_date = packing_list_inputs.ids.start_date.text
        end_date = packing_list_inputs.ids.end_date.text

        if trip_name == '':
            self.ids.input_error.text = "Please enter a Trip Date"
            return
        elif start_date == '':
            self.ids.input_error.text = "Please enter a Start Date"
            return
        elif end_date == '':
            self.ids.input_error.text = "Please enter an End Date"
            return

        try:
            packing_list = PackingList(trip_name, start_date, end_date)
        except PackingDateValueError:
            self.ids.input_error.text = "Trip End Date is before the Start Date. Please try again."
        except ValueError:
            self.ids.input_error.text = "Date Input must be in 'YYYY-MM-DD' form. Please try again."
        else:
            packing_list.write_yaml()

            PackingListScreen.current_packing_list = packing_list

            screen = self.manager.get_screen('packing_list_screen')
            screen.update_layout()
            self.manager.current = "packing_list_screen"
            self.clear_packing_list_inputs()
    
    def load_packing_list_screen(self):
        screen_name ='load_packing_list_screen'
        self.manager.get_screen(screen_name).update_layout()
        self.manager.current = screen_name
    
    def clear_packing_list_inputs(self):
        inputs = self.ids.packing_list_inputs
        inputs.ids.trip_name.text = ""
        inputs.ids.start_date.text = ""
        inputs.ids.end_date.text = ""
