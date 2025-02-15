import random
import unittest


class Solution:
    def solution(self, numbers, pivot):
        return [self.compare(num, pivot) for num in numbers]

    def compare(self, num, pivot):
        if num == 0:
            return 0
        elif (num > 0 and pivot > 0) or (num < 0 and pivot < 0):
            return 1
        else:
            return -1


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_case(self):
        numbers = [6, -5, 0]
        pivot = 2
        expected = [1, -1, 0]
        self.assertEqual(self.sol.solution(numbers, pivot), expected)

    def test_all_positive(self):
        numbers = [1, 2, 3, 4, 5]
        pivot = 1
        expected = [1, 1, 1, 1, 1]
        self.assertEqual(self.sol.solution(numbers, pivot), expected)

    def test_all_negative(self):
        numbers = [-1, -2, -3, -4, -5]
        pivot = -1
        expected = [1, 1, 1, 1, 1]
        self.assertEqual(self.sol.solution(numbers, pivot), expected)

    def test_mixed_signs(self):
        numbers = [-2, -1, 0, 1, 2]
        pivot = 1
        expected = [-1, -1, 0, 1, 1]
        self.assertEqual(self.sol.solution(numbers, pivot), expected)

    def test_large_input(self):
        numbers = [random.randint(-10 ** 9, 10 ** 9) for _ in range(1000)]
        pivot = random.randint(-10 ** 9, 10 ** 9)
        if pivot == 0:
            pivot = 1  # Ensure pivot is not zero
        result = self.sol.solution(numbers, pivot)
        self.assertEqual(len(result), 1000)
        for i, num in enumerate(numbers):
            if num == 0:
                self.assertEqual(result[i], 0)
            elif (num > 0 and pivot > 0) or (num < 0 and pivot < 0):
                self.assertEqual(result[i], 1)
            else:
                self.assertEqual(result[i], -1)

    def test_edge_cases(self):
        self.assertEqual(self.sol.solution([0], 1), [0])
        self.assertEqual(self.sol.solution([-10 ** 9], 10 ** 9), [-1])
        self.assertEqual(self.sol.solution([10 ** 9], -10 ** 9), [-1])


if __name__ == '__main__':
    unittest.main()
