#Python linked list code saved from CS2700 Zybook(Virtual Text Book)

class LinkedList():

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, new_node):
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def print_info(self):
        temp = self.head
        while temp is not None:
            if temp.next == None:
                print(temp.data)
            else:
                print(temp.data, end=',')
            temp = temp.next