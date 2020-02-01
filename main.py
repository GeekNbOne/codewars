class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None

    def __len__(self):
        return 0


def length(node):
    return len(node) if node else 0


def count(node, data):
    return 0

length(Node(99))