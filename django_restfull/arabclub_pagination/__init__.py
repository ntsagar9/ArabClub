import importlib

PAGINATION_NAME = "arabclub_pagination.pagination"


def Pagination(*args, **kwargs):
    mod = importlib.import_module(PAGINATION_NAME, "Pagination")
    return mod.Pagination(*args, **kwargs)
