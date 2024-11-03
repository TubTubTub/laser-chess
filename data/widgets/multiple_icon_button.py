from data.widgets.icon_button import IconButton
from data.components.circular_linked_list import CircularLinkedList
from data.components.custom_event import CustomEvent
from data.constants import WidgetState

class MultipleIconButton(IconButton):
    def __init__(self, icons_dict, **kwargs):
        self._icons_dict = icons_dict
        self._icons = CircularLinkedList(list(self._icons_dict.keys()))
        self._icon_key = self._icons.get_head()
        self._icon = self._icons_dict[self._icon_key.data]
        super().__init__(icon=self._icon, **kwargs)
    
    def up_func(self):
        before_state = self.get_widget_state()
        super().up_func()

        if before_state == WidgetState.PRESS:
            self._icon_key = self._icon_key.next
            self._icon = self._icons_dict[self._icon_key.data]

            self.set_image()
        
    def process_event(self, event):
        widget_event = super().process_event(event)

        if widget_event:
            return CustomEvent(widget_event.type, pvc_enabled=self._icon_key.data)