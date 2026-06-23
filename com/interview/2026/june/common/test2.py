class Solution(object):  # Define the Solution class, same format as LeetCode expects.

    def groupAnagrams(self, strs):  # Define the method that receives the list of strings.
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """

        groups = {}  # Create a dictionary to store anagram groups.

        for word in strs:  # Go through each word one by one.
            sorted_word = ''.join(sorted(word))  # Sort characters and join them to create the common key.

            if sorted_word not in groups:  # Check if this anagram key is not already present.
                groups[sorted_word] = []  # Create a new empty list for this anagram group.

            groups[sorted_word].append(word)  # Add the original word into the correct anagram group.

        return list(groups.values())  # Return only the grouped anagram lists, not the dictionary keys.


def normalize(result):  # Helper method to compare groups without worrying about order.
    normalized_groups = []  # This list will store sorted versions of each group.

    for group in result:  # Go through every group in the result.
        normalized_groups.append(sorted(group))  # Sort words inside each group for easy comparison.

    return sorted(normalized_groups)  # Sort all groups so order does not affect PASS/FAIL.


def run_test(test_name, input_data, expected_output):  # Method to run one test case.
    solution = Solution()  # Create an object of the Solution class.

    actual_output = solution.groupAnagrams(input_data)  # Call the actual method with input data.

    actual_normalized = normalize(actual_output)  # Normalize actual output for fair comparison.

    expected_normalized = normalize(expected_output)  # Normalize expected output for fair comparison.

    if actual_normalized == expected_normalized:  # Compare both normalized outputs.
        print(test_name + ": PASS")  # Print PASS if output is correct.
    else:  # If output does not match.
        print(test_name + ": FAIL")  # Print FAIL if output is incorrect.
        print("Expected:", expected_output)  # Print expected output for debugging.
        print("Actual  :", actual_output)  # Print actual output for debugging.


def main():  # Main method to run all test cases.

    run_test(  # Run test case 1.
        "Test 1 - Example case",  # Test name.
        ["eat", "tea", "tan", "ate", "nat", "bat"],  # Input list.
        [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]  # Expected output.
    )

    run_test(  # Run test case 2.
        "Test 2 - Empty string",  # Test name.
        [""],  # Input contains one empty string.
        [[""]]  # Expected output has one group with empty string.
    )

    run_test(  # Run test case 3.
        "Test 3 - Single character",  # Test name.
        ["a"],  # Input contains one string.
        [["a"]]  # Expected output contains one group.
    )

    run_test(  # Run test case 4.
        "Test 4 - No anagrams",  # Test name.
        ["abc", "def", "ghi"],  # No words are anagrams.
        [["abc"], ["def"], ["ghi"]]  # Each word should be in its own group.
    )

    run_test(  # Run test case 5.
        "Test 5 - All are anagrams",  # Test name.
        ["abc", "bca", "cab"],  # All words are anagrams.
        [["abc", "bca", "cab"]]  # All should come in one group.
    )

    run_test(  # Run test case 6.
        "Test 6 - Duplicate words",  # Test name.
        ["eat", "eat", "tea"],  # Duplicate word and anagram.
        [["eat", "eat", "tea"]]  # All should come in same group.
    )

    large_input = ["abc"] * 5000 + ["def"] * 5000  # Create large input with 10,000 words.

    large_expected = [["abc"] * 5000, ["def"] * 5000]  # Expected two large groups.

    run_test(  # Run large data test.
        "Test 7 - Large input",  # Test name.
        large_input,  # Large input list.
        large_expected  # Expected large output.
    )


if __name__ == "__main__":  # This ensures main runs only when this file is executed directly.
    main()  # Call the main method.