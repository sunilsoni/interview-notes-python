class Inventory:
    def __init__(self):
        # Dictionary to hold item names and their stock levels
        self.items = {}

    def add_item(self, name, stock):
        """Add a new item or update existing item's stock level."""
        self.items[name] = stock

    def get_stock(self, name):
        """Retrieve current stock level for the given item name."""
        return self.items.get(name, None)


def run_tests():
    # Initialize inventory
    inventory = Inventory()

    # Test case results
    results = []

    # Test 1: Add and retrieve a single item
    inventory.add_item("Laptop", 50)
    results.append(inventory.get_stock("Laptop") == 50)

    # Test 2: Retrieve non-existent item
    results.append(inventory.get_stock("Smartphone") is None)

    # Test 3: Update existing item
    inventory.add_item("Laptop", 75)
    results.append(inventory.get_stock("Laptop") == 75)

    # Test 4: Add multiple items and retrieve
    inventory.add_item("Tablet", 30)
    inventory.add_item("Monitor", 20)
    results.append(inventory.get_stock("Tablet") == 30)
    results.append(inventory.get_stock("Monitor") == 20)

    # Test 5: Large data input
    large_inventory = Inventory()
    for i in range(100000):  # Simulating large input
        large_inventory.add_item(f"Item{i}", i)
    pass_all_large = True
    for i in range(100000):
        if large_inventory.get_stock(f"Item{i}") != i:
            pass_all_large = False
            break
    results.append(pass_all_large)

    # Output test results
    all_passed = True
    for i, passed in enumerate(results, 1):
        print(f"Test {i}: {'PASS' if passed else 'FAIL'}")
        if not passed:
            all_passed = False

    print("All tests passed!" if all_passed else "Some tests failed.")


if __name__ == "__main__":
    run_tests()
