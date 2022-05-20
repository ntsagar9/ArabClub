"""
A queue system based on an "Linked list" principle
"""
import warnings
from django.utils.translation import gettext_lazy as _


class LinkedError(Exception):
    pass


class NegativeNumber(LinkedError):
    pass


class EmptyLinked(LinkedError):
    pass


class EmptyLinkedWarnings(RuntimeWarning):
    pass


class Node:
    """Queue with previous"""

    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.previous = None


class LinkedList:
    """Linked-list"""

    def __init__(self):
        self.head = None
        self.length = -1

    def __len__(self):
        return self.length

    def is_empty(self):
        """
        Check that the list is empty
        """
        return True if self.head is None else False

    def push(self, data):
        """
        Push item inside the queue
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.length += 1
            return new_node
        current_node = self.head

        while current_node.next is not None:
            current_node = current_node.next
        new_node.previous = current_node
        current_node.next = new_node
        self.length += 1
        return current_node

    def valid_number(self, number):
        """
        Check that number is valid or not.
        """
        try:
            if number < 0 and number.is_integar():
                raise ValueError
        except (TypeError, ValueError):
            raise NegativeNumber(
                _(
                    """That linked-list is an
                    empty and not support negative number."""
                )
            )
        if number > self.length:
            raise EmptyLinked(_("That number greater than linked length"))
        return number

    def pop(self):
        """
        Remove the following item from the queue
        """
        try:
            self.length = self.valid_length(self.length)
            temp = self.head.data
            self.head = self.head.next
            self.length -= 1

        except EmptyLinked:
            warnings.warn(
                "That Linked is Empty please add items first",
                EmptyLinkedWarnings,
                stacklevel=3,
            )
        return temp

    def get_item(self, index):
        """
        Get the following item from the queue
        Note get is just get
        """
        try:
            index = self.valid_number(index)
            current = 0
            data = self.head
        except NegativeNumber:
            index = 0
        while index > current:
            data = data.next
            current += 1
        return data

    def get_list(self):
        """
        Get all items from the queue
        """
        elements = []
        current_node = self.head
        while current_node is not None:
            elements.append(current_node.data)
            current_node = current_node.next
        return elements

    def get_previous(self, index=None):
        """
        Get the item that accepted the current element of the queue
        """
        if index is None:
            return self.head.previous
        index -= 1
        return self.get_item(index)
