class Memory:
    # - addItem: add a new item to the heap
    # - getItem: get an item from the heap
    # - removeItem: remove an item from the heap
    # - updateItem: update an item in the heap
    # - clear: clear the heap
    # - getAll: get all the items in the heap
    def __init__(self) -> None:
        self.heap = {}
    def getItem(self,name):
        try:
            return self.heap[name]
        except:
            return None
    def removeItem(self,name):
        del self.heap[name]
    def addItem(self,name,value):
        self.heap[name] = value
    def clear(self):
        self.heap.clear()
    def getAll(self):
        return self.heap