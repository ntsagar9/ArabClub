"""
Pagination system based on queue principles
"""
import warnings
from django.utils.translation import gettext_lazy as _

from arabclub_pagination.queue import LinkedList
from django.conf import settings


class UnorderedObjectListWarning(RuntimeWarning):
    pass


class NoPaginationSettings(RuntimeWarning):
    pass


class InvalidPage(Exception):
    pass


class EmptyPage(InvalidPage):
    pass


class PageNumberNotInInteger(InvalidPage):
    pass


class Pagination:
    """
    Pagination
    """

    def __init__(self, object_list, page_count=6):
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

        self.__page_manager = Page(self.__slice_object_list)

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
    def __slice_object_list(self):
        """
        Create a list containing a number of lists
        so that each list within the flagship list
        will reflect one page to view
        """
        sliced_list = []
        count = 0
        index = 0
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
            sliced_list.append(temp)
        del self.object_list
        return sliced_list

    @property
    def create_pages(self):
        """Create Page"""
        return self.__page_manager.create()

    def get_next_page(self, current):
        """return following page"""
        return self.__page_manager.get_next_page(current)

    def get_previous_page(self, current):
        """return previous page"""
        return self.__page_manager.get_previous_page(current)

    @property
    def get_latest_page(self):
        """return last page"""
        return self.__page_manager.get_latest_page

    @property
    def get_first_page(self):
        """git first page"""
        return self.__page_manager.get_first_page

    def get_page(self, page_number):
        """Fetch a specific page by selecting the number of each page"""
        page_number = self.validNumber(page_number)
        return self.__page_manager.get_page(page_number).data

    @property
    def get_all(self):
        """return all pages"""
        return self.__page_manager.get_all_pages


class Page:
    """Pages Manager"""

    def __init__(self, object_list=None):
        self.object_list = object_list
        self.pages = LinkedList()
        self.last_page = -1

    def create(self):
        """Create pages"""
        for p in self.object_list:
            self._add_page(p)
        return self.get_first_page

    @property
    def has_first_page(self):
        """Check if there is a start page or not"""
        return True if not self._check_page_is_empty else False

    @property
    def _check_page_is_empty(self):
        """Check if that page is empty or not"""
        return True if self.pages.length < 0 else False

    @property
    def get_first_page(self):
        """get first page"""
        if self._check_page_is_empty:
            return self.pages.get_item(0)
        pass

    def _add_page(self, data):
        """add new page"""
        page = self.pages.push(data)
        self.last_page += 1
        return page

    def get_next_page(self, current_page):
        """get next page"""
        return self.pages.get_item(current_page + 1)

    def get_previous_page(self, current_page):
        """get previous page"""
        return self.pages.get_previous(current_page)

    def get_page(self, page_number):
        """get page by number"""
        return self.pages.get_item(page_number)

    @property
    def get_latest_page(self):
        """get last page"""
        return self.pages.get_item(self.last_page).data

    @property
    def get_all_pages(self):
        """get all pages from queue"""
        return self.pages.get_list()
