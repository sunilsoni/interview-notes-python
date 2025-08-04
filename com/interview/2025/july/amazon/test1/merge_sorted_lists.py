# Define the node class for a singly linked list
class ListNode:
    def __init__(self, value):                          # initialize a node with a value
        self.value = value                              # store the node's integer value
        self.next = None                                # initialize the next pointer to None

def merge_sorted_lists(l1, l2):
    """
    Merge two sorted linked lists l1 and l2 and return the head of the new sorted list.
    """
    dummy = ListNode(0)                                 # create a dummy head to simplify merges
    current = dummy                                     # current will build the merged list

    # Loop until one list runs out
    while l1 is not None and l2 is not None:
        if l1.value <= l2.value:                       # pick the smaller node
            current.next = l1                          # attach l1's node to merged list
            l1 = l1.next                               # advance pointer in list l1
        else:
            current.next = l2                          # attach l2's node if it's smaller
            l2 = l2.next                               # advance pointer in list l2
        current = current.next                         # advance merged-list pointer

    # At least one list is now empty; attach the rest of the other list
    if l1 is not None:
        current.next = l1                              # attach remaining nodes of l1
    else:
        current.next = l2                              # attach remaining nodes of l2

    return dummy.next                                   # skip dummy and return real head

def list_to_linked(arr):
    """
    Convert a Python list 'arr' to a linked list and return its head.
    """
    head = None                                         # start with empty list
    tail = None                                         # to keep track of last node
    for num in arr:
        node = ListNode(num)                            # create a new node for each element
        if head is None:
            head = node                                 # first node becomes head
            tail = node                                 # tail also points to it initially
        else:
            tail.next = node                            # append new node at the tail
            tail = node                                 # move tail pointer forward
    return head                                         # return the linked-list head

def linked_to_list(head):
    """
    Convert a linked list back to a Python list for easy comparison or display.
    """
    arr = []                                            # initialize empty Python list
    current = head                                     # start from the head of linked list
    while current is not None:
        arr.append(current.value)                      # collect each node's value
        current = current.next                         # move to the next node
    return arr                                         # return the collected list

if __name__ == "__main__":
    # --- Small test cases ---
    tests = [
        # (list A, list B, expected merged list)
        ([1, 3, 5],   [2, 4, 6],   [1, 2, 3, 4, 5, 6]),
        ([],          [1, 2, 3],   [1, 2, 3]),
        ([4, 5, 6],   [],          [4, 5, 6]),
        ([1, 1, 2],   [1, 3, 4],   [1, 1, 1, 2, 3, 4]),
    ]

    for i, (A, B, expected) in enumerate(tests, start=1):
        headA = list_to_linked(A)                      # build linked list A
        headB = list_to_linked(B)                      # build linked list B
        merged_head = merge_sorted_lists(headA, headB) # merge them
        result = linked_to_list(merged_head)           # convert result back to Python list

        if result == expected:
            print(f"Test {i}: PASS")                   # expected and actual match
        else:
            print(f"Test {i}: FAIL — expected {expected}, got {result}")

    # --- Large data performance test ---
    N = 10_000                                       # choose size for each list
    # generate [1, 2, ..., N]
    large_A = list(range(1, N + 1))
    # generate [N+1, N+2, ..., 2N]
    large_B = list(range(N + 1, 2 * N + 1))

    headA = list_to_linked(large_A)                   # build large linked list A
    headB = list_to_linked(large_B)                   # build large linked list B
    merged_head = merge_sorted_lists(headA, headB)     # merge them

    # Verify only length and boundary values to avoid huge output
    length = 0
    current = merged_head
    last_value = None

    while current is not None:
        length += 1                                   # count nodes
        last_value = current.value                    # remember last node's value
        current = current.next

    # Check that we got exactly 2N nodes and that the last value is 2N
    if length == 2 * N and last_value == 2 * N:
        print(f"Large test: PASS ({length} nodes, last={last_value})")
    else:
        print(f"Large test: FAIL (length={length}, last={last_value})")