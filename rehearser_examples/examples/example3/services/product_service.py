from rehearser_examples.examples.example3.cache import Cache


class ProductService:
    def __init__(self, cache=None):
        self.cache = cache if cache else Cache()

    def add_product(self, product_id, product_data):
        key = f"product:{product_id}"
        self.cache.add_record(key, product_data)

    def get_product(self, product_id):
        key = f"product:{product_id}"
        try:
            product_data = self.cache.get_record(key)
            return product_data
        except KeyError:
            # If product data is not found in cache, fetch it from the database and add it to the cache
            product_data = self._fetch_product_from_database(product_id)
            self.cache.add_record(key, product_data)
            return product_data

    def update_product(self, product_id, product_data):
        key = f"product:{product_id}"
        try:
            self.cache.update_record(key, product_data)
        except KeyError:
            # If product data is not found in cache, fetch it from the database and add it to the cache
            self._fetch_product_from_database(product_id)
            self.cache.update_record(key, product_data)

    def delete_product(self, product_id):
        key = f"product:{product_id}"
        try:
            self.cache.delete_record(key)
        except KeyError:
            # If product data is not found in cache, fetch it from the database and delete it from the cache
            self._fetch_product_from_database(product_id)
            self.cache.delete_record(key)

    def _fetch_product_from_database(self, product_id):
        # Simulate fetching product data from the database
        product_data = f"Product data for product {product_id}"
        return product_data
