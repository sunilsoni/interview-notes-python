##WORKING
def findNumOfPairs(a, b):
    # Sort both arrays
    a.sort()
    b.sort()

    # Initialize pointers and the count of pairs
    i, j = len(a) - 1, len(b) - 1
    count = 0

    # Use two pointers to find valid pairs
    while i >= 0 and j >= 0:
        if a[i] > b[j]:
            count += 1
            i -= 1
            j -= 1
        else:
            j -= 1

    return count


# Sample Input For Custom Testing
a = [1, 2, 3, 4, 5]
b = [6, 6, 1, 1, 1]
print(findNumOfPairs(a, b))  # Output: 3

a = [2, 3, 3]
b = [3, 4, 5]
print(findNumOfPairs(a, b))  # Output: 0
