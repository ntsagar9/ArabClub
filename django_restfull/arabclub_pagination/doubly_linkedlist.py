from arabclub_pagination.base import BaseNode


class LinkedError(Exception):
    pass


class NegativeNumber(LinkedError):
    pass


class EmptyLinked(LinkedError):
    pass


class EmptyLinkedWarnings(RuntimeWarning):
    pass


class DoublyLinkedListNode(BaseNode):
    """Queue with previous"""

    def __init__(self, data=None):
        super().__init__(data)
        self.__previous = None

    @property
    def previous(self):
        return self.head.previous

    @previous.setter
    def previous(self, obj):
        self.__previous = obj

    def push(self, value) -> object:
        """
        super = BaseNode
        head = First BaseNode
        push item in BaseNode. Data
        add new attribute in baseNode "previous"
        access to previous from head
        """
        if self.length < 0:
            super().push(value)
            return self.head
        self.head.next = super().push(value)
        last = self.tail
        self.head.previous = last
        return self.head
