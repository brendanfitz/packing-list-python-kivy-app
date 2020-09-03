
from packing_list import PackingList, PackingItem
from kivy.uix.screenmanager import Screen

class PackingListScreen(Screen):

    def select_packing_list_screen(self):
        pl_screen = self.manager.get_screen('select_packing_list_screen')
        pl_screen.ids.grid.update_layout()
        self.manager.current = "select_packing_list_screen"
    