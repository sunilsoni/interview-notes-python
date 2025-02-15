"""
WORKING:

We are in a flower garden. The garden is represented as a collection of flower names.

We are trying to keep similar flowers close together, and we want to see what the farthest apart pair of the same flower are. Write a function that takes in a garden and returns the longest distance between any two flowers of the same type. If no such distance exists, return -1.

### Example:
```
Garden:    | Ivy | Rue | Ivy | Yew | Rue | Dock | Iris | Rue | Lily |
Positions: |  0  |  1  |  2  |  3  |  4  |  5   |  6   |  7  |  8   |
```
The longest distance is between Rue (position 1 and position 7), resulting in distance 6.

### Test cases:

```python
garden_1 = ["Ivy", "Rue", "Ivy", "Yew", "Rue", "Dock", "Iris", "Rue", "Lily"]
garden_2 = ["Rose"]
garden_3 = ["Ivy", "Rue", "Yew", "Arum", "Dock", "Iris", "Lily", "Reed", "Rose"]
garden_4 = ["Sage", "Rose", "Sage", "Reed", "Sage", "Lily", "Sage", "Iris", "Dock", "Sage", "Yew", "Rue", "Ivy"]
garden_5 = ["Dock", "Arum", "Yew", "Rue", "Ivy", "Ivy", "Rue", "Yew", "Arum", "Dock", "Iris", "Lily", "Reed", "Rose", "Sage", "Dock"]
garden_6 = ["Rose", "Rose", "Rose", "Rose", "Rose", "Rose"]
garden_7 = ["Iris", "Iris"]

max_distance(garden_1) => 6
max_distance(garden_2) => -1
max_distance(garden_3) => -1
max_distance(garden_4) => 9
max_distance(garden_5) => 15
max_distance(garden_6) => 5
max_distance(garden_7) => 1
```

### Complexity variables:
- **n**: the number of elements in the input garden

```python
print("Hello, world!")
print("This is a fully functioning Python 3 environment.")
```
"""


# File: FlowerGarden.py

def max_distance(garden):
    """
    Given a list of flower names, return the maximum distance between two occurrences
    of the same flower. If no such pair exists, return -1.

    :param garden: List[str] - list representing the garden with flower names.
    :return: int - maximum index distance between two same flowers, or -1 if none exist.
    """
    # Dictionary to store flower: (first_index, last_index)
    positions = {}

    for index, flower in enumerate(garden):
        if flower in positions:
            # Update last occurrence
            positions[flower] = (positions[flower][0], index)
        else:
            # Record first and initial last occurrence (same as first)
            positions[flower] = (index, index)

    # Find maximum distance among flowers that appear more than once
    max_gap = -1
    for first, last in positions.values():
        if last > first:
            max_gap = max(max_gap, last - first)

    return max_gap


def main():
    # Provided test cases
    garden_1 = ["Ivy", "Rue", "Ivy", "Yew", "Rue", "Dock", "Iris", "Rue", "Lily"]
    garden_2 = ["Rose"]
    garden_3 = ["Ivy", "Rue", "Yew", "Arum", "Dock", "Iris", "Lily", "Reed", "Rose"]
    garden_4 = ["Sage", "Rose", "Sage", "Reed", "Sage", "Lily", "Sage", "Iris", "Dock", "Sage", "Yew", "Rue", "Ivy"]
    garden_5 = ["Dock", "Arum", "Yew", "Rue", "Ivy", "Ivy", "Rue", "Yew", "Arum", "Dock", "Iris", "Lily", "Reed",
                "Rose", "Sage", "Dock"]
    garden_6 = ["Rose", "Rose", "Rose", "Rose", "Rose", "Rose"]
    garden_7 = ["Iris", "Iris"]

    expected_results = {
        'garden_1': 6,
        'garden_2': -1,
        'garden_3': -1,
        'garden_4': 9,
        'garden_5': 15,
        'garden_6': 5,
        'garden_7': 1,
    }

    tests = [
        ('garden_1', garden_1),
        ('garden_2', garden_2),
        ('garden_3', garden_3),
        ('garden_4', garden_4),
        ('garden_5', garden_5),
        ('garden_6', garden_6),
        ('garden_7', garden_7),
    ]

    # Run provided tests
    all_passed = True
    for name, garden in tests:
        result = max_distance(garden)
        expected = expected_results[name]
        if result == expected:
            print(f"{name}: PASS (result: {result})")
        else:
            print(f"{name}: FAIL (result: {result}, expected: {expected})")
            all_passed = False

    # Additional edge case: empty garden
    empty_garden = []
    if max_distance(empty_garden) == -1:
        print("empty_garden: PASS")
    else:
        print("empty_garden: FAIL")
        all_passed = False

    # Additional test: large data input
    # Create a large garden with 1 million elements where one flower repeats at the beginning and the end.
    large_garden = ["FlowerA"] + ["FlowerB"] * 999998 + ["FlowerA"]
    # Expected distance: last index (1,000,000 - 1) - first index (0) = 999,999
    if max_distance(large_garden) == 999999:
        print("large_garden: PASS")
    else:
        print("large_garden: FAIL")
        all_passed = False

    if all_passed:
        print("All test cases passed!")
    else:
        print("Some test cases failed.")


if __name__ == '__main__':
    main()
