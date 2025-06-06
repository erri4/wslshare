from linkedlist import LinkedList, DoubleLinkedList, LoopedLinkedList, DoubleLoopedLinkedList


def jump(ll: LinkedList | DoubleLinkedList | LoopedLinkedList | DoubleLoopedLinkedList, start_value, jumps):
    node = ll.find(start_value)
    if jumps >= 0:
        for _ in range(jumps):
            node = node.next
    else:
        for _ in range(-jumps):
            node = node.before
    return node.data
