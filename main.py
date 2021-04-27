from packing import PackingList, PackingItem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from packing.utils.datepicker import DatePicker
from packing.screens.home_screen import HomeScreen 
from packing.screens.load_packing_list_screen import LoadPackingListScreen
from packing.screens.packing_list_screen import PackingListScreen
from packing.widgets.recycle_view_data_table import RecycleViewDataTable
from packing.widgets.selectable_button import SelectableButton
from packing.widgets.hoverable_button import HoverableButton

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