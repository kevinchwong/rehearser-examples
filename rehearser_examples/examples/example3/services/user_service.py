from rehearser_examples.examples.example3.cache import Cache


class UserService:
    def __init__(self, cache=None):
        self.cache = cache if cache else Cache()

    def add_user(self, user_id, user_data):
        key = f"user:{user_id}"
        self.cache.add_record(key, user_data)

    def get_user(self, user_id):
        key = f"user:{user_id}"
        try:
            user_data = self.cache.get_record(key)
            return user_data
        except KeyError:
            # If user data is not found in cache, fetch it from the database and add it to the cache
            user_data = self._fetch_user_from_database(user_id)
            self.cache.add_record(key, user_data)
            return user_data

    def update_user(self, user_id, user_data):
        key = f"user:{user_id}"
        try:
            self.cache.update_record(key, user_data)
        except KeyError:
            # If user data is not found in cache, fetch it from the database and add it to the cache
            self._fetch_user_from_database(user_id)
            self.cache.update_record(key, user_data)

    def delete_user(self, user_id):
        key = f"user:{user_id}"
        try:
            self.cache.delete_record(key)
        except KeyError:
            # If user data is not found in cache, fetch it from the database and delete it from the cache
            self._fetch_user_from_database(user_id)
            self.cache.delete_record(key)

    def _fetch_user_from_database(self, user_id):
        # Simulate fetching user data from the database
        user_data = f"User data for user {user_id}"
        return user_data
