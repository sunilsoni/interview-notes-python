def findNumOfPairs2(a, b):
    a.sort()
    b.sort()
    count = 0
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            count += 1
            i += 1
            j += 1
        else:
            j += 1
    return count


# Sample Input
a = [1, 2, 3, 4, 5]
b = [6, 6, 1, 1, 1]


def findNumOfPairs2(a, b):
    a.sort()
    b.sort()
    count = 0
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            count += 1
            i += 1
        j += 1
    return count


# Sample Input
a = [1, 2, 3, 4, 5]
b = [6, 6, 1, 1, 1]


def findNumOfPairs(a, b):
    # Sort both lists for ordered comparison
    a.sort()
    b.sort()
    i, j = 0, 0
    count = 0
    while i < len(a) and j < len(b):
        # Increment j until we find a b[j] that a[i] can pair with
        while j < len(b) and a[i] <= b[j]:
            j += 1
        # If we find such a b[j], count the pair and move to next a[i]
        if j < len(b):
            count += 1
            j += 1  # Move to the next element in b
        i += 1  # Move to the next element in a
    return count


# Example usage
a = [1, 2, 3, 4, 5]
b = [6, 1, 1, 1, 1]
print(findNumOfPairs(a, b))  # Output should be 3

# Additional edge cases
print(findNumOfPairs([], []))  # Output: 0
print(findNumOfPairs([1, 2, 3], [4, 5, 6]))  # Output: 0
print(findNumOfPairs([4, 5, 6], [1, 2, 3]))  # Output: 3
print(findNumOfPairs([2, 2, 2], [2, 2, 2]))  # Output: 0

# Sample Output: 3
print(findNumOfPairs(a, b))

# Sample Output: 3
print(findNumOfPairs(a, b))
print(findNumOfPairs([2, 3, 3], [3, 4, 5]))
print(findNumOfPairs([3, 2, 3, 3], [3, 3, 4, 5]))
print(findNumOfPairs([5, 1, 2, 3, 4, 5], [5, 6, 6, 1, 1, 1]))
