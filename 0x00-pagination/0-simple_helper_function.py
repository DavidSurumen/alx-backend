#!/usr/bin/env python3
""" This module defines a function 'index_range' for calculating the start and
    end indexes for a specifc page in pagination.
"""


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
