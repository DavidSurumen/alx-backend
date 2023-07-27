#!/usr/bin/python3
""" LIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache inherits from Basecaching, and implements
        LIFO replacement policy
    """
    def __init__(self):
        """ Initialize
        """
        super().__init__()

    def put(self, key, item):
        """ Adds an item to the cache using LIFO replacement
        """
        if key is None or item is None:
            return

        if self.cache_data.get(key) is not None:
            self.cache_data.pop(key)

        self.cache_data[key] = item

        if len(self.cache_data) > 4:
            last = list(self.cache_data.keys())[-2]
            print('DISCARD: {}'.format(last))
            self.cache_data.pop(last)

    def get(self, key):
        """ Returns a cache item
        """
        if key is None or self.cache_data.get(key) is None:
            return None
        return self.cache_data.get(key)
