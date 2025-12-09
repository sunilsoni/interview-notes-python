def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance

@singleton
class Logger:
    pass

l1 = Logger()
l2 = Logger()

print(id(l1), id(l2))  # same instance
