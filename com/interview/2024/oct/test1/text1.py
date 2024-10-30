import re

class Solution:
    def solution(self, text):
        words = text.strip().split()
        vowel_set = set('aeiou')

        word_differences = []
        for word in words:
            vowel_count = sum(1 for char in word if char in vowel_set)
            consonant_count = sum(1 for char in word if char.isalpha() and char not in vowel_set)
            abs_difference = abs(vowel_count - consonant_count)
            word_differences.append((abs_difference, word))

        # Custom sort function to handle numerical sorting
        def sort_key(item):
            abs_diff, word = item
            # Extract numbers from the word for numerical sorting
            numbers = re.findall(r'\d+', word)
            num = int(numbers[0]) if numbers else None
            return (abs_diff, num if num is not None else word, word)

        # Sort the list based on absolute difference and then numerically/alphabetically
        word_differences.sort(key=sort_key)

        sorted_words = [word for _, word in word_differences]
        return sorted_words


def run_tests():
    """
    Runs a series of test cases to verify the correctness of the solution method.
    Outputs 'PASS' if the test case passes, and 'FAIL' along with details if it fails.
    """
    solution_instance = Solution()
    test_cases = [
        # Test case 1: Example from the problem description
        ("penelope lives in hawaii", ["in", "penelope", "lives", "hawaii"]),

        # Test case 2: Another example from the problem description
        ("aabb ccpp aaap a", ["aabb", "a", "aaap", "ccpp"]),

        # Test case 3: Words with same absolute difference and alphabetical sorting
        ("apple banana apricot", ["apple", "apricot", "banana"]),

        # Test case 4: All words with zero difference
        ("aeiou bcdfg", ["aeiou", "bcdfg"]),

        # Test case 5: Single word input
        ("education", ["education"]),

        # Test case 6: Words with maximum length and varying differences
        ("abcdefghij klmnopqrst uvwxyz", ["klmnopqrst", "abcdefghij", "uvwxyz"]),

        # Test case 7: Empty string (edge case)
        ("", []),

        # Test case 8: Words with no vowels
        ("rhythm myths", ["myths", "rhythm"]),

        # Test case 9: Words with no consonants
        ("aeiou aei", ["aei", "aeiou"]),

        # Test case 10: Large input data
        (" ".join(["word" + str(i) for i in range(1000)]), ["word" + str(i) for i in range(1000)]),
    ]

    all_passed = True

    for idx, (input_text, expected_output) in enumerate(test_cases):
        output = solution_instance.solution(input_text)
        if output == expected_output:
            print(f"Test case {idx + 1}: PASS")
        else:
            all_passed = False
            print(f"Test case {idx + 1}: FAIL")
            print(f"  Input text: '{input_text}'")
            print(f"  Expected output: {expected_output}")
            print(f"  Actual output:   {output}")

    if all_passed:
        print("\nAll test cases passed!")
    else:
        print("\nSome test cases failed.")

if __name__ == "__main__":
    run_tests()
