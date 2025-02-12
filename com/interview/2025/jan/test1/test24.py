#!/usr/bin/env python3

class Item:
    """
    Represents an individual inventory item with various attributes.
    """
    def __init__(self, stock, threshold, freshness=None, color=None):
        # Ensure stock and threshold are non-negative
        self.stock = stock if stock >= 0 else 0
        if stock < 0:
            print(f"Warning: Negative stock level provided. Defaulting stock to 0.")

        self.threshold = threshold if threshold >= 0 else 0
        if threshold < 0:
            print(f"Warning: Negative threshold provided. Defaulting threshold to 0.")

        self.freshness = freshness
        self.color = color

class InventoryManager:
    """
    A simple inventory management system to add items with their attributes
    and to retrieve those attributes.
    """
    def __init__(self):
        # Initialize an empty dictionary to hold inventory items
        self.items = {}

    def add_item(self, item_name, stock_level, threshold, freshness=None, color=None):
        """
        Adds a new item to the inventory or updates an existing item with provided attributes.
        :param item_name: Name of the item.
        :param stock_level: Current stock level (integer).
        :param threshold: Minimum desired stock level (integer).
        :param freshness: Optional attribute representing freshness.
        :param color: Optional attribute representing color.
        """
        # Create or update the Item instance in the inventory
        self.items[item_name] = Item(stock_level, threshold, freshness, color)

    def get_stock(self, item_name):
        """
        Retrieves the current stock level for a given item.
        :param item_name: Name of the item.
        :return: Stock level (integer) or -1 if item does not exist.
        """
        if item_name in self.items:
            return self.items[item_name].stock
        return -1

    def get_threshold(self, item_name):
        """
        Retrieves the threshold for a given item.
        :param item_name: Name of the item.
        :return: Threshold (integer) or -1 if item does not exist.
        """
        if item_name in self.items:
            return self.items[item_name].threshold
        return -1

    def get_freshness(self, item_name):
        """
        Retrieves the freshness attribute for a given item.
        :param item_name: Name of the item.
        :return: Freshness value or None if not set or item doesn't exist.
        """
        if item_name in self.items:
            return self.items[item_name].freshness
        return None

    def get_color(self, item_name):
        """
        Retrieves the color attribute for a given item.
        :param item_name: Name of the item.
        :return: Color value or None if not set or item doesn't exist.
        """
        if item_name in self.items:
            return self.items[item_name].color
        return None

def main():
    # Create an instance of InventoryManager
    manager = InventoryManager()

    # =======================
    # Test Cases
    # =======================

    # Test 1: Add a new item and check all attributes
    manager.add_item("Bananas", 10, 7, freshness="Fresh", color="Yellow")
    print("Test 1 - Bananas Stock:", "PASS" if manager.get_stock("Bananas") == 10 else "FAIL")
    print("Test 1 - Bananas Threshold:", "PASS" if manager.get_threshold("Bananas") == 7 else "FAIL")
    print("Test 1 - Bananas Freshness:", "PASS" if manager.get_freshness("Bananas") == "Fresh" else "FAIL")
    print("Test 1 - Bananas Color:", "PASS" if manager.get_color("Bananas") == "Yellow" else "FAIL")

    # Test 2: Add another item with different attributes
    manager.add_item("Apples", 20, 5, freshness="Crisp", color="Red")
    print("Test 2 - Apples Stock:", "PASS" if manager.get_stock("Apples") == 20 else "FAIL")
    print("Test 2 - Apples Threshold:", "PASS" if manager.get_threshold("Apples") == 5 else "FAIL")
    print("Test 2 - Apples Freshness:", "PASS" if manager.get_freshness("Apples") == "Crisp" else "FAIL")
    print("Test 2 - Apples Color:", "PASS" if manager.get_color("Apples") == "Red" else "FAIL")

    # Test 3: Retrieve non-existent item attributes
    print("Test 3 - Non-existent Stock:", "PASS" if manager.get_stock("Oranges") == -1 else "FAIL")
    print("Test 3 - Non-existent Threshold:", "PASS" if manager.get_threshold("Oranges") == -1 else "FAIL")
    print("Test 3 - Non-existent Freshness:", "PASS" if manager.get_freshness("Oranges") is None else "FAIL")
    print("Test 3 - Non-existent Color:", "PASS" if manager.get_color("Oranges") is None else "FAIL")

    # Test 4: Update an existing item with new attributes
    manager.add_item("Bananas", 5, 3, freshness="Less Fresh", color="Greenish")
    print("Test 4 - Updated Bananas Stock:", "PASS" if manager.get_stock("Bananas") == 5 else "FAIL")
    print("Test 4 - Updated Bananas Threshold:", "PASS" if manager.get_threshold("Bananas") == 3 else "FAIL")
    print("Test 4 - Updated Bananas Freshness:", "PASS" if manager.get_freshness("Bananas") == "Less Fresh" else "FAIL")
    print("Test 4 - Updated Bananas Color:", "PASS" if manager.get_color("Bananas") == "Greenish" else "FAIL")

    # Test 5: Large data insertion
    large_data_count = 5000
    for i in range(large_data_count):
        manager.add_item(f"Item_{i}", i, i//2, freshness=f"Fresh_{i}", color="Color_"+str(i%5))
    # Verify a sample from the large dataset
    sample_index = 4999
    sample_item = f"Item_{sample_index}"
    print("Test 5 - Large Data Stock:", "PASS" if manager.get_stock(sample_item) == sample_index else "FAIL")
    print("Test 5 - Large Data Threshold:", "PASS" if manager.get_threshold(sample_item) == sample_index//2 else "FAIL")
    print("Test 5 - Large Data Freshness:", "PASS" if manager.get_freshness(sample_item) == f"Fresh_{sample_index}" else "FAIL")
    print("Test 5 - Large Data Color:", "PASS" if manager.get_color(sample_item) == "Color_"+str(sample_index%5) else "FAIL")

if __name__ == "__main__":
    main()
