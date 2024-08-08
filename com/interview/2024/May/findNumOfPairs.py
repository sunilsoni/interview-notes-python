def findNumOfPairs(a, b):
    a.sort()
    b.sort()
    pairs = 0
    j = 0
    for i in range(len(a)):
        while j < len(b) and a[i] >= b[j]:
            j += 1
        if j == len(b):
            break
        pairs += 1
        j += 1
    return pairs


# Test
print(findNumOfPairs([2, 3, 3], [3, 4, 5]))
