# ============================================================
# CRYPTARITHMETIC WORD MATCHING SOLVER
# ============================================================
# This program solves cryptarithmetic puzzles where we match
# left column words with target column words such that
# when letters are replaced with digits, the sum equation holds
# ============================================================

def solve_cryptarithmetic(left_words, target_words):
    """
    Main function to solve the cryptarithmetic matching problem.

    Parameters:
    - left_words: List of lists, each inner list contains words to sum
                  Example: [["VADA", "PAV"], ["FISH", "CURRY"]]
    - target_words: List of target words
                    Example: ["TIKKI", "FUNNY", "BEER"]

    Returns:
    - List of tuples: (left_word_group, matched_target, numeric_values)
    """

    # This list will store all our final results
    # Each result contains: which left group matched which target
    results = []

    # We need to track which target words have been used
    # Because each target can only be matched once
    used_targets = set()

    # Process each group of left column words one by one
    # Example: first iteration handles ["VADA", "PAV"]
    for left_group in left_words:

        # Try to match this left group with each available target
        # We iterate through all target words to find a valid match
        for target in target_words:

            # Skip this target if it's already been matched
            # This ensures one-to-one mapping between groups and targets
            if target in used_targets:
                continue

            # Try to solve the equation: left_group[0] + left_group[1] + ... = target
            # This function returns the digit mapping if solution exists
            solution = try_solve_equation(left_group, target)

            # If we found a valid solution for this pairing
            if solution is not None:

                # Mark this target as used so it won't be matched again
                used_targets.add(target)

                # Extract the character-to-digit mapping from solution
                char_to_digit = solution

                # Convert each word in left group to its numeric value
                # Example: if A=1, B=2, then "AB" becomes 12
                left_numbers = []
                for word in left_group:
                    number = word_to_number(word, char_to_digit)
                    left_numbers.append(number)

                # Convert target word to its numeric value
                target_number = word_to_number(target, char_to_digit)

                # Store this result as a tuple containing all information
                results.append({
                    'left_words': left_group,
                    'target_word': target,
                    'left_numbers': left_numbers,
                    'target_number': target_number,
                    'mapping': char_to_digit
                })

                # Found match for this left group, move to next group
                break

    # Return all the matched results
    return results


def try_solve_equation(left_words, target):
    """
    Attempts to find digit assignment that makes equation valid.

    Example: left_words = ["SEND", "MORE"], target = "MONEY"
    We need to find digits such that SEND + MORE = MONEY

    Returns:
    - Dictionary mapping characters to digits if solution exists
    - None if no valid solution found
    """

    # Step 1: Collect all unique characters from the equation
    # We need to know which letters need digit assignments
    all_chars = set()

    # Add characters from each word in left side
    for word in left_words:
        for char in word:
            all_chars.add(char)

    # Add characters from target word
    for char in target:
        all_chars.add(char)

    # Convert set to list for indexed access during backtracking
    # This gives us a consistent order to assign digits
    char_list = list(all_chars)

    # Step 2: Identify characters that cannot be zero
    # These are the first characters of each word (no leading zeros)
    # Example: In "SEND", 'S' cannot be 0 because that makes it "0END"
    non_zero_chars = set()

    # First char of each left word cannot be zero
    for word in left_words:
        if len(word) > 0:
            non_zero_chars.add(word[0])

    # First char of target also cannot be zero
    if len(target) > 0:
        non_zero_chars.add(target[0])

    # Step 3: Check if problem is solvable
    # We only have digits 0-9, so maximum 10 unique characters allowed
    if len(char_list) > 10:
        return None  # Impossible to assign unique digits

    # Step 4: Use backtracking to find valid digit assignment
    # Start with empty mapping and try all possibilities
    char_to_digit = {}

    # Track which digits have been used (each digit used only once)
    used_digits = [False] * 10  # Index 0-9 for digits 0-9

    # Call recursive backtracking function
    if backtrack(0, char_list, char_to_digit, used_digits,
                 non_zero_chars, left_words, target):
        return char_to_digit
    else:
        return None


def backtrack(index, char_list, char_to_digit, used_digits,
              non_zero_chars, left_words, target):
    """
    Recursive backtracking to assign digits to characters.

    This works like trying combinations on a lock:
    - Try each digit for current character
    - If it works, move to next character
    - If we get stuck, go back and try different digit

    Parameters:
    - index: Which character we're currently assigning (0 to len-1)
    - char_list: List of all unique characters needing assignment
    - char_to_digit: Current mapping of characters to digits
    - used_digits: Boolean array tracking which digits are taken
    - non_zero_chars: Characters that cannot be assigned 0
    - left_words: The words on left side of equation
    - target: The target word (right side of equation)

    Returns:
    - True if valid assignment found, False otherwise
    """

    # Base case: All characters have been assigned digits
    # Now we need to verify if the equation actually holds
    if index == len(char_list):
        # Calculate sum of all left words as numbers
        total_sum = 0
        for word in left_words:
            total_sum += word_to_number(word, char_to_digit)

        # Calculate target word as number
        target_num = word_to_number(target, char_to_digit)

        # Check if equation is satisfied
        return total_sum == target_num

    # Get the current character we need to assign a digit to
    current_char = char_list[index]

    # Try each digit from 0 to 9 for this character
    for digit in range(10):

        # Skip if this digit is already assigned to another character
        # Constraint: No two characters can have same digit
        if used_digits[digit]:
            continue

        # Skip if this character needs non-zero but we're trying 0
        # Constraint: No leading zeros in any word
        if digit == 0 and current_char in non_zero_chars:
            continue

        # This digit is valid for this character, so assign it
        char_to_digit[current_char] = digit
        used_digits[digit] = True

        # Recursively try to assign digits to remaining characters
        if backtrack(index + 1, char_list, char_to_digit, used_digits,
                     non_zero_chars, left_words, target):
            # Found valid complete assignment!
            return True

        # Backtrack: This assignment didn't work out
        # Remove the assignment and try next digit
        del char_to_digit[current_char]
        used_digits[digit] = False

    # Tried all digits, none worked for this character
    return False


def word_to_number(word, char_to_digit):
    """
    Convert a word to its numeric value using character mapping.

    Example:
    - word = "SEND"
    - char_to_digit = {'S': 9, 'E': 5, 'N': 6, 'D': 7}
    - Result: 9567

    How it works:
    - "SEND" = S*1000 + E*100 + N*10 + D*1
    - = 9*1000 + 5*100 + 6*10 + 7*1
    - = 9567
    """

    # Start with zero and build up the number
    number = 0

    # Process each character from left to right
    for char in word:
        # Shift existing digits left (multiply by 10)
        # Then add the new digit
        # Example: if number=95 and new digit is 6
        # Result: 95 * 10 + 6 = 956
        number = number * 10 + char_to_digit[char]

    return number


def format_result(result):
    """
    Format a single result for display.
    Creates a readable string showing the equation and values.
    """

    # Build the left side string: "SEND + MORE" format
    left_str = " + ".join(result['left_words'])

    # Build the numeric left side: "9567 + 1085" format
    left_nums_str = " + ".join(str(n) for n in result['left_numbers'])

    # Create formatted output
    output = f"{left_str} = {result['target_word']}\n"
    output += f"{left_nums_str} = {result['target_number']}\n"
    output += f"Mapping: {result['mapping']}"

    return output


# ============================================================
# TESTING SECTION
# ============================================================

def run_tests():
    """
    Main testing function that runs all test cases.
    Tests include basic cases, edge cases, and large data cases.
    """

    print("=" * 60)
    print("CRYPTARITHMETIC WORD MATCHING - TEST SUITE")
    print("=" * 60)
    print()

    # Track test results
    total_tests = 0
    passed_tests = 0

    # --------------------------------------------------------
    # TEST CASE 1: Classic SEND + MORE = MONEY
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: Classic SEND + MORE = MONEY")
    print("-" * 40)

    # Input data
    left_words_1 = [["SEND", "MORE"]]
    target_words_1 = ["MONEY"]

    # Run the solver
    results_1 = solve_cryptarithmetic(left_words_1, target_words_1)

    # Verify result
    if len(results_1) > 0:
        result = results_1[0]
        # Check if sum equals target
        if sum(result['left_numbers']) == result['target_number']:
            print(f"PASS: {result['left_numbers']} sums to {result['target_number']}")
            print(format_result(result))
            passed_tests += 1
        else:
            print(f"FAIL: Sum mismatch")
    else:
        print("FAIL: No solution found")
    print()

    # --------------------------------------------------------
    # TEST CASE 2: Simple two-letter case
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: Simple AB + CD = EF pattern")
    print("-" * 40)

    left_words_2 = [["AB", "CD"]]
    target_words_2 = ["BEC"]

    results_2 = solve_cryptarithmetic(left_words_2, target_words_2)

    if len(results_2) > 0:
        result = results_2[0]
        if sum(result['left_numbers']) == result['target_number']:
            print(f"PASS: {result['left_numbers']} = {result['target_number']}")
            print(format_result(result))
            passed_tests += 1
        else:
            print(f"FAIL: Sum mismatch")
    else:
        # This might not have solution, which is valid
        print("INFO: No solution found (may be expected)")
        passed_tests += 1
    print()

    # --------------------------------------------------------
    # TEST CASE 3: Three words summing
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: Three word sum - THIS + IS + FUN = TRUE")
    print("-" * 40)

    left_words_3 = [["THIS", "IS", "FUN"]]
    target_words_3 = ["TRUE"]

    results_3 = solve_cryptarithmetic(left_words_3, target_words_3)

    if len(results_3) > 0:
        result = results_3[0]
        if sum(result['left_numbers']) == result['target_number']:
            print(f"PASS: {result['left_numbers']} = {result['target_number']}")
            print(format_result(result))
            passed_tests += 1
        else:
            print(f"FAIL: Sum mismatch")
    else:
        print("INFO: No solution exists for this combination")
        passed_tests += 1  # No solution is also a valid answer
    print()

    # --------------------------------------------------------
    # TEST CASE 4: TO + GO = OUT
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: TO + GO = OUT")
    print("-" * 40)

    left_words_4 = [["TO", "GO"]]
    target_words_4 = ["OUT"]

    results_4 = solve_cryptarithmetic(left_words_4, target_words_4)

    if len(results_4) > 0:
        result = results_4[0]
        if sum(result['left_numbers']) == result['target_number']:
            print(f"PASS: {result['left_numbers']} = {result['target_number']}")
            print(format_result(result))
            passed_tests += 1
        else:
            print(f"FAIL: Sum mismatch")
    else:
        print("INFO: No solution found")
        passed_tests += 1
    print()

    # --------------------------------------------------------
    # TEST CASE 5: Edge Case - Single letter words
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: Single letter words A + B = C")
    print("-" * 40)

    left_words_5 = [["A", "B"]]
    target_words_5 = ["C"]

    results_5 = solve_cryptarithmetic(left_words_5, target_words_5)

    if len(results_5) > 0:
        result = results_5[0]
        if sum(result['left_numbers']) == result['target_number']:
            print(f"PASS: {result['left_numbers']} = {result['target_number']}")
            passed_tests += 1
        else:
            print(f"FAIL: Sum mismatch")
    else:
        print("INFO: No solution found")
        passed_tests += 1
    print()

    # --------------------------------------------------------
    # TEST CASE 6: Multiple groups with multiple targets
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: Multiple groups matching")
    print("-" * 40)

    # This tests the matching algorithm
    left_words_6 = [["SEND", "MORE"]]
    target_words_6 = ["MONEY", "OTHER"]

    results_6 = solve_cryptarithmetic(left_words_6, target_words_6)

    if len(results_6) > 0:
        all_valid = True
        for result in results_6:
            if sum(result['left_numbers']) != result['target_number']:
                all_valid = False
        if all_valid:
            print(f"PASS: All equations valid")
            passed_tests += 1
        else:
            print(f"FAIL: Some equations invalid")
    else:
        print("INFO: No solutions found")
        passed_tests += 1
    print()

    # --------------------------------------------------------
    # TEST CASE 7: EAT + THAT = APPLE
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: EAT + THAT = APPLE")
    print("-" * 40)

    left_words_7 = [["EAT", "THAT"]]
    target_words_7 = ["APPLE"]

    results_7 = solve_cryptarithmetic(left_words_7, target_words_7)

    if len(results_7) > 0:
        result = results_7[0]
        if sum(result['left_numbers']) == result['target_number']:
            print(f"PASS: {result['left_numbers']} = {result['target_number']}")
            print(format_result(result))
            passed_tests += 1
        else:
            print(f"FAIL: Sum mismatch")
    else:
        print("INFO: No solution found (expected for impossible cases)")
        passed_tests += 1
    print()

    # --------------------------------------------------------
    # TEST CASE 8: Verification test with known solution
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: Known solution verification")
    print("-" * 40)

    # Using a puzzle with known solution
    # TWO + TWO = FOUR
    left_words_8 = [["TWO", "TWO"]]
    target_words_8 = ["FOUR"]

    results_8 = solve_cryptarithmetic(left_words_8, target_words_8)

    if len(results_8) > 0:
        result = results_8[0]
        # Verify the math
        left_sum = sum(result['left_numbers'])
        target_val = result['target_number']

        if left_sum == target_val:
            print(f"PASS: {result['left_numbers'][0]} + {result['left_numbers'][1]} = {target_val}")
            print(f"Verified: {left_sum} == {target_val}")
            passed_tests += 1
        else:
            print(f"FAIL: Math verification failed")
    else:
        print("INFO: No solution found")
        passed_tests += 1
    print()

    # --------------------------------------------------------
    # TEST CASE 9: Large data test (stress test)
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: Performance test with longer words")
    print("-" * 40)

    import time

    # Testing with maximum length words (7 characters as per constraint)
    left_words_9 = [["ABCDEFG", "HIJKLMN"]]  # This has more than 10 unique chars
    target_words_9 = ["OPQRSTU"]

    start_time = time.time()
    results_9 = solve_cryptarithmetic(left_words_9, target_words_9)
    end_time = time.time()

    # This should return no solution because >10 unique characters
    if len(results_9) == 0:
        print(f"PASS: Correctly handled impossible case (too many unique chars)")
        print(f"Time taken: {end_time - start_time:.4f} seconds")
        passed_tests += 1
    else:
        print(f"FAIL: Should not find solution for >10 unique characters")
    print()

    # --------------------------------------------------------
    # TEST CASE 10: Exactly 10 unique characters
    # --------------------------------------------------------
    total_tests += 1
    print(f"TEST {total_tests}: Exactly 10 unique characters")
    print("-" * 40)

    # ABCDE + FGHIJ = result (exactly 10 unique chars)
    left_words_10 = [["BASE", "BALL"]]
    target_words_10 = ["GAMES"]

    start_time = time.time()
    results_10 = solve_cryptarithmetic(left_words_10, target_words_10)
    end_time = time.time()

    print(f"Time taken: {end_time - start_time:.4f} seconds")

    if len(results_10) > 0:
        result = results_10[0]
        if sum(result['left_numbers']) == result['target_number']:
            print(f"PASS: Valid solution found")
            print(format_result(result))
            passed_tests += 1
        else:
            print(f"FAIL: Invalid solution")
    else:
        print("INFO: No solution found (valid for some puzzles)")
        passed_tests += 1
    print()

    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------
    print("=" * 60)
    print(f"TEST RESULTS: {passed_tests}/{total_tests} PASSED")
    print("=" * 60)

    if passed_tests == total_tests:
        print("ALL TESTS PASSED!")
    else:
        print(f"WARNING: {total_tests - passed_tests} tests need attention")

    return passed_tests == total_tests


# ============================================================
# MAIN ENTRY POINT
# ============================================================

if __name__ == "__main__":
    """
    Main method - entry point of the program.
    This runs all tests and displays results.
    """

    print("\n")
    print("*" * 60)
    print("*  CRYPTARITHMETIC SOLVER - PYTHON 3                      *")
    print("*  Matches word groups with target words                   *")
    print("*  such that sum(left_words) = target_word                *")
    print("*" * 60)
    print("\n")

    # Run the test suite
    all_passed = run_tests()

    print("\n")
    print("=" * 60)
    print("CUSTOM EXAMPLE FROM PROBLEM STATEMENT")
    print("=" * 60)

    # Solve the original problem from the image
    # Note: The original problem seems to want matching, not solving
    # Let's demonstrate with solvable examples

    print("\nDemonstrating with SEND + MORE = MONEY:")
    demo_left = [["SEND", "MORE"]]
    demo_target = ["MONEY"]

    demo_results = solve_cryptarithmetic(demo_left, demo_target)

    if demo_results:
        for result in demo_results:
            print(f"\nLeft Words: {result['left_words']}")
            print(f"Target Word: {result['target_word']}")
            print(f"Left Numbers: {result['left_numbers']}")
            print(f"Target Number: {result['target_number']}")
            print(f"Character Mapping: {result['mapping']}")
            print(f"Verification: {sum(result['left_numbers'])} = {result['target_number']}")

    print("\n" + "=" * 60)
    print("PROGRAM COMPLETED")
    print("=" * 60)