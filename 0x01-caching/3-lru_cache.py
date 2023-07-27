#!/usr/bin/python3
""" LRUCache module
"""
from collections import OrderedDict
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache inherits from BaseCaching and implements LRU replacement
    """
    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.cache_data = OrderedDict(self.cache_data)

    def put(self, key, item):
        """ Adds an item to the cache using the LRU replacement policy
        """
        if key is None or item is None:
            return

        # move the accessed key to the end
        if key in self.cache_data.keys():
            self.cache_data.move_to_end(key)

        # if cache is full remove the least recently used (first item)
        elif len(self.cache_data) + 1 > BaseCaching.MAX_ITEMS:
            first = self.cache_data.popitem(last=False)
            print('DISCARD: {}'.format(first[0]))

        self.cache_data[key] = item

    def get(self, key):
        """ Returns a cache item
        """
        if key is None or self.cache_data.get(key) is None:
            return None

        # move the accessed key to last
        self.cache_data.move_to_end(key)
        return self.cache_data.get(key)
