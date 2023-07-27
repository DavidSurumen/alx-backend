#!/usr/bin/python3
""" FIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache inherits from BaseCaching
      - implements get and put methods, using FIFO
    """
    def __init__(self):
        """ Initialize
        """
        super().__init__()

    def put(self, key, item):
        """ Overrides parent class' put()
          - discards items using FIFO if max elements reached
        """
        if key is None or item is None:
            return

        self.cache_data[key] = item
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            first = next(iter(self.cache_data))
            print('DISCARD: {}'.format(first))
            self.cache_data.pop(first)

    def get(self, key):
        """ Overrides parent class' get()
          - returns a cache item
        """
        if key is None or self.cache_data.get(key) is None:
            return None

        return self.cache_data.get(key)
