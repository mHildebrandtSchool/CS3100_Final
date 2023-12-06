#Python linked list code saved from CS2700 Zybook(Virtual Text Book)
#Further code and also anlysis of Python Linked List from Udemy.com

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
    
    def search_index(self, index, from_delete = False):
        temp = self.head
        prev = None
        #empty list nothing to delete
        if self.head == None:
            return False
        #if the given index is out of range
        if self.length <= index or index < 0:
            return False
        
        for _ in range(0, index):
            prev = temp
            temp = temp.next

        if from_delete:
            return (prev, temp)
        return temp
    
    def swap_nodes(self, node_a, node_b, prev):
        #swapping from the head
        if prev is None:
            self.head = node_b
        #swapping from not the head
        else:
            prev.next = node_b
            
        node_a.next = node_b.next
        node_b.next = node_a
        return True

    def sort_alpha(self, cmp_value):
        #implement  bubble sort     
        n = self.length + 1
        for _ in range(0, n):
            temp = self.head
            prev = None
            while temp is not None:
                after = temp.next
                if after is not None:
                    if temp.data[cmp_value][0] > after.data[cmp_value][0]:
                        self.swap_nodes(temp, after, prev)
                prev = temp
                temp = temp.next

    def remove_head(self):
        #If the list empty can't remove
        if self.head == None:
            return False
        
        if type(self.tail.data) == str:
            note_id = None
        else:
            note_id = self.tail.data['note_id']
        #save head value
        temp = self.head
        #set head to head's next value
        self.head = self.head.next
        #remove original heads pointer to new head
        temp.next = None
        self.length -= 1
        #If there is only one item in the list then head and tail are the same
        if self.length == 1:
            self.tail = self.head
        return note_id

    def remove_tail(self):
        
        #if the list empty can't remove
        if self.head == None:
            return False
        
        note_id = self.tail.data['note_id']
        #get the previous value by looping to ll.length - 2 (-1 to make it an index & -1 to make it find prev not tail)
        prev = self.search_index(self.length -2)
        #Set tail to previous value
        self.tail = prev
        #remove new tails pointer to old tail
        self.tail.next = None
        self.length -= 1
        if self.length == 1:
            self.head = self.tail
        
        return note_id

    def delete(self, index):
        #index is out of range
        if index < 0 or index >= self.length:
            return False
        
        

        if index == 0:
            #remove head value
            return self.remove_head()
        if index == self.length - 1:
            #remove tail
            return self.remove_tail()
        prev = self.search_index(index - 1)
        temp = prev.next
        note_id = temp.data['note_id']

        prev.next = temp.next
        temp.next = None
        self.length -= 1
        return note_id
        

    def print_info(self):
        temp = self.head
        while temp is not None:
            if temp.next == None:
                print(temp.data)
            else:
                print(temp.data, end=',')
            temp = temp.next