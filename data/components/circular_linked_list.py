class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

class CircularLinkedList: # Doubly-linked circular linked list
    def __init__(self, list_to_convert=None):
        self._head = None

        if list_to_convert:
            for item in list_to_convert:
                self.insert_at_end(item)
    
    def __str__(self):
        if self._head is None:
            return '| empty |'
        
        characters = '| -> '
        current_node = self._head
        while True:
            characters += str(current_node.data) + ' -> '
            current_node = current_node.next

            if current_node == self._head:
                characters += '|'
                return characters
    
    def insert_at_beginning(self, data):
        new_node = Node(data)

        if self._head is None:
            self._head = new_node
            new_node.next = self._head
            new_node.previous = self._head
        else:
            current_node = self._head.previous
            current_node.next = new_node
            new_node.next = self._head
            new_node.previous = current_node
            self._head.previous = new_node
            self._head = new_node
    
    def insert_at_end(self, data):
        new_node = Node(data)

        if self._head is None:
            self._head = new_node
            new_node.next = self._head
            new_node.previous = self._head
        else:
            current_node = self._head.previous
            current_node.next = new_node
            new_node.next = self._head
            new_node.previous = current_node
            self._head.previous = new_node
    
    def insert_at_index(self, data, index):
        if index < 0:
            raise ValueError('Invalid index! (CircularLinkedList.insert_at_index)')
        
        if index == 0:
            self.insert_at_beginning(data)
        else:
            new_node = Node(data)
            current_node = self._head
            count = 0

            while count < index - 1 and current_node.next != self._head:
                current_node = current_node.next
                count += 1
            
            if count == (index - 1):
                new_node.next = current_node.next
                new_node.previous = current_node
                current_node.next = new_node
            else:
                raise ValueError('Index out of range! (CircularLinkedList.insert_at_index)')
    
    def delete(self, data):
        if self._head is None:
            return
        
        if self._head.data == data:
            if self._head.next == self._head:
                self._head = None
            else:
                current_node = self._head.previous
                current_node.next = self._head.next
                self._head.next.previous = current_node
                self._head = self._head.next
            return
        
        current_node = self._head
        previous_node = None

        while current_node.next != self._head:
            if current_node.data == data:
                previous_node.next = current_node.next
                current_node.next.previous = previous_node
                return

            previous_node = current_node
            current_node = current_node.next

        if current_node.data == data:
            previous_node.next = current_node.next
            current_node.next.previous = previous_node
        else:
            raise ValueError('Data not found in circular linked list! (CircularLinkedList.delete)')
    
    def data_in_list(self, data):
        if self._head is None:
            return False
        
        current_node = self._head
        while True:
            if current_node.data == data:
                return True
            
            current_node = current_node.next
            if current_node == self._head:
                return False
    
    def shift_head(self):
        self._head = self._head.next

    def unshift_head(self):
        self._head = self._head.previous
    
    def get_head(self):
        return self._head