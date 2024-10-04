'''

There is a string of length N made only of letters "a". Whenever there are two identical adjacent letters (e.g. "aa"), they can be transformed into a single letter that is the next letter of the alphabet. For example, "aa" can be transformed into "b" and "ee" into "f".
". However, "zz" cannot be further
transformed.
What is the alphabetically largest string that can be obtained from the initial string?
Write a function:
def solution(N)
that, given an integer N, returns the alphabetically largest string that can be obtained after such transformations.
Examples:
1. Given N = 11, the function should return "dba". The initial string
"aaaaaaaaaaa" can be transformed in the following manner: "aaaaaaaaaaa" →
"bbbbba" → "ccba" → "dba".
2. Given N = 1, the function should return "a".
". The initial string "a" cannot be
transformed in any way.
3. Given N = 67108876, the function should return "zzdc".
Write an efficient algorithm for the following assumptions:
• N is an integer within the range [1.1,000,000,000].

'''


class Solution:
    def solution(self, N: int) -> str:
        counts = [0] * 26  # counts for letters 'a' to 'z'
        counts[0] = N  # Start with N 'a's

        # Perform transformations from 'a' to 'y'
        for i in range(25):
            counts[i + 1] += counts[i] // 2  # Transform pairs to the next letter
            counts[i] %= 2  # Keep the remainder

        # Handle 'z's (we can only have up to 25 'z's)
        counts[25] %= 26

        # Build the result string from 'z' to 'a'
        result = []
        for i in range(25, -1, -1):
            result.extend([chr(ord('a') + i)] * counts[i])

        return ''.join(result)


# Test cases to check the solution
def test_solution():
    sol = Solution()

    # Test case 1
    result = sol.solution(11)
    print("Test Case 1: ", result == "dba", result)

    # Test case 2
    result = sol.solution(1)
    print("Test Case 2: ", result == "a", result)

    # Test case 3
    result = sol.solution(67108876)
    print("Test Case 3: ", result == "zzdc", result)


test_solution()
