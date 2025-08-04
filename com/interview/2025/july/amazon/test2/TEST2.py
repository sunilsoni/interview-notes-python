class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def mergeKLists(lists):
    if not lists:
        return None

    # Divide and conquer approach
    def merge_lists(start, end):
        # Base case: if only one list, return it
        if start == end:
            return lists[start]

        # Base case: if two lists, merge them
        if start + 1 == end:
            return merge_two_lists(lists[start], lists[end])

        # Recursive case: divide lists into two halves
        mid = (start + end) // 2
        left = merge_lists(start, mid)
        right = merge_lists(mid + 1, end)

        # Merge the two halves
        return merge_two_lists(left, right)

    def merge_two_lists(l1, l2):
        # Handle edge cases
        if not l1: return l2
        if not l2: return l1

        # Create dummy node
        dummy = ListNode(0)
        current = dummy

        # Merge while both lists have elements
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next

        # Attach remaining elements
        current.next = l1 if l1 else l2

        return dummy.next

    # Start the divide and conquer process
    return merge_lists(0, len(lists) - 1)


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


# Helper function to convert linked list to array
def linked_list_to_array(head):
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


# Test the implementation
def test_merge_k_lists():
    # Example 1
    lists1 = [
        create_linked_list([1, 4, 7]),
        create_linked_list([2, 5, 8]),
        create_linked_list([3, 6, 9])
    ]
    result1 = mergeKLists(lists1)
    print("Example 1 Result:", linked_list_to_array(result1))

    # Example 2
    lists2 = [
        create_linked_list([1, 2]),
        create_linked_list([3, 4]),
        create_linked_list([5, 6]),
        create_linked_list([7, 8])
    ]
    result2 = mergeKLists(lists2)
    print("Example 2 Result:", linked_list_to_array(result2))


# Run the tests
test_merge_k_lists()
