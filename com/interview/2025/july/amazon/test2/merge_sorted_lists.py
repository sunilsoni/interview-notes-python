# Class to represent a node in the linked list
class ListNode:
    def __init__(self, val=0, next=None):
        # Store the value of current node
        self.val = val
        # Reference to the next node, defaults to None
        self.next = next


def merge_sorted_lists(list1, list2):
    # Create a dummy node to serve as the head of merged list
    # This simplifies handling the first node case
    dummy = ListNode(0)
    # Current pointer to build the merged list
    current = dummy

    # Continue while both lists have nodes to compare
    while list1 and list2:
        # Compare values from both lists
        if list1.val <= list2.val:
            # If list1 value is smaller, add it to merged list
            current.next = list1
            # Move list1 pointer forward
            list1 = list1.next
        else:
            # If list2 value is smaller, add it to merged list
            current.next = list2
            # Move list2 pointer forward
            list2 = list2.next
        # Move current pointer forward
        current = current.next

    # If list1 has remaining nodes, append them
    if list1:
        current.next = list1
    # If list2 has remaining nodes, append them
    if list2:
        current.next = list2

    # Return the merged list (skip the dummy node)
    return dummy.next


# Helper function to create linked list from array
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


# Helper function to convert linked list to array for testing
def linked_list_to_array(head):
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


# Main testing function
def main():
    # Test Case 1: Basic merge
    test1_list1 = create_linked_list([1, 3, 5])
    test1_list2 = create_linked_list([2, 4, 6])
    result1 = merge_sorted_lists(test1_list1, test1_list2)
    print("Test 1:", "PASS" if linked_list_to_array(result1) == [1, 2, 3, 4, 5, 6] else "FAIL")

    # Test Case 2: One empty list
    test2_list1 = create_linked_list([1, 2, 3])
    test2_list2 = create_linked_list([])
    result2 = merge_sorted_lists(test2_list1, test2_list2)
    print("Test 2:", "PASS" if linked_list_to_array(result2) == [1, 2, 3] else "FAIL")

    # Test Case 3: Lists with duplicate values
    test3_list1 = create_linked_list([1, 2, 2])
    test3_list2 = create_linked_list([1, 2, 3])
    result3 = merge_sorted_lists(test3_list1, test3_list2)
    print("Test 3:", "PASS" if linked_list_to_array(result3) == [1, 1, 2, 2, 2, 3] else "FAIL")

    # Test Case 4: Large lists
    large_list1 = create_linked_list(list(range(0, 1000, 2)))  # Even numbers
    large_list2 = create_linked_list(list(range(1, 1000, 2)))  # Odd numbers
    result4 = merge_sorted_lists(large_list1, large_list2)
    print("Test 4 (Large Lists):", "PASS" if len(linked_list_to_array(result4)) == 1000 else "FAIL")


if __name__ == "__main__":
    main()
