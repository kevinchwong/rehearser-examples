import redis
from datetime import datetime

class Cache:
    def __init__(self, host='localhost', port=6379, db=0, name='cache'):
        self.redis_client = redis.Redis(host=host, port=port, db=db)
        self.name = name
        self.latest_update_datetime = None

    def add_record(self, key, value):
        self.redis_client.set(key, value)
        self.latest_update_datetime = datetime.now()

    def update_record(self, key, value):
        if self.redis_client.exists(key):
            self.redis_client.set(key, value)
            self.latest_update_datetime = datetime.now()
        else:
            raise KeyError(f"Record with key '{key}' does not exist")

    def delete_record(self, key):
        if self.redis_client.exists(key):
            self.redis_client.delete(key)
            self.latest_update_datetime = datetime.now()
        else:
            raise KeyError(f"Record with key '{key}' does not exist")

    def get_record(self, key):
        if self.redis_client.exists(key):
            return self.redis_client.get(key)
        else:
            raise KeyError(f"Record with key '{key}' does not exist")