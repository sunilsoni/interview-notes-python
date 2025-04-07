class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class CustomHashMap:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        index = self._hash(key)
        if not self.buckets[index]:
            self.buckets[index] = Node(key, value)
            self.size += 1
        else:
            current = self.buckets[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                if not current.next:
                    current.next = Node(key, value)
                    self.size += 1
                    return
                current = current.next

        if self.size / self.capacity >= 0.75:
            self._resize()

    def get(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def _resize(self):
        self.capacity *= 2
        new_buckets = [None] * self.capacity
        for bucket in self.buckets:
            current = bucket
            while current:
                index = self._hash(current.key)
                if not new_buckets[index]:
                    new_buckets[index] = Node(current.key, current.value)
                else:
                    node = new_buckets[index]
                    while node.next:
                        node = node.next
                    node.next = Node(current.key, current.value)
                current = current.next
        self.buckets = new_buckets