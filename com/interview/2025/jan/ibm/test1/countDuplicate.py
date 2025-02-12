"""### Refined Combined Text:

---
WORKING:
### Problem Description

Given an integer array, `numbers`, count the number of elements that occur more than once.

---

### Example

#### Input:
```
numbers = [1, 3, 3, 4, 4, 4]
```

#### Output:
```
2
```

#### Explanation:
- The non-unique elements are `3` and `4`.
- Therefore, the answer is `2`.

---

### Function Description

Complete the function `countDuplicate` in the editor below:

#### Function Signature:
```python
def countDuplicate(numbers):
```

#### Parameters:
- `int numbers[n]`: An array of integers.

#### Returns:
- `int`: An integer that denotes the number of non-unique values in the `numbers` array.

---

### Constraints
- \(1 \leq \text{numbers}[i] \leq 1000\), \(0 \leq i < n\)

---

### Input Format for Custom Testing
1. The first line contains an integer `n`, the size of the `numbers` array.
2. Each of the next `n` lines contains an integer, `numbers[i]`.

---

### Sample Cases:

#### Case 0:
**Input:**
```
8
1
3
1
4
5
6
3
2
```

**Output:**
```
2
```

**Explanation:**
- The values `1` and `3` occur more than once.
- Therefore, the answer is `2`.

---

#### Case 1:
**Input:**
```
6
1
1
2
2
2
3
```

**Output:**
```
2
```

**Explanation:**
- The values `1` and `2` occur more than once.
- Therefore, the answer is `2`."""


def countDuplicate(numbers):
    # Create a dictionary to store frequency of each number
    freq = {}
    for num in numbers:
        freq[num] = freq.get(num, 0) + 1

    # Count numbers that appear more than once
    duplicate_count = sum(1 for count in freq.values() if count > 1)

    return duplicate_count


def test_countDuplicate():
    # Test cases structure: (input_array, expected_output, test_description)
    test_cases = [
        ([1, 3, 1, 4, 5, 6, 3, 2], 2, "Sample Case 0"),
        ([1, 1, 2, 2, 2, 3], 2, "Sample Case 1"),
        ([1, 3, 3, 4, 4, 4], 2, "Example Case"),
        ([1, 2, 3, 4, 5], 0, "No duplicates"),
        ([1, 1, 1, 1, 1], 1, "All same numbers"),
        ([1] * 1000, 1, "Large input - same number"),
        (list(range(1, 1001)), 0, "Large input - unique numbers")
    ]

    for i, (input_arr, expected, description) in enumerate(test_cases, 1):
        result = countDuplicate(input_arr)
        status = "PASS" if result == expected else "FAIL"
        print(f"\nTest #{i} ({description}): {status}")
        print(f"Input: {input_arr[:10]}{'...' if len(input_arr) > 10 else ''}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")


def main():
    print("Starting countDuplicate function tests...\n")
    test_countDuplicate()
    print("\nTesting completed.")


if __name__ == "__main__":
    main()
