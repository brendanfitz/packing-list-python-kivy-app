from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup

class PackingListItemPopUp(Popup):
    def __init__(self, **kwargs):
        kwargs['size_hint'] = (0.75, 0.75)
        super(PackingListItemPopUp, self).__init__(**kwargs)


class UpdatePackingListPopup(Popup):
    pass


class PackingListItemUpdatePopUp(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        kwargs['size_hint'] = (0.75, 0.75)
        super(PackingListItemUpdatePopUp, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text

