from packing_list import PackingList 
from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from screens.packing_list_screen import PackingListScreen

class LoadPackingListScreen(Screen):

    def update_layout(self):
        grid = self.ids.grid
        grid.clear_widgets()
        filenames = PackingList.list_packing_lists()
        for filename in filenames:
            rel_layout = RelativeLayout()
            btn_kwargs = dict(
                text=filename,
                on_press=self.packing_list_screen,
                size_hint=(1, 0.5),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            btn = Button(**btn_kwargs)
            rel_layout.add_widget(btn)
            grid.add_widget(rel_layout)

    def packing_list_screen(self, btn):
        screen = self.manager.get_screen('packing_list_screen')
        filename = btn.text + '.yaml'
        PackingListScreen.current_packing_list = PackingList.read_yaml(filename)
        screen.update_layout()
        self.manager.current = "packing_list_screen"