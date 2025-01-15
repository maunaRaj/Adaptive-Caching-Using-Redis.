import redis
import random


class MLDrivenCache:
    def __init__(self, redis_host='localhost', redis_port=6379, capacity=100):
        self.client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        self.capacity = capacity
        self.model = self.train_model()  # Placeholder for ML model

    def train_model(self):
        # Placeholder for training an ML model - can be replaced with a real model
        return lambda x: random.choice([True, False])  # Mock decision


    def access(self, key, value=None):
        if self.client.exists(key):
            # Refresh the key's position in the LRU with a GET operation
            self.client.get(key)  # This updates its last used time for LRU tracking
        else:
            self.insert(key, value)


    def insert(self, key, value):
        if self.client.dbsize() >= self.capacity:
            # Eviction will be handled by Redis' policy, but you can prune proactively if needed
            self.evict()


        # Based on the ML model's recommendation, manipulate data placement
        if self.model(key):
            # Strongly cache for longer, could adjust based on inside thresholding logic
            self.client.set(key, value, ex=600)  # 10 minute expiration, example setup
        else:
            # Default caching with possibly shorter TTL, based on model guiding intervals
            self.client.set(key, value, ex=300)  # 5 minute expiration, example setup


    def evict(self):
        # Could manually evict if certain logic requires it, but Redis's policy should handle it
        pass


    def display(self):
        # Display the current cache keys for verification
        keys = self.client.keys('*')
        print("Cached Keys:", keys)


# Example Usage:
cache = MLDrivenCache(capacity=10)
cache.access('a', 'data1')
cache.access('b', 'data2')
cache.access('a')  # Refreshing 'a'
cache.access('c', 'data3')
cache.display()
