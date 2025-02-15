class Item:
    def __init__(self, item_id, name, quantity, weight):
        self.id = item_id
        self.name = name
        self.quantity = quantity
        self.weight = weight

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, quantity={self.quantity}, weight={self.weight})"


class Container:
    def __init__(self, container_id):
        self.id = container_id
        self.childContainers = []
        self.items = []

    def add_item(self, item):
        # If items are added, there should be no childContainers added.
        if self.childContainers:
            raise ValueError("This container already has child containers. Cannot add items.")
        self.items.append(item)

    def add_container(self, container):
        # If containers are added, there should be no items added.
        if self.items:
            raise ValueError("This container already has items. Cannot add containers.")
        self.childContainers.append(container)


def find_items_over_weight(container, weight_limit):
    """
    Recursively find all items in a container (and its nested containers) that have a weight > weight_limit.
    """
    result = []
    if container.items:
        # This container directly holds items
        for item in container.items:
            if item.weight > weight_limit:
                result.append(item)
    else:
        # This container holds other containers
        for child in container.childContainers:
            result.extend(find_items_over_weight(child, weight_limit))
    return result


def test_find_items_over_weight():
    # Construct a hierarchy of containers
    root = Container("root")

    # Container 1 with items
    c1 = Container("c1")
    c1.add_item(Item("item1", "Item One", 10, 45))  # <= 50 kg
    c1.add_item(Item("item2", "Item Two", 5, 60))  # > 50 kg
    c1.add_item(Item("item3", "Item Three", 2, 100))  # > 50 kg

    # Container 2 with child containers
    c2 = Container("c2")
    c21 = Container("c21")
    c21.add_item(Item("item4", "Item Four", 1, 50))  # == 50 kg (not over)
    c21.add_item(Item("item5", "Item Five", 1, 51))  # > 50 kg
    c2.add_container(c21)

    # Container 3 empty
    c3 = Container("c3")

    root.add_container(c1)
    root.add_container(c2)
    root.add_container(c3)

    # Test Case 1: Items over 50 in root (includes nested)
    results = find_items_over_weight(root, 50)
    # Expected: item2 (60), item3 (100), item5 (51)
    expected_ids = {"item2", "item3", "item5"}
    result_ids = {item.id for item in results}

    if result_ids == expected_ids:
        print("Test Case 1: PASS")
    else:
        print("Test Case 1: FAIL", f"Expected: {expected_ids}, Got: {result_ids}")

    # Edge Case: No items > 200 kg
    results = find_items_over_weight(root, 200)
    # Expected: empty
    if len(results) == 0:
        print("Test Case 2: PASS")
    else:
        print("Test Case 2: FAIL", f"Expected empty, got {results}")

    # Edge Case: All items <= 1000 kg (large limit)
    # Everything under 1000 means we only get those above 50 since we are testing the same function
    # Let's just verify performance with no structural fail.
    large_weight_results = find_items_over_weight(root, 1000)
    # Technically, no items over 1000. This tests a scenario where maybe none match.
    if len(large_weight_results) == 0:
        print("Test Case 3: PASS")
    else:
        print("Test Case 3: FAIL", f"Expected empty, got {large_weight_results}")

    # Additional edge test: Container with no items/containers
    empty_container = Container("empty")
    empty_results = find_items_over_weight(empty_container, 50)
    if len(empty_results) == 0:
        print("Test Case 4: PASS")
    else:
        print("Test Case 4: FAIL", f"Expected empty, got {empty_results}")

    # Performance Test (Large Data Simulation)
    # Construct a large number of containers and items
    large_root = Container("large_root")
    large_sub = Container("large_sub")
    for i in range(10000):
        # Mix items slightly above and below the threshold
        weight = 51 if i % 2 == 0 else 49
        large_sub.add_item(Item(f"bulk_item_{i}", "Bulk Item", 1, weight))
    large_root.add_container(large_sub)

    large_results = find_items_over_weight(large_root, 50)
    # Expect about half of them (those even i have weight 51)
    if len(large_results) == 5000:
        print("Test Case 5 (Large Data): PASS")
    else:
        print("Test Case 5 (Large Data): FAIL", f"Expected 5000, got {len(large_results)}")


def main():
    # Execute our test method without using any testing framework
    test_find_items_over_weight()


if __name__ == "__main__":
    main()
