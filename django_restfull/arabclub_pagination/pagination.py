"""
Pagination system based on queue principles
"""
import warnings
from django.utils.translation import gettext_lazy as _
from arabclub_pagination.doubly_linkedlist import DoublyLinkedListNode
from django.conf import settings


class UnorderedObjectListWarning(RuntimeWarning):
    pass


class NoPaginationSettings(RuntimeWarning):
    pass


class InvalidPage(Exception):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    pass


class EmptyPage(InvalidPage):
    pass


class PageNumberNotInInteger(InvalidPage):
    pass


class Pagination:
    __temp = []
    __save_index = 0

    def __init__(self, object_list=__temp, page_count=6):
        self.object_list = object_list

        # Load pagination settings
        try:
            if hasattr(settings, "PAGINATION"):
                self.page_count = settings.PAGINATION.get(
                    "page_count", page_count
                )
            else:
                self.page_count = page_count
                raise AttributeError
        except AttributeError:
            warnings.warn(
                """You have not set up the pagination settings
                 and the pagination system will work in default settings""",
                NoPaginationSettings,
                stacklevel=3,
            )
        self.__page_manager = Page()

    @classmethod
    def temp(cls):
        return Pagination.__temp

    @classmethod
    def set_temp(cls, data):
        cls.__temp.append(data)
        return cls.__temp

    @classmethod
    def save_index(cls):
        return cls.__save_index

    @classmethod
    def increase_save_index(cls):
        cls.__save_index += 1

    @classmethod
    def reset_save_index(cls):
        cls.__temp.clear()
        cls.__save_index = 0

    def validNumber(self, number):
        """
        Check that number is valid or not.
        """
        try:
            number = int(number) - 1
            if not type(number) is int:
                raise ValueError
        except (TypeError, ValueError):
            raise PageNumberNotInInteger(_("That page number is not Integer."))
        if number < 0:
            raise EmptyPage(_("That page number less than 1."))
        if number > self.page_count or number == self.page_count:
            raise EmptyPage(_("That page contains no result."))

        return number

    @property
    def _get_page_size(self):
        """
        return item size per page
        """
        return len(self.object_list) // self.page_count

    @property
    def _get_reminder(self):
        """
        Return the number of remaining items
         that will not be included on any of the pages currently
        """
        return len(self.object_list) % self.page_count

    @property
    def get_range(self):
        """
        Return page range from 1 to n.
        """
        return range(1, self.page_count + 1)

    @property
    def is_temped(self):
        current_index = self.__save_index // self.page_count
        if len(self.__temp) > 0 and self._get_page_size == current_index:
            return True
        return False

    @property
    def __slice_object_list(self):
        """
        Create a list containing a number of lists
        so that each list within the flagship list
        will reflect one page to view
        """
        count = 0
        index = 0

        if self.is_temped:
            return self.temp()
        self.reset_save_index()
        while count <= self.page_count:
            count += 1
            temp = []
            page_size = 0
            while (
                page_size <= self._get_page_size
                and index < self.object_list.__len__()
            ):
                temp.append(self.object_list[index])
                index += 1
                page_size += 1
                self.increase_save_index()
            if len(temp):
                self.set_temp(temp)
        return self.temp()

    @property
    def create_pages(self):
        self.__page_manager.object_list = self.__slice_object_list
        self.__page_manager.object = self.__page_manager.create()
        return self.__page_manager.object

    def get_next_page(self, current):
        return self.__page_manager.get_next_page(current)

    def get_previous_page(self, current):
        return self.__page_manager.get_previous_page(current)

    @property
    def get_latest_page(self):
        return self.__page_manager.get_latest_page

    @property
    def get_first_page(self):
        return self.__page_manager.get_first_page

    def get_page(self, page_number):
        page_number = self.validNumber(page_number)
        return self.__page_manager.get_page(page_number).data

    @property
    def get_all(self):
        return self.__page_manager.get_all_pages


class Page:
    __object = None
    __head_middle = None

    def __init__(self, object_list=None):
        self.object_list = object_list
        self.pages = DoublyLinkedListNode()
        self.last_page = -1

    @classmethod
    def object(cls):
        return cls.__object

    @classmethod
    def set_object(cls, head):
        cls.__object = head

    def create(self):
        """Create pages"""
        if self.object():
            self.pages.head = Page.__object
            return Page.__object

        for p in self.object_list:
            self.set_object(self._add_page(p))
        return self.object()

    @property
    def has_first_page(self):
        return True if not self._check_page_is_empty else False

    @property
    def _check_page_is_empty(self):
        return True if self.pages.length < 0 else False

    @property
    def get_first_page(self):
        if self._check_page_is_empty:
            return self.pages.get_item(0)

    def _add_page(self, data):
        page = self.pages.push(data)
        self.last_page += 1
        return page

    def get_next_page(self, current_page):
        return self.pages.get_item(current_page + 1)

    def get_previous_page(self, current_page):
        return self.pages.get_previous(current_page)

    def get_page(self, page_number):
        return self.pages.get_item(page_number)

    @property
    def get_latest_page(self):
        return self.pages.get_item(self.last_page).data

    @property
    def get_all_pages(self):
        return self.pages.get_all_items()
