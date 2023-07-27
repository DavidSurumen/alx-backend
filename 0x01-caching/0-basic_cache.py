""" BasicCache module
"""
BaseCaching = __import__('base_caching').BaseCaching

class BasicCache(BaseCaching):
    """ BasicCache inherits from BaseCaching, and defines the methods put and get.
    """
    def __init__(self):
        """ Initialize
        """
        super().__init__()

    def put(self, key, item):
        """ Overrides the parent class' put()
            Adds an item to the cache
        """
        if key is None or item is None:
            return

        self.cache_data[key] = item

    def get(self, key):
        """ Overrides the parent class' get()
            Gets an item from the cache
        """
        if key is None or self.cache_data.get(key) is None:
            return None

        return self.cache_data.get(key)
