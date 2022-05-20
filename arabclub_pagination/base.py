"""
A queue system based on an "Linked list" principle
"""


class LinkedError(Exception):
    pass


class NegativeNumber(LinkedError):
    pass


class EmptyLinked(LinkedError):
    pass


class EmptyLinkedWarnings(RuntimeWarning):
    pass


class NoneObject(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class EmptyError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class BaseNode:
    """Base Node"""

    __length = -1
    __last_node: None = None

    def __init__(self, data=None):
        self.__data = data
        self.__next = None
        self.__head = None

        if self.__data is not None:
            BaseNode.move_tail(self)
            # BaseNode.__last_node = self
            # BaseNode.length += 1

    def __repr__(self):
        return "{}({}, {})".format(
            self.__class__.__name__, self.__data, self.__next
        )

    def __str__(self):
        return str(BaseNode)

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __len__(self):
        if self.length < 0:
            raise EmptyError(f"{self.__class__.__name__} is empty.!")
        return self.__length

    @classmethod
    def move_tail(cls, obj):
        cls.__last_node = obj
        return cls.__last_node

    @classmethod
    def decrease_length(cls):
        cls.__length -= 1

    @classmethod
    def increase_length(cls):
        cls.__length += 1

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    @property
    def next(self) -> object:
        return self.__next

    @next.setter
    def next(self, obj: object):
        if self.is_valid_object(obj):
            self.__next = obj

    @property
    def head(self) -> object:
        return self.__head

    @head.setter
    def head(self, obj: object):
        if obj.__class__.__name__ == "BaseNode":
            self.__head = obj

    @property
    def tail(self) -> object:
        return BaseNode.__last_node

    @property
    def length(self):
        return BaseNode.__length

    def is_valid_object(self, other):
        try:
            if other.__class__.__name__ == self.__class__.__name__:
                return True
            raise AttributeError
        except AttributeError:
            raise NoneObject(
                """I expect you to pass an object similar to: {}()
            """.format(
                    self.__class__.__name__
                )
            )

    def has_next(self) -> bool:
        return bool(self.__next)

    def is_empty(self) -> bool:
        return False if self.__length >= 0 else True

    def is_valid_index(self, index):
        if index > self.__length:
            raise IndexError("Index out of range.!")

    def push(self, value) -> object:
        last_node = self.tail
        BaseNode.increase_length()
        try:
            last_node.next = BaseNode(value)
            # self.__head.next = BaseNode(value)
            return self.head.next
        except AttributeError:
            self.__head = BaseNode(value)
        return self.__head

    def pop(self):
        BaseNode.decrease_length()
        if BaseNode.__length < 0:
            BaseNode.move_tail(None)
        curr = self.__head
        self.__head = curr.next
        return curr.data

    def get_item(self, index):
        self.is_valid_index(index)
        curr = self.__head
        current_index = 0

        if index == current_index:
            return curr

        while index != current_index:
            current_index += 1
            curr = curr.next
        return curr

    def get_all_items(self) -> list:
        items_list = []

        if len(self) == 0:
            items_list.append(self.pop())
            return items_list

        items_list.append(self.pop())
        return items_list + self.get_all_items()
