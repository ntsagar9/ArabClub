class Node:
    __count = -1

    def __init__(self, data=None) -> None:
        self.data = data
        self.next = None
        Node.__count += 1

    @classmethod
    def floor_count(cls):
        cls.__count -= 1

    @classmethod
    def __len__(cls):
        return cls.__count
