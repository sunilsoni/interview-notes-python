#!/usr/bin/env python3

class InventoryManager:
    """
    A simple inventory management system to add items with their stock levels and thresholds,
    and to retrieve their stock and threshold values.
    Items are stored in a dictionary with their stock levels and thresholds.
    """

    def __init__(self):
        # Initialize an empty dictionary to hold inventory items
        # Each key will map to a dictionary with keys 'stock' and 'threshold'
        self.items = {}

    def add_item(self, item_name, stock_level, threshold):
        """
        Adds a new item with a stock level and threshold to the inventory,
        or updates an existing item.
        :param item_name: Name of the item.
        :param stock_level: Current stock level (integer).
        :param threshold: Minimum desired stock level (integer).
        """
        # Validate negative stock level input
        if stock_level < 0:
            print(f"Warning: Attempted to add a negative stock level for '{item_name}'. Defaulting to 0.")
            stock_level = 0

        # Validate negative threshold input
        if threshold < 0:
            print(f"Warning: Attempted to set a negative threshold for '{item_name}'. Defaulting to 0.")
            threshold = 0

        # Store or update the item with both stock level and threshold
        self.items[item_name] = {'stock': stock_level, 'threshold': threshold}

    def get_stock(self, item_name):
        """
        Retrieves the current stock level for a given item.
        :param item_name: Name of the item.
        :return: Stock level (integer) or -1 if item does not exist.
        """
        # If item exists, return its stock; otherwise, -1
        return self.items[item_name]['stock'] if item_name in self.items else -1

    def get_threshold(self, item_name):
        """
        Retrieves the threshold for a given item.
        :param item_name: Name of the item.
        :return: Threshold (integer) or -1 if item does not exist.
        """
        # If item exists, return its threshold; otherwise, -1
        return self.items[item_name]['threshold'] if item_name in self.items else -1


def main():
    # Create an instance of InventoryManager
    manager = InventoryManager()

    # =======================
    # Test Cases
    # =======================

    # 1) Add a new item with threshold and check stock and threshold
    manager.add_item("Laptop", 50, 10)
    stock_result = manager.get_stock("Laptop")
    threshold_result = manager.get_threshold("Laptop")
    print("Test 1 - Add/Get Item with Threshold:",
          "PASS" if (stock_result == 50 and threshold_result == 10)
          else f"FAIL (Expected stock=50, threshold=10; got stock={stock_result}, threshold={threshold_result})")

    # 2) Add another item with zero stock and a threshold, then check
    manager.add_item("Mouse", 0, 5)
    stock_result = manager.get_stock("Mouse")
    threshold_result = manager.get_threshold("Mouse")
    print("Test 2 - Add/Get Zero Stock with Threshold:",
          "PASS" if (stock_result == 0 and threshold_result == 5)
          else f"FAIL (Expected stock=0, threshold=5; got stock={stock_result}, threshold={threshold_result})")

    # 3) Check an item that does not exist
    stock_result = manager.get_stock("Keyboard")
    threshold_result = manager.get_threshold("Keyboard")
    print("Test 3 - Get Non-existent Item:",
          "PASS" if (stock_result == -1 and threshold_result == -1)
          else f"FAIL (Expected stock=-1, threshold=-1; got stock={stock_result}, threshold={threshold_result})")

    # 4) Add an item with negative stock and threshold
    manager.add_item("Monitor", -5, -2)
    stock_result = manager.get_stock("Monitor")
    threshold_result = manager.get_threshold("Monitor")
    print("Test 4 - Add Item with Negative Stock and Threshold:",
          "PASS" if (stock_result == 0 and threshold_result == 0)
          else f"FAIL (Expected stock=0, threshold=0; got stock={stock_result}, threshold={threshold_result})")

    # 5) Update existing item stock and threshold
    manager.add_item("Laptop", 100, 20)  # Update "Laptop"
    stock_result = manager.get_stock("Laptop")
    threshold_result = manager.get_threshold("Laptop")
    print("Test 5 - Update Existing Item Stock and Threshold:",
          "PASS" if (stock_result == 100 and threshold_result == 20)
          else f"FAIL (Expected stock=100, threshold=20; got stock={stock_result}, threshold={threshold_result})")

    # 6) Large Data Test with threshold
    large_data_count = 10000  # Example size for large-scale testing
    for i in range(large_data_count):
        # Set arbitrary thresholds, e.g., half of the stock as threshold
        manager.add_item(f"Item_{i}", i, i // 2)
    # Check a random sample for correctness
    sample_item = f"Item_{9999}"
    stock_result = manager.get_stock(sample_item)
    threshold_result = manager.get_threshold(sample_item)
    print("Test 6 - Large Data Handling with Threshold:",
          "PASS" if (stock_result == 9999 and threshold_result == 9999 // 2)
          else f"FAIL (Expected stock=9999, threshold={9999 // 2}; got stock={stock_result}, threshold={threshold_result})")


if __name__ == "__main__":
    main()
