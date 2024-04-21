'''Memory'''
class Memory:
    '''
    # TODO: docstring
    '''
    # - addItem: add a new item to the heap
    # - getItem: get an item from the heap
    # - removeItem: remove an item from the heap
    # - updateItem: update an item in the heap
    # - clear: clear the heap
    # - getAll: get all the items in the heap
    def __init__(self) -> None:
        self.heap = {}
    def get_item(self, name=''):
        '''
        # TODO: WRITE DOCSTRINGj 
        '''
        try:
            return self.heap[name]
        except:
            return None
    def remove_item(self,name):
        '''
        # TODO: WRITE DOCSTRINGj 
        '''
        del self.heap[name]
    def add_item(self,name,value):
        '''
        # TODO: WRITE DOCSTRINGj 
        '''
        self.heap[name] = value
    def clear(self):
        '''
        # TODO: WRITE DOCSTRINGj 
        '''
        self.heap.clear()
    def get_all(self):
        '''
        # TODO: WRITE DOCSTRINGj 
        '''
        return self.heap
