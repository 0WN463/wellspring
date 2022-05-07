class Vertex:
    """Section: Constructor"""
    def __init__(self, value, next_v=None):
        self.value = value
        self.next_v = next_v
    
    """Section: Dunder"""
    def __str__(self):
        return self.value
        
    def __repr__(self):
        return f'Vertex(value: {self.value}, next: Vertex({self.next_v.value if self.next_v else None}))'

    """Section: Insert after"""
    def insert_after(self, value):
        self.next_v = Vertex(value, self.next_v)

    """Section: Delete after"""
    def delete_after(self):
        self.next_v = self.next_v.next_v

class SinglyLinkedList:
    """Section: Constructor"""
    def __init__(self, arr=None):
        self.head = None
        self.tail = None
        
        if arr is None:
            return
        
        self.head = Vertex(arr[0])
        v = self.head
        
        for i in arr[1:]:
            v.next_v = Vertex(i)
            v = v.next_v
        self.tail = v
        
    """Section: Dunder"""
    def __str__(self):
        s = ""
        v = self.head
        
        arr = []
        while v:
            arr.append(v.value)
            v = v.next_v
        
        return '->'.join(map(str, arr))

    def __repr__(self):
        return f'SinglyLinkedList({self})'

    def __len__(self):
        length = 0
        v = self.head
        while v:
            length += 1
            v = v.next_v

        return length

    """Section: Get"""
    def get(self, index:int):
        v = self.head
        for _ in range(index):
            v = v.next_v

        return v

    """Section: Find"""
    def find(self, value):
        v = self.head
        while True:
            if v is None:
                return None
            if v.value == value:
                return v
            
            v = v.next_v

    """Section: Insert at"""
    def insert_at(self, index:int, value):
        if index == 0:
            new_v = Vertex(value, self.head)
            self.head = new_v
            return
        
        v = self.get(index-1)
        v.insert_after(value)

    """Section: Delete"""
    def delete(self, index:int):
        if index == 0:
            self.head = self.head.next_v
            return

        prev_v = self.get(index-1)

        if index == len(self) - 1:
            self.tail = prev_v

        prev_v.delete_after()
