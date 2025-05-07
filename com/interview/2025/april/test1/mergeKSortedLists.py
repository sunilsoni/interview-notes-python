class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def mergeKSortedLists(lists):
    """
    Merges k sorted linked lists into a single sorted linked list
    Args:
        lists: List of head pointers to sorted linked lists
    Returns:
        Head of merged sorted linked list
    """
    # Input validation
    if not lists:
        return None
    if len(lists) == 1:
        return lists[0]

    # Approach 1: Using Divide and Conquer
    def mergeTwoLists(l1, l2):
        dummy = ListNode(0)
        current = dummy

        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next

        current.next = l1 if l1 else l2
        return dummy.next

    def mergeKListsHelper(lists, start, end):
        if start == end:
            return lists[start]
        if start + 1 == end:
            return mergeTwoLists(lists[start], lists[end])

        mid = (start + end) // 2
        left = mergeKListsHelper(lists, start, mid)
        right = mergeKListsHelper(lists, mid + 1, end)
        return mergeTwoLists(left, right)

    return mergeKListsHelper(lists, 0, len(lists) - 1)


# Alternative Approach 2: Using Min Heap
from heapq import heappush, heappop


def mergeKSortedListsHeap(lists):
    """
    Merges k sorted linked lists using min heap
    """
    # Input validation
    if not lists:
        return None

    # Initialize min heap
    heap = []

    # Add first node from each list to heap
    for i, lst in enumerate(lists):
        if lst:
            heappush(heap, (lst.val, i, lst))

    dummy = ListNode(0)
    current = dummy

    # Process nodes from heap
    while heap:
        val, i, node = heappop(heap)
        current.next = node
        current = current.next

        if node.next:
            heappush(heap, (node.next.val, i, node.next))

    return dummy.next


# Test Helper Functions
def createList(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def printList(head):
    result = []
    current = head
    while current:
        result.append(str(current.val))
        current = current.next
    return ' -> '.join(result)


# Test Cases
def runTests():
    # Test case 1: Multiple lists of equal length
    lists1 = [
        createList([1, 4, 7]),
        createList([2, 5, 8]),
        createList([3, 6, 9])
    ]

    # Test case 2: Lists of different lengths
    lists2 = [
        createList([1, 3, 5, 7]),
        createList([2, 4]),
        createList([6, 8, 9])
    ]

    # Test case 3: Some empty lists
    lists3 = [
        createList([]),
        createList([1, 2, 3]),
        createList([]),
        createList([4, 5])
    ]

    # Run tests for both approaches
    test_cases = [lists1, lists2, lists3]

    for i, lists in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print("Input lists:")
        for lst in lists:
            print(printList(lst) if lst else "Empty")

        # Test Divide and Conquer approach
        result1 = mergeKSortedLists(lists)
        print("\nDivide and Conquer Result:")
        print(printList(result1))

        # Test Heap approach
        result2 = mergeKSortedListsHeap(lists)
        print("\nHeap Approach Result:")
        print(printList(result2))


if __name__ == "__main__":
    runTests()
