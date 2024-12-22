from typing import List, Optional


class Item:
    def __init__(self, id: str, name: str, quantity: int, weight: int):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.weight = weight

    def __repr__(self):
        return f"Item(id='{self.id}', name='{self.name}', quantity={self.quantity}, weight={self.weight})"


class Container:
    def __init__(self, id: str, child_containers: Optional[List['Container']] = None,
                 items: Optional[List[Item]] = None):
        self.id = id
        self.child_containers = child_containers if child_containers is not None else []
        self.items = items if items is not None else []

        # Enforce mutual exclusivity
        if self.child_containers and self.items:
            raise ValueError(f"Container '{self.id}' cannot contain both child containers and items.")

    def add_child_container(self, container: 'Container'):
        if self.items:
            raise ValueError(f"Cannot add child containers to Container '{self.id}' as it already contains items.")
        self.child_containers.append(container)

    def add_item(self, item: Item):
        if self.child_containers:
            raise ValueError(f"Cannot add items to Container '{self.id}' as it already contains child containers.")
        self.items.append(item)


class InventoryQuery:
    @staticmethod
    def query_items_over_weight(container: Container, weight_threshold: int) -> List[Item]:
        """
        Recursively traverse the container hierarchy and collect items over the specified weight.

        :param container: The root container to start the search.
        :param weight_threshold: The weight threshold in kilograms.
        :return: List of items that weigh more than the specified threshold.
        """
        result = []
        # If container has items, filter them
        if container.items:
            for item in container.items:
                if item.weight > weight_threshold:
                    result.append(item)
        # If container has child containers, recurse
        elif container.child_containers:
            for child in container.child_containers:
                result.extend(InventoryQuery.query_items_over_weight(child, weight_threshold))
        return result


def main():
    # Test Case 1: Basic functionality
    try:
        # Create items
        item1 = Item(id="I001", name="Laptop", quantity=10, weight=2)
        item2 = Item(id="I002", name="Refrigerator", quantity=5, weight=60)
        item3 = Item(id="I003", name="Washing Machine", quantity=3, weight=55)

        # Create containers
        container1 = Container(id="C001", items=[item1])
        container2 = Container(id="C002", items=[item2, item3])
        root_container = Container(id="C_ROOT", child_containers=[container1, container2])

        # Query
        result = InventoryQuery.query_items_over_weight(root_container, 50)
        expected = [item2, item3]
        assert result == expected, f"Test Case 1 Failed: Expected {expected}, Got {result}"
        print("Test Case 1 Passed: Basic functionality.")
    except Exception as e:
        print(f"Test Case 1 Failed: {e}")

    # Test Case 2: Nested containers
    try:
        # Create items
        item4 = Item(id="I004", name="TV", quantity=7, weight=30)
        item5 = Item(id="I005", name="Microwave", quantity=15, weight=25)
        item6 = Item(id="I006", name="Air Conditioner", quantity=2, weight=70)

        # Create containers
        sub_container1 = Container(id="C003", items=[item4, item5])
        sub_container2 = Container(id="C004", items=[item6])
        container3 = Container(id="C005", child_containers=[sub_container1, sub_container2])
        root_container2 = Container(id="C_ROOT2", child_containers=[container3])

        # Query
        result = InventoryQuery.query_items_over_weight(root_container2, 50)
        expected = [item6]
        assert result == expected, f"Test Case 2 Failed: Expected {expected}, Got {result}"
        print("Test Case 2 Passed: Nested containers.")
    except Exception as e:
        print(f"Test Case 2 Failed: {e}")

    # Test Case 3: Empty container
    try:
        empty_container = Container(id="C_EMPTY")
        result = InventoryQuery.query_items_over_weight(empty_container, 50)
        expected = []
        assert result == expected, f"Test Case 3 Failed: Expected {expected}, Got {result}"
        print("Test Case 3 Passed: Empty container.")
    except Exception as e:
        print(f"Test Case 3 Failed: {e}")

    # Test Case 4: Large data input
    try:
        import random
        import string
        import time

        def generate_random_id(prefix, length=5):
            return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

        large_container = Container(id="C_LARGE")
        num_items = 100000  # Large number of items
        for _ in range(num_items):
            item = Item(
                id=generate_random_id("I"),
                name="Product",
                quantity=random.randint(1, 100),
                weight=random.randint(1, 100)
            )
            large_container.add_item(item)

        start_time = time.time()
        result = InventoryQuery.query_items_over_weight(large_container, 50)
        end_time = time.time()
        print(
            f"Test Case 4 Passed: Large data input. Items found: {len(result)} in {end_time - start_time:.2f} seconds.")
    except Exception as e:
        print(f"Test Case 4 Failed: {e}")

    # Test Case 5: Mutual exclusivity enforcement
    try:
        # Attempt to create a container with both items and child containers
        invalid_container = Container(id="C_INVALID", items=[Item("I007", "Blender", 5, 3)],
                                      child_containers=[Container("C006")])
        print("Test Case 5 Failed: Mutual exclusivity not enforced.")
    except ValueError as ve:
        print("Test Case 5 Passed: Mutual exclusivity enforced.")
    except Exception as e:
        print(f"Test Case 5 Failed: {e}")


if __name__ == "__main__":
    main()
