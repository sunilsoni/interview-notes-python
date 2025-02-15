"""

WORKING


### Function Description

Complete the function `getOptimalPriority` in the editor below:

#### Function Signature:
```python
def getOptimalPriority(priority):
```

#### Parameters:
- `int priority[n]`: The priority sequence of the tasks.

#### Returns:
- `int[]`: The lexicographically smallest possible priority sequence after making any number of valid operations (including zero).

---

### Constraints
- \(1 \leq n \leq 2 \times 10^5\)
- \(0 \leq \text{priority}[i] \leq 9\)

---

### Input Format for Custom Testing
1. The first line contains an integer `n`, the size of the array `priority`.
2. Each of the next `n` lines contains an integer `priority[i]`.

---

### Sample Cases:

#### Case 0:
**Input:**
```
4
0
7
0
9
```

**Output:**
```
[0, 0, 7, 9]
```

**Explanation:**
An optimal sequence of swaps is as follows:
- **Before Swapping**: [0, 7, 0, 9]
- **After Swapping**: [0, 0, 7, 9]

---

#### Case 1:
**Input:**
```
5
9
4
8
6
3
```

**Output:**
```
[4, 8, 6, 9, 3]
```

**Explanation:**
An optimal sequence of swaps is as follows:
- **Before Swapping**: [9, 4, 8, 6, 3]
- **After Swapping**: [4, 9, 8, 6, 3]
- **After Swapping**: [4, 8, 9, 6, 3]
- **After Swapping**: [4, 8, 6, 9, 3]

The lexicographically smallest possible priority sequence is `[4, 8, 6, 9, 3]`.

"""


class GetOptimalPrioritySolution:

    def getOptimalPriority(self, priority):
        """
        Returns the lexicographically smallest possible priority sequence
        after making any number of valid swaps (each swap must be between
        one CPU-bound task (odd) and one I/O-bound task (even) if they are adjacent).

        Strategy (in simple terms):
          1) Collect all even numbers in the order they appear.
          2) Collect all odd numbers in the order they appear.
          3) Merge these two lists in a lexicographically minimal way
             while preserving each sub-list’s internal order.
        """
        # Separate evens and odds in their original order
        evens = []
        odds = []
        for x in priority:
            if x % 2 == 0:
                evens.append(x)
            else:
                odds.append(x)

        # Merge evens and odds to form the lexicographically smallest sequence
        result = []
        i, j = 0, 0
        while i < len(evens) and j < len(odds):
            # If the next numbers differ, choose the smaller
            if evens[i] < odds[j]:
                result.append(evens[i])
                i += 1
            elif evens[i] > odds[j]:
                result.append(odds[j])
                j += 1
            else:
                # Tie-breaking if evens[i] == odds[j]
                # Compare the remaining subsequences lexicographically
                # Convert slices to tuples for comparison
                remain_evens = tuple(evens[i:])
                remain_odds = tuple(odds[j:])
                if remain_evens < remain_odds:
                    result.append(evens[i])
                    i += 1
                else:
                    result.append(odds[j])
                    j += 1

        # Append whatever is left
        while i < len(evens):
            result.append(evens[i])
            i += 1
        while j < len(odds):
            result.append(odds[j])
            j += 1

        return result

    def main(self):
        """
        Simple main method to demonstrate the solution with test cases.
        We compare the output of getOptimalPriority with expected results
        and print PASS/FAIL accordingly. Also includes a large data test
        to check performance.
        """

        def test_case(case_name, priority, expected):
            output = self.getOptimalPriority(priority)
            print(case_name + ":", "PASS" if output == expected else f"FAIL (got {output}, expected {expected})")

        # Sample Case 0
        # n=4, priority=[0, 7, 0, 9], expected=[0, 0, 7, 9]
        test_case(
            "Sample Case 0",
            [0, 7, 0, 9],
            [0, 0, 7, 9]
        )

        # Sample Case 1
        # n=5, priority=[9, 4, 8, 6, 3], expected=[4, 8, 6, 9, 3]
        test_case(
            "Sample Case 1",
            [9, 4, 8, 6, 3],
            [4, 8, 6, 9, 3]
        )

        # Example from prompt (another example):
        # n=6, priority=[2,4,6,4,3,2] -> final is [2,3,4,6,4,2] in the prompt
        test_case(
            "Example from prompt",
            [2, 4, 6, 4, 3, 2],
            [2, 3, 4, 6, 4, 2]
        )

        # Edge Case: All evens -> no swaps possible
        # final must remain unchanged
        test_case(
            "All Evens",
            [2, 4, 6, 8],
            [2, 4, 6, 8]
        )

        # Edge Case: All odds -> no swaps possible
        # final must remain unchanged
        test_case(
            "All Odds",
            [9, 7, 5],
            [9, 7, 5]
        )

        # Edge Case: Single element
        test_case(
            "Single Element",
            [4],
            [4]
        )

        # Additional check with repeated values
        # We want to ensure tie-breaking is correct
        test_case(
            "Tie-Break Case",
            [2, 2, 3, 3, 2],
            # Evens=[2,2,2], Odds=[3,3]
            # Merging: compare 2<3 => pick 2
            # compare 2<3 => pick 2
            # compare 2<3 => pick 2
            # now only odds left => pick 3,3
            [2, 2, 2, 3, 3]
        )

        # Large Data Test
        import random
        random.seed(0)
        large_n = 10 ** 5
        large_priority = [random.randint(0, 9) for _ in range(large_n)]
        # Just run to ensure no timeout/error. We won't check exact final result here.
        _ = self.getOptimalPriority(large_priority)
        print("Large Data Test: PASS (completed without error)")


if __name__ == '__main__':
    GetOptimalPrioritySolution().main()
