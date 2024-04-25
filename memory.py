'''
Memory module contains a class that stores token data in a heap structure.
'''
class Memory:
    '''
    Memory class is a class that stores
    the data in the heap memory. It has the following

    Methods:
    1. add_item: add a new item to the heap
    2. get_item: get an item from the heap
    3. remove_item: remove an item from the heap
    4. update_item: update an item in the heap
    5. clear: clear the heap
    6. get_all: get all the items in the heap
    '''
    def __init__(self) -> None:
        self.heap = {}
    def get_item(self, name):
        '''
        get_item method returns the value of the item with the given name.
        
        Parameters:
            name: str
        
        Returns:
            value: heap[name]
        '''
        try:
            return self.heap[name]
        except KeyError:
            return None
    def remove_item(self,name):
        '''
        # todo add description
        '''
        del self.heap[name]
    def add_item(self,name,value):
        '''
        # todo add description
        '''
        self.heap[name] = value
    def clear(self):
        '''
        # todo add description
        '''
        self.heap.clear()
    def get_all(self):
        '''
        # todo add description
        '''
        return self.heap
