#!/usr/bin/python3
""" MRUCache module
"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache inherits from BaseCaching and implements MRU
        replacement algorithm
    """
    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.cache_data = OrderedDict(self.cache_data)

    def put(self, key, item):
        """ Adds an item the cache, using MRU replacement algo
        """
        if key is None or item is None:
            return

        # move modified key to the last
        if key in self.cache_data.keys():
            self.cache_data.move_to_end(key)

        elif len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
            # remove the most recently used (last item)
            last = self.cache_data.popitem()
            print('DISCARD: {}'.format(last[0]))

        self.cache_data[key] = item

    def get(self, key):
        """ Returns a cache item
        """
        if key is None or key not in self.cache_data.keys():
            return None

        # move the accessed key to the end
        self.cache_data.move_to_end(key)
        return self.cache_data.get(key)
