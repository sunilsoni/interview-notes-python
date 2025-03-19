class PalindromeChecker:
    def is_palindrome_after_removal(self, s: str) -> bool:
        """
        Check if string can become palindrome by removing at most one character
        Time Complexity: O(n) where n is length of string
        Space Complexity: O(1) as we only use pointers
        """

        # Helper function to check if substring is palindrome
        def is_palindrome(left: int, right: int) -> bool:
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        # Initialize two pointers from ends
        left, right = 0, len(s) - 1

        # Check characters from both ends
        while left < right:
            # If characters don't match
            if s[left] != s[right]:
                # Try removing either left or right character
                # and check if remaining is palindrome
                return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)
            left += 1
            right -= 1

        # If we reach here, string is already palindrome
        return True


def run_tests():
    """
    Comprehensive test suite including edge cases and large inputs
    """
    checker = PalindromeChecker()

    # Test cases with expected results
    test_cases = [
        ("tacocats", True),  # Remove 's' to get 'tacocat'
        ("racercar", True),  # Already a palindrome
        ("abcba", True),  # Already a palindrome
        ("abcde", False),  # Can't make palindrome with one removal
        ("", True),  # Empty string is palindrome
        ("a", True),  # Single character is palindrome
        ("ab", True),  # Remove either character
        ("abc", False),  # Can't make palindrome
        ("abca", True),  # Remove 'c'
        # Large input test
        ("a" * 100000 + "b" + "a" * 100000, True)  # Large palindrome with one different char
    ]

    total_tests = len(test_cases)
    passed_tests = 0

    for i, (test_input, expected) in enumerate(test_cases, 1):
        try:
            start_time = time.time()
            result = checker.is_palindrome_after_removal(test_input)
            end_time = time.time()

            status = "PASS" if result == expected else "FAIL"
            if status == "PASS":
                passed_tests += 1

            print(f"Test {i}: {status}")
            print(f"Input: {test_input[:50]}... (len={len(test_input)})")
            print(f"Expected: {expected}, Got: {result}")
            print(f"Time: {(end_time - start_time) * 1000:.2f}ms\n")

        except Exception as e:
            print(f"Test {i} raised an exception: {str(e)}\n")

    # Print summary
    print(f"Summary:")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests / total_tests) * 100:.2f}%")


if __name__ == "__main__":
    import time

    run_tests()
