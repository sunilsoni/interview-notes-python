def funcTwins(inputArr):
    frequency = {}
    for num in inputArr:
        frequency[num] = frequency.get(num, 0) + 1

    non_twins = [num for num, count in frequency.items() if count == 1]

    return min(non_twins) if non_twins else -1


# Simple testing function without unit test frameworks
def run_tests():
    tests = [
        {"input": [1, 1, 2, 3, 3, 4, 4], "expected": 2},
        {"input": [1, 1, 2, 2], "expected": -1},
        {"input": [], "expected": -1},
        {"input": [5], "expected": 5},
        {"input": [4, 4, 2, 2, 1], "expected": 1},
        # Large input test
        {"input": [i for i in range(1, 100001)] * 2 + [100001], "expected": 100001},
    ]

    for idx, test in enumerate(tests, 1):
        result = funcTwins(test["input"])
        status = "PASS" if result == test["expected"] else "FAIL"
        print(f"Test Case {idx}: Expected {test['expected']}, Got {result} - {status}")


if __name__ == "__main__":
    run_tests()
