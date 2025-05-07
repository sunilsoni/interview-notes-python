def mergeLists_direct(list1, list2):
    # Handle empty lists
    if not list1: return list2
    if not list2: return list1

    # Initialize with smaller head
    if list1.val <= list2.val:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next

    current = head

    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next

    current.next = list1 if list1 else list2
    return head

# Example:
# list1: 2 -> 4 -> 6
# list2: 1 -> 3 -> 5
# Steps:
# 1. head = 1, current = 1
# 2. current.next = 2
# 3. current.next = 3
# Final: 1 -> 2 -> 3 -> 4 -> 5 -> 6
