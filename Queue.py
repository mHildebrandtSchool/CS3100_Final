from LinkedList import LinkedList
from Node import Node
class Queue():

    def __init__(self):
        self.list = LinkedList()

    def enqueue(self, new_item):
        new_node = Node(new_item)
        self.list.append(new_node)
    
    def dequeue(self):
        dequeue_item = self.list.head.data
        self.list.remove_head()
        return dequeue_item
    
    def print_info(self):
        self.list.print_info()
    
