#!/usr/bin/env python3

class InventoryManager:
    """
    A simple inventory management system to add items and get their stock levels.
    Items and their stock are stored in a dictionary.
    """

    def __init__(self):
        self.items = {}

    def add_item(self, item_name, stock_level):
        """
        Adds a new item to the inventory or updates stock if item already exists.
        :param item_name: Name of the item.
        :param stock_level: Current stock level (integer).
        """
        if stock_level < 0:
            print(f"Warning: Attempted to add a negative stock level for '{item_name}'. Defaulting to 0.")
            stock_level = 0
        self.items[item_name] = stock_level

    def get_stock(self, item_name):
        """
        Retrieves the current stock level for a given item.
        :param item_name: Name of the item.
        :return: Stock level (integer) or -1 if item does not exist.
        """
        return self.items.get(item_name, -1)

def main():
    # Create an instance of InventoryManager
    manager = InventoryManager()

    # =======================
    # Test Cases
    # =======================

    # 1) Add a new item and check stock
    manager.add_item("Laptop", 50)
    result = manager.get_stock("Laptop")
    expected = 50
    print("Test 1 - Add/Get an Item:", "PASS" if result == expected else f"FAIL (Expected {expected}, got {result})")

    # 2) Add another item with zero stock
    manager.add_item("Mouse", 0)
    result = manager.get_stock("Mouse")
    expected = 0
    print("Test 2 - Add/Get Zero Stock:", "PASS" if result == expected else f"FAIL (Expected {expected}, got {result})")

    # 3) Check an item that does not exist
    result = manager.get_stock("Keyboard")  # Not added
    expected = -1
    print("Test 3 - Get Non-existent Item:", "PASS" if result == expected else f"FAIL (Expected {expected}, got {result})")

    # 4) Add an item with negative stock
    manager.add_item("Monitor", -5)
    result = manager.get_stock("Monitor")
    expected = 0  # We handle negative stock by defaulting to 0 in this example
    print("Test 4 - Add Item with Negative Stock:", "PASS" if result == expected else f"FAIL (Expected {expected}, got {result})")

    # 5) Add existing item with new stock
    manager.add_item("Laptop", 100)  # Update the existing "Laptop" stock
    result = manager.get_stock("Laptop")
    expected = 100
    print("Test 5 - Update Existing Item Stock:", "PASS" if result == expected else f"FAIL (Expected {expected}, got {result})")

    # 6) Large Data Test
    # Attempting to add a large number of items to confirm it can handle scale
    # (This is a simplified demonstration, actual large-scale tests might be in the thousands or millions)
    large_data_count = 10000  # Example size
    for i in range(large_data_count):
        manager.add_item(f"Item_{i}", i)
    # Just check a random sample
    result = manager.get_stock("Item_9999")
    expected = 9999
    print("Test 6 - Large Data Handling:", "PASS" if result == expected else f"FAIL (Expected {expected}, got {result})")

if __name__ == "__main__":
    main()
