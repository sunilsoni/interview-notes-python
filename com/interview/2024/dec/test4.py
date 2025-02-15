"""question2
You are given a strings and an integer k, a k duplicate removal consists of choosing k adjacent and equal letters from s and
removing them,
pausing the left and the right side of the deleted substring to concatenate together.
We repeatedly make k duplicate removals on s until we no longer can.
Return the final string after all such duplicate removals have been made. It is guaranteed that the answer is unique.
Casel:
Input: s = "deeedbbcccbdaa"
, k = 3
Output: "aa"Explanation: First delete "eee" and "ccc"
', get "ddbbbdaa"
Then delete "bbb", get "dddaa"
Finally delete "ddd"
, get "aa"
Case2: input: "azxxzy" k = 2
output: ay"""


class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        """
        Removes k adjacent duplicates in the string s repeatedly until no more can be removed.

        Parameters:
        s (str): The input string.
        k (int): The number of adjacent duplicates required for removal.

        Returns:
        str: The final string after all possible removals.
        """
        stack = []  # Each element is a [character, count] pair

        for char in s:
            if stack and stack[-1][0] == char:
                stack[-1][1] += 1  # Increment the count
                if stack[-1][1] == k:
                    stack.pop()  # Remove the sequence
            else:
                stack.append([char, 1])  # Start a new sequence

        # Reconstruct the final string
        result = ''.join(char * count for char, count in stack)
        return result


def main():
    """
    Main method to test the removeDuplicates function with various test cases.
    """
    test_cases = [
        # Provided test cases
        {"s": "deeedbbcccbdaa", "k": 3, "expected": "aa"},
        {"s": "azxxzy", "k": 2, "expected": "ay"},
        # Additional test cases
        {"s": "", "k": 2, "expected": ""},
        {"s": "a", "k": 1, "expected": ""},
        {"s": "aabbcc", "k": 2, "expected": ""},
        {"s": "aabbcc", "k": 3, "expected": "aabbcc"},
        {"s": "abcd", "k": 2, "expected": "abcd"},
        {"s": "pbbcggttciiippooaais", "k": 2, "expected": "ps"},
        # Edge cases
        {"s": "aaaaaaaaaa", "k": 2, "expected": ""},
        {"s": "a" * 100000, "k": 100000, "expected": ""},
        {"s": "a" * 99999 + "b", "k": 100000, "expected": "a" * 99999 + "b"},
    ]

    solution = Solution()
    passed = 0
    for idx, case in enumerate(test_cases, 1):
        s = case["s"]
        k = case["k"]
        expected = case["expected"]
        output = solution.removeDuplicates(s, k)
        if output == expected:
            print(f"Test Case {idx}: PASS")
            passed += 1
        else:
            print(f"Test Case {idx}: FAIL")
            print(f"  Input: s = {s[:50]}{'...' if len(s) > 50 else ''}, k = {k}")
            print(f"  Expected: {expected}")
            print(f"  Got: {output}")

    print(f"\nPassed {passed} out of {len(test_cases)} test cases.")


if __name__ == "__main__":
    main()
