#!/usr/bin/env python3

class InventoryManager:
    """
    A simple inventory management system to add items, get stock levels,
    and store a threshold for minimum inventory.
    """

    def __init__(self):
        # Using a dictionary to hold each item and its attributes (stock, threshold).
        # Structure example:
        # self.items[item_name] = {
        #    "stock": current_stock,
        #    "threshold": threshold_value
        # }
        self.items = {}

    def add_item(self, item_name, stock_level, threshold=0):
        """
        Adds or updates an item in the inventory.

        :param item_name: Name of the item.
        :param stock_level: Current stock level (integer).
        :param threshold: Minimum desired stock level (integer).
        """
        if stock_level < 0:
            print(f"Warning: Attempted to add a negative stock level for '{item_name}'. Defaulting to 0.")
            stock_level = 0

        if threshold < 0:
            print(f"Warning: Threshold cannot be negative for '{item_name}'. Defaulting to 0.")
            threshold = 0

        self.items[item_name] = {
            "stock": stock_level,
            "threshold": threshold
        }

    def get_stock(self, item_name):
        """
        Retrieves the current stock level for a given item.

        :param item_name: Name of the item.
        :return: Stock level (integer) or -1 if the item does not exist.
        """
        item_data = self.items.get(item_name)
        if item_data is None:
            return -1
        return item_data["stock"]

    def get_threshold(self, item_name):
        """
        Retrieves the threshold for a given item.

        :param item_name: Name of the item.
        :return: Threshold level (integer) or -1 if the item does not exist.
        """
        item_data = self.items.get(item_name)
        if item_data is None:
            return -1
        return item_data["threshold"]

    def is_below_threshold(self, item_name):
        """
        Checks if an item's stock is below the threshold.

        :param item_name: Name of the item.
        :return: True if stock is below threshold, False otherwise.
                 Returns None if item does not exist.
        """
        item_data = self.items.get(item_name)
        if item_data is None:
            return None
        return item_data["stock"] < item_data["threshold"]


def main():
    manager = InventoryManager()

    # =============================================
    # Tests for threshold functionality
    # =============================================

    # 1) Add item with threshold
    manager.add_item("Laptop", 50, threshold=20)
    stock_result = manager.get_stock("Laptop")
    threshold_result = manager.get_threshold("Laptop")

    print("Test 1 - Add item with threshold:")
    print("  - Checking stock:", "PASS" if stock_result == 50 else f"FAIL (Expected 50, got {stock_result})")
    print("  - Checking threshold:",
          "PASS" if threshold_result == 20 else f"FAIL (Expected 20, got {threshold_result})")

    # 2) Check if stock is below threshold
    below = manager.is_below_threshold("Laptop")
    # 50 is NOT below 20, so it should be False
    print("Test 2 - Stock below threshold check:")
    print("  - is_below_threshold:", "PASS" if below is False else f"FAIL (Expected False, got {below})")

    # 3) Add item with negative threshold
    manager.add_item("Monitor", 10, threshold=-5)
    threshold_result = manager.get_threshold("Monitor")
    print("Test 3 - Negative threshold defaults to 0:")
    print("  - Checking threshold:", "PASS" if threshold_result == 0 else f"FAIL (Expected 0, got {threshold_result})")

    # 4) Update existing item and test again
    manager.add_item("Laptop", 10, threshold=15)  # Overwrite existing
    stock_result = manager.get_stock("Laptop")
    threshold_result = manager.get_threshold("Laptop")
    below = manager.is_below_threshold("Laptop")

    print("Test 4 - Update existing item (Laptop) with new stock and threshold:")
    print("  - Checking stock:", "PASS" if stock_result == 10 else f"FAIL (Expected 10, got {stock_result})")
    print("  - Checking threshold:",
          "PASS" if threshold_result == 15 else f"FAIL (Expected 15, got {threshold_result})")
    # Now the stock (10) is below threshold (15), so is_below_threshold should be True
    print("  - is_below_threshold:", "PASS" if below is True else f"FAIL (Expected True, got {below})")

    # 5) Add some large data, verifying threshold handling
    large_data_count = 1000
    for i in range(large_data_count):
        manager.add_item(f"Item_{i}", i, threshold=i // 2)

    # Check a specific item in the large dataset
    item_name = "Item_999"
    if manager.get_stock(item_name) == -1:
        print("Test 5 - Large data test: PASS (No out-of-range error, items 0-999 added)")
    else:
        # For "Item_999", we didn't add it because the loop runs until 999 inclusive?
        # Actually, i goes from 0 to 999, so "Item_999" should exist.
        # Let's also see if the threshold check is correct:
        is_below = manager.is_below_threshold(item_name)
        # stock = 999, threshold = 999//2 = 499, so not below threshold
        should_be_below = (999 < 499)  # which is False
        print("Test 5 - Large data test - existence check:",
              "PASS" if manager.get_stock(item_name) == 999 else "FAIL")
        print("Test 5 - Large data test - threshold check:",
              "PASS" if is_below == should_be_below else "FAIL")


if __name__ == "__main__":
    main()
