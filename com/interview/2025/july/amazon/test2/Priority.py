# Definition of LinkedNode class to represent each node in the linked list
class LinkedNode:
    def __init__(self, value=0, nextNode=None):
        self.value = value  # Store the value of current node
        self.nextNode = nextNode  # Reference to the next node in list


def merge_sorted_lists(lists):
    """
    Merges N sorted linked lists into a single sorted linked list
    Args:
        lists: List of head nodes of sorted linked lists
    Returns:
        Head node of merged sorted linked list
    """
    # Handle edge cases: empty input or single list
    if not lists:
        return None
    if len(lists) == 1:
        return lists[0]

    # Initialize result as first list
    result = lists[0]

    # Iterate through remaining lists and merge one by one
    for i in range(1, len(lists)):
        result = merge_two_lists(result, lists[i])

    return result


def merge_two_lists(l1, l2):
    """
    Helper function to merge two sorted linked lists
    Args:
        l1, l2: Head nodes of two sorted linked lists
    Returns:
        Head node of merged sorted linked list
    """
    # Create dummy node to handle edge cases
    dummy = LinkedNode(0)
    current = dummy

    # Compare nodes from both lists and merge in sorted order
    while l1 and l2:
        if l1.value <= l2.value:
            current.nextNode = l1
            l1 = l1.nextNode
        else:
            current.nextNode = l2
            l2 = l2.nextNode
        current = current.nextNode

    # Attach remaining nodes from either list
    current.nextNode = l1 if l1 else l2

    return dummy.nextNode


def create_linked_list(arr):
    """
    Helper function to create linked list from array
    """
    if not arr:
        return None
    head = LinkedNode(arr[0])
    current = head
    for value in arr[1:]:
        current.nextNode = LinkedNode(value)
        current = current.nextNode
    return head


def print_linked_list(head):
    """
    Helper function to print linked list
    """
    result = []
    current = head
    while current:
        result.append(current.value)
        current = current.nextNode
    return result


# Main testing function
def main():
    # Test Case 1: Basic merge of two lists
    test1_lists = [
        create_linked_list([1, 3, 5]),
        create_linked_list([2, 4, 6])
    ]
    expected1 = [1, 2, 3, 4, 5, 6]
    result1 = print_linked_list(merge_sorted_lists(test1_lists))
    print(f"Test 1: {'PASS' if result1 == expected1 else 'FAIL'}")
    print(f"Expected: {expected1}")
    print(f"Got: {result1}\n")

    # Test Case 2: Merge three lists
    test2_lists = [
        create_linked_list([1, 4, 7]),
        create_linked_list([2, 5, 8]),
        create_linked_list([3, 6, 9])
    ]
    expected2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    result2 = print_linked_list(merge_sorted_lists(test2_lists))
    print(f"Test 2: {'PASS' if result2 == expected2 else 'FAIL'}")
    print(f"Expected: {expected2}")
    print(f"Got: {result2}\n")

    # Test Case 3: Large data input
    large_list1 = create_linked_list(list(range(0, 1000, 2)))  # Even numbers
    large_list2 = create_linked_list(list(range(1, 1000, 2)))  # Odd numbers
    test3_lists = [large_list1, large_list2]
    result3 = print_linked_list(merge_sorted_lists(test3_lists))
    expected3 = list(range(1000))
    print(f"Test 3 (Large Data): {'PASS' if result3 == expected3 else 'FAIL'}")
    print(f"Length of merged list: {len(result3)}\n")


if __name__ == "__main__":
    main()
