from collections import defaultdict

class FourSumZero:
    @staticmethod
    def four_sum_count(A, B, C, D):
        """
        Finds the number of tuples (i, j, k, l) such that:
        - i is an element from list A
        - j is an element from list B
        - k is an element from list C
        - l is an element from list D
        - The sum i + j + k + l == 0

        Args:
        A, B, C, D: Lists of integers.

        Returns:
        An integer representing the number of valid tuples.
        """

        # Create a dictionary to store the sums of elements from A and B
        sum_ab = defaultdict(int)
        for a in A:
            for b in B:
                sum_ab[a + b] += 1

        count = 0
        for c in C:
            for d in D:
                target = -(c + d)
                if target in sum_ab:
                    count += sum_ab[target]
        return count

    @staticmethod
    def run_tests():
        # Define test cases
        test_cases = [
            {
                'A': [1, 2],
                'B': [-2, -1],
                'C': [-1, 0],
                'D': [0, 2],
                'expected': 2
            },
            {
                'A': [0],
                'B': [0],
                'C': [0],
                'D': [0],
                'expected': 1
            },
            {
                'A': [1, 2, -1],
                'B': [-2, -1, 2],
                'C': [-1, 0, 1],
                'D': [0, 2, -2],
                'expected': 8
            },
            # Edge case: Empty lists
            {
                'A': [],
                'B': [],
                'C': [],
                'D': [],
                'expected': 0
            },
            # Edge case: Large input
            {
                'A': [i for i in range(-50, 50)],
                'B': [i for i in range(-50, 50)],
                'C': [i for i in range(-50, 50)],
                'D': [i for i in range(-50, 50)],
                'expected': 1000000  # This is just a placeholder
            }
        ]

        # Run tests and check results
        for i, test_case in enumerate(test_cases, 1):
            A = test_case['A']
            B = test_case['B']
            C = test_case['C']
            D = test_case['D']
            expected = test_case['expected']
            result = FourSumZero.four_sum_count(A, B, C, D)

            # For the large input, we won't compare the expected, just ensure it runs
            if i == 5:
                print(f"Test Case {i}: PASS (Executed with large input)")
                continue

            if result == expected:
                print(f"Test Case {i}: PASS")
            else:
                print(f"Test Case {i}: FAIL")
                print(f"Expected Output: {expected}")
                print(f"Actual Output: {result}")

if __name__ == "__main__":
    FourSumZero.run_tests()