from collections import Counter
from typing import List, Tuple


class PopularItemsTracker:
    def __init__(self):
        # Initialize a Counter object to keep track of item purchase counts
        # Counter is more efficient than regular dict for counting operations
        self.item_counts = Counter()

        # Keep track of total number of purchases for statistics
        self.total_purchases = 0

    def record_purchase(self, customer_id: str, item_id: str) -> None:
        """
        Record a new purchase by incrementing the count for the item
        Parameters:
            customer_id (str): ID of the customer making purchase
            item_id (str): ID of the item being purchased
        """
        # Increment the count for this item by 1
        self.item_counts[item_id] += 1
        # Increment total purchase counter
        self.total_purchases += 1

    def get_top_k_items(self, k: int = 10) -> List[Tuple[str, int]]:
        """
        Get the top k most purchased items
        Parameters:
            k (int): Number of top items to return
        Returns:
            List of tuples containing (item_id, purchase_count)
        """
        # Return k items with highest counts using Counter's most_common method
        return self.item_counts.most_common(k)


def test_popular_items():
    """
    Test function to verify the PopularItemsTracker functionality
    Prints PASS/FAIL for each test case
    """
    print("\nRunning tests...")

    # Initialize tracker
    tracker = PopularItemsTracker()

    # Test Case 1: Single purchase
    print("\nTest Case 1: Single purchase")
    tracker.record_purchase("user1", "item1")
    result = tracker.get_top_k_items(1)
    expected = [("item1", 1)]
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    print("PASS" if result == expected else "FAIL")

    # Test Case 2: Multiple purchases of same item
    print("\nTest Case 2: Multiple purchases of same item")
    tracker = PopularItemsTracker()  # Reset tracker
    for i in range(3):
        tracker.record_purchase(f"user{i}", "item1")
    result = tracker.get_top_k_items(1)
    expected = [("item1", 3)]
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    print("PASS" if result == expected else "FAIL")

    # Test Case 3: Multiple items with different counts
    print("\nTest Case 3: Multiple items with different counts")
    tracker = PopularItemsTracker()  # Reset tracker
    purchase_data = [
        ("user1", "item1"),
        ("user2", "item1"),
        ("user3", "item2"),
        ("user4", "item3"),
        ("user5", "item3"),
    ]
    for customer_id, item_id in purchase_data:
        tracker.record_purchase(customer_id, item_id)

    result = tracker.get_top_k_items(3)
    expected = [("item1", 2), ("item3", 2), ("item2", 1)]
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    print("PASS" if result == expected else "FAIL")

    # Test Case 4: Large data input
    print("\nTest Case 4: Large data input (10000 purchases)")
    tracker = PopularItemsTracker()  # Reset tracker
    # Simulate 10000 purchases with 100 different items
    import random
    for i in range(10000):
        item_id = f"item{random.randint(1, 100)}"
        tracker.record_purchase(f"user{i}", item_id)

    result = tracker.get_top_k_items(5)
    print(f"Top 5 items from 10000 purchases: {result}")
    print("PASS" if len(result) == 5 and all(x[1] > 0 for x in result) else "FAIL")


if __name__ == "__main__":
    test_popula
