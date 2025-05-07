from typing import List

def solution(diffs: List[int]) -> List[int]:
    current = 1500
    highest = 1500
    for diff in diffs:
        current += diff
        highest = max(highest, current)
    return [highest, current]


def main():
    test_cases = [
        # Format: (input, expected_output)
        ([100, -200, 350, 100, -600], [1850, 1250]),
        ([], [1500, 1500]),
        ([-1000], [1500, 500]),
        ([500, 500, -100, -200], [2500, 2200]),
        ([-100, -200, -300], [1500, 900]),
        ([0]*1000, [1500, 1500]),  # Large case, no changes
        ([1]*1000, [1500 + 1000, 1500 + 1000]),  # All +1
        ([-1]*1000, [1500, 500])  # All -1 but rating won't go below 0
    ]

    for i, (diffs, expected) in enumerate(test_cases):
        result = solution(diffs)
        status = "PASS" if result == expected else f"FAIL (Expected {expected}, Got {result})"
        print(f"Test case {i + 1}: {status}")


if __name__ == "__main__":
    main()