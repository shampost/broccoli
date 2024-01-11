class Memory:
    def __init__(self) -> None:
        self.heap = {}
    
    def addItem(self,name,value):
        self.heap[name] = value


