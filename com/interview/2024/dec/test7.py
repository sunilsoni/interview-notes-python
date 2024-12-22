"""Amazon has warehouse all around the world. In each warehouse the way we track inventory items is quite simple -

Amazon has warehouse all around the world. In each warehouse the way we track inventory items is quite simple - we have containers (think of them like open boxes where you can put stuff in and take stuff out).
There are two rules about Containers - they can contain other containers OR they can contain items(products for customers), but not both.
public class Container {
private String id;
private List<Container> childContainers;
private List<Item> items;
public class Item {
private String id; private String name; private int quantity; private int weight;
For auditing purposes, as a software engineer I want to query for items over 50kgs


so Amazon has warehouse all over the world. In this example. And let's say the way we track items that our warehouse is that we use a simple container class. And this container class can contain items or can contain. For containers that could contain.
In this example. And let's say the way we track items that our warehouse is that we use a simple container class. And this container class can contain items or can contain. for containers that could contain the very, but so now let's say that I as a software engineer want to query for list of items that meet some conditions, so, for other purposes, I want to find a list of items that are over let's say.
items that meet some conditions, so, for other purposes, I want to find a list of items that are over let's say 50,000. East. Okay. Can you see repeated? Okay. Yeah. Okay, so So we want to write some kind of library that other engineers or other developers could use to query for items that meet some criteria. Okay. And the first example that we get is, A simple example for all items that are over.

For auditing purposes, as a software engineer I want to query for items over 50kgs
"""

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
        if self.childContainers:
            raise ValueError("This container already has child containers. Cannot add items.")
        self.items.append(item)

    def add_container(self, container):
        if self.items:
            raise ValueError("This container already has items. Cannot add containers.")
        self.childContainers.append(container)


def find_items(container, filter_func):
    """
    Recursively finds all items in the container hierarchy that match a given condition.
    The condition is defined by filter_func, a function that takes an Item and returns True/False.
    """
    result = []
    if container.items:
        # Leaf container holding items - apply the filter to each item
        for item in container.items:
            if filter_func(item):
                result.append(item)
    else:
        # Not a leaf, so it has child containers - recurse into each
        for child in container.childContainers:
            result.extend(find_items(child, filter_func))
    return result


def test_find_items():
    # Construct a test structure
    root = Container("root")

    c1 = Container("c1")
    c1.add_item(Item("item1", "Item One", 10, 45))
    c1.add_item(Item("item2", "Item Two", 5, 60))
    c1.add_item(Item("item3", "Item Three", 2, 100))

    c2 = Container("c2")
    c21 = Container("c21")
    c21.add_item(Item("item4", "Item Four", 1, 50))
    c21.add_item(Item("item5", "Item Five", 1, 51))
    c2.add_container(c21)

    c3 = Container("c3")

    root.add_container(c1)
    root.add_container(c2)
    root.add_container(c3)

    # Example 1: Find items over 50 kg
    heavy_items = find_items(root, lambda item: item.weight > 50)
    print("Items over 50 kg:", heavy_items)

    # Example 2: Find items by a specific ID
    # Suppose we want to find an item with ID "item5"
    specific_item = find_items(root, lambda item: item.id == "item5")
    print("Items with ID == 'item5':", specific_item)

    # Example 3: Find items by name keyword
    # Suppose we want items whose name contains "Three"
    name_match_items = find_items(root, lambda item: "Three" in item.name)
    print("Items whose name contains 'Three':", name_match_items)

    # Example 4: Find items by minimum quantity
    # Suppose we want items with quantity >= 5
    high_quantity_items = find_items(root, lambda item: item.quantity >= 5)
    print("Items with quantity >= 5:", high_quantity_items)


if __name__ == "__main__":
    test_find_items()
