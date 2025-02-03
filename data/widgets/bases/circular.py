from data.components.circular_linked_list import CircularLinkedList

class _Circular:
    def __init__(self, items_dict, **kwargs):
        self._items_dict = items_dict
        self._keys_list = CircularLinkedList(list(items_dict.keys()))
    
    @property
    def current_key(self):
        return self._keys_list.get_head().data

    @property
    def current_item(self):
        return self._items_dict[self.current_key]
    
    def set_next_item(self):
        self._keys_list.shift_head()
    
    def set_previous_item(self):
        self._keys_list.unshift_head()

    def set_to_key(self, key):
        if self._keys_list.data_in_list(key) is False:
            raise ValueError('(_Circular.set_to_key) Key not found:', key)
        
        for _ in range(len(self._items_dict)):
            if self.current_key == key:
                self.set_image()
                self.set_geometry()
                return
            
            self.set_next_item()