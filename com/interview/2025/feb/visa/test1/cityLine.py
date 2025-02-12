"""WORKING 100%


## Problem Statement

You are tasked with analyzing the potential space in a cityscape outlined by a series of skyscrapers. Each skyscraper's height is represented by an element in the array `cityLine`, where the width of each skyscraper is consistently `1`, and they are placed directly adjacent to each other along a road with no gaps. Your mission is to determine the **largest square area** that can fit within this row of skyscrapers.

### Input/Output

- **Execution time limit**: 4 seconds (Python 3)
- **Memory limit**: 1 GB
- **Input**: `array.integer cityLine`
  - An array representing the heights of the skyscrapers. Each skyscraper has a width of `1`.
  - **Guaranteed constraints**:
    - \( 1 \leq cityLine.length \leq 10^6 \)
    - \( 1 \leq cityLine[i] \leq 10^6 \)

- **Output**: `integer64`
  - Return the **area** of the largest square that can fit within the skyscrapers along the road.

### Example 1

#### Input:
```plaintext
cityLine = [4, 3, 4]
```

#### Output:
```plaintext
solution(cityLine) = 9
```

#### Explanation:
- In this scenario, a **3×3** square can fit snugly within the skyscraper setup, taking advantage of the uniform heights at the edges.

---

### Example 2

#### Input:
```plaintext
cityLine = [1, 2, 3, 2, 1]
```

#### Output:
```plaintext
solution(cityLine) = 4
```

#### Explanation:
- In this configuration, there are several **2×2** squares that can be accommodated within the skyscrapers, but **no larger square** can fit due to the height limitations.

---

### Function Signature

```python
def solution(cityLine):
```

This function should compute the **largest square area** that can be formed given the heights of the skyscrapers.
"""
def solution(cityLine):
    """
    Computes the area of the largest square that can fit within the cityLine skyline.

    A square of side s can be placed if there is a contiguous segment of skyscrapers
    of length at least s, and every skyscraper in that segment has height at least s.

    This function uses a stack-based approach to compute, for each building,
    the maximum contiguous block (width) that has buildings of at least that building's height.
    Then, the candidate square side is the minimum of the building's height and the width.

    :param cityLine: List[int] - heights of the skyscrapers.
    :return: int - area of the largest square.
    """
    n = len(cityLine)
    if n == 0:
        return 0

    # Arrays to store the index of the nearest smaller building on the left and right
    left = [-1] * n
    right = [n] * n

    # Compute nearest smaller to the left for each building
    stack = []
    for i in range(n):
        while stack and cityLine[stack[-1]] >= cityLine[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    # Clear stack for computing nearest smaller to the right
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and cityLine[stack[-1]] >= cityLine[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)

    # Find the maximum square side length
    max_side = 0
    for i in range(n):
        # Width of contiguous block where every building has height >= cityLine[i]
        width = right[i] - left[i] - 1
        # Maximum square side using building i as the limiting height
        side = min(cityLine[i], width)
        max_side = max(max_side, side)

    return max_side * max_side  # area = side^2


# --- Simple Testing Harness in main() ---

def main():
    # List of test cases; each test case is a tuple (input, expected_output)
    test_cases = [
        # Provided examples
        ([4, 3, 4], 9),
        ([1, 2, 3, 2, 1], 4),
        # Edge case: single element
        ([5], 25),
        # All same heights; the best square side is min(height, number of buildings)
        ([3, 3, 3, 3], 9),  # contiguous block of 4 buildings, but height 3 limits the square side to 3
        # Increasing sequence
        ([1, 2, 3, 4, 5], 9),  # best is 3x3 (even though last building has height 5, contiguous segment is limited)
        # Decreasing sequence
        ([5, 4, 3, 2, 1], 9),  # similarly, best square is 3x3
    ]

    all_passed = True
    for idx, (cityLine, expected) in enumerate(test_cases):
        result = solution(cityLine)
        if result == expected:
            print(f"Test case {idx + 1} PASSED: solution({cityLine}) = {result}")
        else:
            print(f"Test case {idx + 1} FAILED: solution({cityLine}) = {result}, expected {expected}")
            all_passed = False

    # Large data test: create a large input (e.g., 1e6 elements)
    # For instance, a repeating pattern that should not break performance.
    import random
    random.seed(42)
    large_input = [random.randint(1, 10 ** 6) for _ in
                   range(10 ** 5)]  # using 10^5 for demonstration; can increase to 10^6 if needed
    # We don't have an "expected" value for this random test, but we check that it runs quickly.
    try:
        _ = solution(large_input)
        print("Large input test PASSED: processed large input successfully.")
    except Exception as e:
        print(f"Large input test FAILED: encountered an error: {e}")
        all_passed = False

    if all_passed:
        print("All tests passed successfully!")
    else:
        print("Some tests failed.")


if __name__ == "__main__":
    main()