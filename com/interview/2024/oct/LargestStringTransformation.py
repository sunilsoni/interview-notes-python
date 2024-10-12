class Solution:
    def solution(self, N: int) -> str:
        # Initialize counts for each letter from 'a' to 'z'
        counts = [0] * 26  # counts for letters 'a' to 'z'
        counts[0] = N  # Start with N 'a's
        print(f"Initial counts: {counts}")

        # Perform transformations from 'a' to 'y'
        for i in range(25):
            # Transform pairs of the current letter to the next letter
            counts[i + 1] += counts[i] // 2  # Move half of the current letter count to the next letter
            counts[i] %= 2  # Keep only the remainder (0 or 1) for the current letter
            print(f"After processing letter {chr(ord('a') + i)}: {counts}")

        # Handle 'z's (we can only have up to 25 'z's)
        counts[25] %= 26  # Ensure the count of 'z' does not exceed 25
        print(f"Final counts after handling 'z': {counts}")

        # Build the result string from 'z' to 'a'
        result = []
        for i in range(25, -1, -1):
            # Append the character 'a' + i, repeated counts[i] times
            result.extend([chr(ord('a') + i)] * counts[i])
            print(f"Building result: {result}")

        return ''.join(result)  # Join the list into a final string


# Test cases to check the solution
def test_solution():
    sol = Solution()

    # Test case 1
    result = sol.solution(11)
    print("Test Case 1: ", result == "dba", result)  # Expected output is "dba"

    # Test case 2
    result = sol.solution(1)
    print("Test Case 2: ", result == "a", result)  # Expected output is "a"

    # Test case 3
    result = sol.solution(67108876)
    print("Test Case 3: ", result == "zzdc", result)  # Expected output is "zzdc"

test_solution()