#!/usr/bin/env python3
"""This module defines a function 'index_range' for calculating the start and
    end indexes for a specifc page in pagination.
"""
import csv
import math
from typing import List


def index_range(page, page_size):
    """
    Calculate the start and end indexes for a specific page in pagination.

    Parameters:
        page (int): current page number (1-indexed)
        page_size (int): number of items to be displayed per page

    Return:
        tuple: A tuple of size two containing a start index and an end index
        corresponding to the range of indexes to return in a list for the
        particular pagination parameters.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        assert type(page) is int and page > 0, \
                "page must be an integer greater than 0"

        assert type(page_size) is int and page_size > 0, \
            "page size must be an integer than 0"

        ranges = index_range(page, page_size)
        return self.dataset()[ranges[0]:ranges[1]]
