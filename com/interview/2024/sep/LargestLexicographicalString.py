class LargestLexicographicalString:

    @staticmethod
    def solution(N):
        """
        This method returns the largest lexicographical string that can be generated
        from a string of length N consisting entirely of 'a's, after performing the
        allowed transformations.
        """
        # Step 1: Calculate how many 'z's can be formed
        result = []

        # Number of 'z's we can form
        z_count = N // 26
        remainder = N % 26

        # Append 'z' z_count times
        result.extend(['z'] * z_count)

        # Step 2: Handle the remainder which is less than 26
        if remainder > 0:
            result.append(chr(ord('a') + remainder - 1))

        # Return the result as a string
        return ''.join(result)

    @staticmethod
    def run_tests():
        """
        This method runs predefined test cases to validate the solution.
        """
        # List of test cases as tuples (input, expected_output)
        test_cases = [
            (11, "dba"),
            (1, "a"),
            (67108876, "zzdc")
        ]

        # Running the test cases
        for i, (input_value, expected_output) in enumerate(test_cases):
            output = LargestLexicographicalString.solution(input_value)
            if output == expected_output:
                print(f"Test case {i + 1} with input {input_value} passed.")
            else:
                print(
                    f"Test case {i + 1} with input {input_value} failed. Expected: {expected_output} but got: {output}")


# Main method to execute tests
if __name__ == "__main__":
    LargestLexicographicalString.run_tests()
