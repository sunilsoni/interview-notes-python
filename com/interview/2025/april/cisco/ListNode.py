class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def mergeSortedLists(list1, list2):
    # Create dummy node to handle edge cases
    dummy = ListNode(0)
    current = dummy

    # Process while both lists have nodes
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    # Add remaining nodes if any
    if list1:
        current.next = list1
    if list2:
        current.next = list2

    return dummy.next


def createList(values):
    # Helper function to create linked list from array
    dummy = ListNode(0)
    current = dummy
    for val in values:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def printList(head):
    # Helper function to print linked list
    result = []
    while head:
        result.append(str(head.val))
        head = head.next
    return '->'.join(result)


# Test cases
def runTests():
    print("Running tests...")

    # Test Case 1: Basic even and odd numbers
    test1_list1 = createList([2, 4, 6, 8, 10])
    test1_list2 = createList([1, 3, 5, 7, 9])
    result1 = mergeSortedLists(test1_list1, test1_list2)
    print("Test 1:", printList(result1))
    expected1 = "1->2->3->4->5->6->7->8->9->10"
    print("PASS" if printList(result1) == expected1 else "FAIL")

    # Test Case 2: Empty lists
    test2_list1 = None
    test2_list2 = createList([1, 3, 5])
    result2 = mergeSortedLists(test2_list1, test2_list2)
    print("Test 2:", printList(result2))
    expected2 = "1->3->5"
    print("PASS" if printList(result2) == expected2 else "FAIL")

    # Test Case 3: Large numbers
    test3_list1 = createList([2, 4, 6, 8] * 1000)  # Large list
    test3_list2 = createList([1, 3, 5, 7] * 1000)  # Large list
    result3 = mergeSortedLists(test3_list1, test3_list2)
    print("Test 3: Large lists processed successfully")


if __name__ == "__main__":
    runTests()
