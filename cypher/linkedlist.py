class Node:
    def __init__(self, data):
        self.data = data
        self.next: Node = None

    
    def __str__(self):
        return str(self.data)


class LoopedNode(Node):
    def __init__(self, data):
        super().__init__(data)


class DoubleNode(Node):
    def __init__(self, data):
        super().__init__(data)
        self.before: Node = None


class DoubleLoopedNode(DoubleNode, LoopedNode):
    def __init__(self, data):
        super().__init__(data)


class LinkedList:
    def __init__(self, ls = []):
        self.head = None
        for item in ls:
            self.append(item)
        self._iter_node = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def __iter__(self):
        self._iter_node = self.head
        return self

    def __next__(self):
        if self._iter_node is None:
            raise StopIteration
        data = self._iter_node.data
        self._iter_node = self._iter_node.next
        return data
    

    def find(self, value):
        node = self.head
        while node:
            if node.data == value:
                return node
            node = node.next
            if node == self.head or node is None:
                break
        return None


class LoopedLinkedList(LinkedList):
    def append(self, data):
        new_node = LoopedNode(data)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
            return
        last = self.head
        while last.next != self.head:
            last = last.next
        last.next = new_node
        new_node.next = self.head

    def find(self, value) -> LoopedNode:
        return super().find(value)


class DoubleLinkedList(LinkedList):
    def append(self, data):
        new_node = DoubleNode(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
        new_node.before = last


    def find(self, value) -> DoubleNode:
        return super().find(value)


class DoubleLoopedLinkedList(DoubleLinkedList, LoopedLinkedList):
    def append(self, data):
        new_node = DoubleLoopedNode(data)
        if not self.head:
            self.head = new_node
            new_node.before = self.head
            new_node.next = self.head
            return
        last = self.head
        while last.next != self.head:
            last = last.next
        last.next = new_node
        new_node.before = last
        new_node.next = self.head
        self.head.before = new_node


    def find(self, value) -> DoubleLoopedNode:
        return super().find(value)