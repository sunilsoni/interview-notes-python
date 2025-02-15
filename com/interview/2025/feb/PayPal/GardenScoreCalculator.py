"""
### Garden Score Calculation

We are writing an application for calculating garden scores in this year’s garden contest. All gardens have a rectangular shape. Within a garden, all rows have the same number of cells.

This year’s committee decided to use the following criteria for scoring gardens:
- Identify the largest square block of the same flower.
- Add 1 point for every cell in that block.

#### Example:
```
Garden:
| Iris  | Iris  | Iris  | Iris  | Iris  | Iris  | Iris  |
| Iris  | Iris  | Rose  | Rose  | Rose  | Rose  | Lily  |
| Iris  | Iris  | Rose  | Rose  | Rose  | Rose  | Lily  |
| Iris  | Iris  | Rose  | Rose  | Rose  | Rose  | Lily  |
| Iris  | Iris  | Rose  | Rose  | Rose  | Rose  | Lily  |
| Iris  | Iris  | Sage  | Sage  | Sage  | Sage  | Lily  |
```
The largest square block of the same flower (Rose) has **16** cells, so the above garden’s score is **16**.

Write a function that accepts a garden and returns the total score.

---

### Test Cases

#### Gardens:
```python
garden_1 = [
    ["Iris", "Iris", "Iris", "Iris", "Iris", "Iris", "Iris"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Sage", "Sage", "Sage", "Sage", "Lily"]
]

garden_2 = [
    ["Larch", "Holly", "Holly", "Heath", "Holly", "Heath"],
    ["Heath", "Pansy", "Holly", "Pansy", "Aspen", "Aspen"],
    ["Pansy", "Pansy", "Larch", "Lilac", "Aspen", "Lilac"],
    ["Hazel", "Lilac", "Basil", "Lilac", "Lilac", "Larch"],
    ["Peony", "Hazel", "Basil", "Hazel", "Holly", "Basil"]
]

garden_3 = [
    ["Arum", "Dock", "Iris", "Lily", "Reed", "Rose", "Sage", "Woad"]
]

garden_4 = [
    ["Arum"],
    ["Dock"],
    ["Iris"],
    ["Lily"],
    ["Reed"],
    ["Rose"],
    ["Sage"],
    ["Woad"]
]

garden_5 = [["Peony"]]

garden_6 = [
    ["Ivy", "Rue", "Yew", "Arum", "Dock"],
    ["Iris", "Lily", "Reed", "Rose", "Sage"],
    ["Woad", "Aspen", "Basil", "Hazel", "Heath"],
    ["Holly", "Larch", "Lilac", "Pansy", "Peony"]
]

garden_7 = [
    ["Rose", "Rose", "Rose", "Rose", "Rose"],
    ["Rose", "Rose", "Rose", "Rose", "Rose"],
    ["Rose", "Rose", "Rose", "Rose", "Rose"],
    ["Rose", "Rose", "Rose", "Rose", "Rose"],
    ["Rose", "Rose", "Rose", "Rose", "Rose"]
]

garden_8 = [
    ["Iris", "Iris", "Iris"],
    ["Iris", "Iris", "Iris"],
    ["Iris", "Iris", "Rose"]
]

garden_9 = [
    ["Iris", "Iris", "Rose", "Rose", "Iris", "Iris", "Iris"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Sage", "Sage", "Sage", "Sage", "Lily"]
]

garden_10 = [
    ["Iris", "Iris", "Iris", "Iris", "Iris", "Iris"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
    ["Iris", "Iris", "Sage", "Sage", "Sage", "Sage", "Lily"]
]

garden_11 = [
    ["Iris", "Iris", "Iris"],
    ["Iris", "Iris", "Iris"],
    ["Lily", "Iris", "Iris"]
]
```

#### Expected Outputs:
```python
calc_score(garden_1)  => 16
calc_score(garden_2)  => 1
calc_score(garden_3)  => 1
calc_score(garden_4)  => 1
calc_score(garden_5)  => 1
calc_score(garden_6)  => 1
calc_score(garden_7)  => 25
calc_score(garden_8)  => 4
calc_score(garden_9)  => 16
calc_score(garden_10) => 16
calc_score(garden_11) => 4
```

---

### Complexity Variables:
- **r** - the number of rows in the input garden
- **c** - the number of columns in the input garden
"""


class GardenScoreCalculator:
    @staticmethod
    def calc_score(garden):
        """
        Calculate the garden score based on the largest square block of the same flower.
        The score is the number of cells in that square (side_length^2).

        Args:
            garden (List[List[str]]): A 2D list representing the garden.

        Returns:
            int: The score, i.e. the area of the largest square block with identical flowers.
        """
        if not garden or not garden[0]:
            return 0  # In case of an empty garden

        rows = len(garden)
        cols = len(garden[0])

        # Create a DP table with the same dimensions as the garden.
        # dp[i][j] will represent the side length of the largest square ending at (i, j)
        dp = [[0] * cols for _ in range(rows)]
        max_side = 0

        for i in range(rows):
            for j in range(cols):
                # For the first row or first column, the largest square is 1 if there is a flower.
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    # Only if the current cell's flower is the same as its top, left, and top-left neighbors,
                    # we can form a larger square. Otherwise, the largest square ending at (i,j) is 1.
                    if (garden[i][j] == garden[i - 1][j] and
                            garden[i][j] == garden[i][j - 1] and
                            garden[i][j] == garden[i - 1][j - 1]):
                        dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                    else:
                        dp[i][j] = 1
                # Update the maximum square side found so far.
                if dp[i][j] > max_side:
                    max_side = dp[i][j]

        # The score is the area (number of cells) of the largest square block.
        return max_side * max_side


def main():
    # Provided test cases:
    garden_1 = [
        ["Iris", "Iris", "Iris", "Iris", "Iris", "Iris", "Iris"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Sage", "Sage", "Sage", "Sage", "Lily"]
    ]

    garden_2 = [
        ["Larch", "Holly", "Holly", "Heath", "Holly", "Heath"],
        ["Heath", "Pansy", "Holly", "Pansy", "Aspen", "Aspen"],
        ["Pansy", "Pansy", "Larch", "Lilac", "Aspen", "Lilac"],
        ["Hazel", "Lilac", "Basil", "Lilac", "Lilac", "Larch"],
        ["Peony", "Hazel", "Basil", "Hazel", "Holly", "Basil"]
    ]

    garden_3 = [
        ["Arum", "Dock", "Iris", "Lily", "Reed", "Rose", "Sage", "Woad"]
    ]

    garden_4 = [
        ["Arum"],
        ["Dock"],
        ["Iris"],
        ["Lily"],
        ["Reed"],
        ["Rose"],
        ["Sage"],
        ["Woad"]
    ]

    garden_5 = [["Peony"]]

    garden_6 = [
        ["Ivy", "Rue", "Yew", "Arum", "Dock"],
        ["Iris", "Lily", "Reed", "Rose", "Sage"],
        ["Woad", "Aspen", "Basil", "Hazel", "Heath"],
        ["Holly", "Larch", "Lilac", "Pansy", "Peony"]
    ]

    garden_7 = [
        ["Rose", "Rose", "Rose", "Rose", "Rose"],
        ["Rose", "Rose", "Rose", "Rose", "Rose"],
        ["Rose", "Rose", "Rose", "Rose", "Rose"],
        ["Rose", "Rose", "Rose", "Rose", "Rose"],
        ["Rose", "Rose", "Rose", "Rose", "Rose"]
    ]

    garden_8 = [
        ["Iris", "Iris", "Iris"],
        ["Iris", "Iris", "Iris"],
        ["Iris", "Iris", "Rose"]
    ]

    garden_9 = [
        ["Iris", "Iris", "Rose", "Rose", "Iris", "Iris", "Iris"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Sage", "Sage", "Sage", "Sage", "Lily"]
    ]

    garden_10 = [
        ["Iris", "Iris", "Iris", "Iris", "Iris", "Iris"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Rose"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Rose", "Rose", "Rose", "Lily"],
        ["Iris", "Iris", "Sage", "Sage", "Sage", "Sage", "Lily"]
    ]

    garden_11 = [
        ["Iris", "Iris", "Iris"],
        ["Iris", "Iris", "Iris"],
        ["Lily", "Iris", "Iris"]
    ]

    # Mapping test cases to their expected outputs.
    test_cases = [
        ("garden_1", garden_1, 16),
        ("garden_2", garden_2, 1),
        ("garden_3", garden_3, 1),
        ("garden_4", garden_4, 1),
        ("garden_5", garden_5, 1),
        ("garden_6", garden_6, 1),
        ("garden_7", garden_7, 25),
        ("garden_8", garden_8, 4),
        ("garden_9", garden_9, 16),
        ("garden_10", garden_10, 16),
        ("garden_11", garden_11, 4)
    ]

    all_passed = True
    print("Running test cases...")
    for name, garden, expected in test_cases:
        result = GardenScoreCalculator.calc_score(garden)
        if result == expected:
            print(f"Test {name}: PASS (Expected: {expected}, Got: {result})")
        else:
            print(f"Test {name}: FAIL (Expected: {expected}, Got: {result})")
            all_passed = False

    # Additional testing: Large data input
    # Create a large garden where each cell is "Rose" to test performance.
    large_rows, large_cols = 1000, 1000
    large_garden = [["Rose"] * large_cols for _ in range(large_rows)]
    # The largest square is the entire garden.
    expected_large = large_rows * large_cols  # 1,000,000 cells
    result_large = GardenScoreCalculator.calc_score(large_garden)
    if result_large == expected_large:
        print(f"Large data test: PASS (Expected: {expected_large}, Got: {result_large})")
    else:
        print(f"Large data test: FAIL (Expected: {expected_large}, Got: {result_large})")
        all_passed = False

    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed.")


if __name__ == '__main__':
    main()
