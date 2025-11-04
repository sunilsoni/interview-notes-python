# Roman numeral converter with line-by-line comments for clarity and testing

def int_to_roman(num):
    # Validate input type and range first to ensure reliable behavior later
    # We require an integer between 1 and 3999 inclusive for classic Roman numerals
    if not isinstance(num, int):
        # If input is not integer, raise error so caller/test knows it's invalid
        raise ValueError("Input must be integer")
    # Check the allowed numeric range for standard Roman numerals
    if num <= 0 or num > 3999:
        # Raise error for out-of-range values to mark them invalid
        raise ValueError("Input must be in range 1..3999")

    # Thousands mapping: index 0 -> "", 1 -> "M", 2 -> "MM", 3 -> "MMM"
    # This covers values 0, 1000, 2000, 3000
    thousands = ["", "M", "MM", "MMM"]

    # Hundreds mapping handles 0..9 hundreds with subtractive forms included
    # Index 4 corresponds to 400 -> "CD", index 9 corresponds to 900 -> "CM"
    hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]

    # Tens mapping handles 0..9 tens with subtractive forms for 40 and 90
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]

    # Ones mapping handles 0..9 ones with subtractive forms for 4 and 9
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # Compute how many thousands are in the number (0..3)
    th = num // 1000
    # Compute hundreds digit (0..9) by removing thousands then integer div by 100
    hd = (num % 1000) // 100
    # Compute tens digit (0..9) by removing hundreds then integer div by 10
    td = (num % 100) // 10
    # Compute ones digit (0..9) by modulo 10
    od = num % 10

    # Build Roman numeral by concatenating mapped parts in descending order
    roman = thousands[th] + hundreds[hd] + tens[td] + ones[od]

    # Return the final Roman numeral string to the caller
    return roman


def run_tests():
    # Prepare explicit test cases from problem statement and more edge cases
    # Each test is (input, expected_output_or_None_if_error_expected)
    test_cases = [
        (14, "XIV"),            # Example: 14 -> XIV
        (79, "LXXIX"),          # Example: 79 -> LXXIX
        (225, "CCXXV"),         # Example: 225 -> CCXXV
        (845, "DCCCXLV"),       # Example: 845 -> DCCCXLV
        (2022, "MMXXII"),       # Example: 2022 -> MMXXII
        (1, "I"),               # Smallest valid number -> "I"
        (4, "IV"),              # Subtractive form for 4
        (9, "IX"),              # Subtractive form for 9
        (40, "XL"),             # Subtractive form for 40
        (90, "XC"),             # Subtractive form for 90
        (400, "CD"),            # Subtractive form for 400
        (900, "CM"),            # Subtractive form for 900
        (3999, "MMMCMXCIX"),    # Largest valid number under classic rules
        (0, None),              # Invalid: 0 -> expect error/None
        (-5, None),             # Invalid: negative -> expect error/None
        (4000, None),           # Invalid: >3999 -> expect error/None
        ("100", None),          # Invalid: non-integer string -> expect error/None
    ]

    # Tracker for overall pass count to summarize after tests
    passed = 0
    total = len(test_cases)

    # Run each test case and print PASS/FAIL and details for debugging
    for i, (inp, expected) in enumerate(test_cases, start=1):
        # For clarity, print which test we are executing
        try:
            # Try to get roman result for valid inputs
            result = int_to_roman(inp)
            # If expected is None but we got a result, that is a failure for this case
            if expected is None:
                # Print failure information when an error was expected but didn't happen
                print(f"Test {i}: FAIL - input={inp!r} expected error, got '{result}'")
            else:
                # Compare the expected output with actual result (case-sensitive)
                if result == expected:
                    # Test passed: result matches expected exactly
                    print(f"Test {i}: PASS - input={inp} => {result}")
                    passed += 1
                else:
                    # Test failed: show expected vs actual for debugging
                    print(f"Test {i}: FAIL - input={inp} expected '{expected}' got '{result}'")
        except Exception as e:
            # If an exception occurred, it is expected when expected is None
            if expected is None:
                # This is a pass because an error was expected for invalid input
                print(f"Test {i}: PASS (expected error) - input={inp!r} error='{e}'")
                passed += 1
            else:
                # Unexpected error for a case that should succeed -> fail and show exception
                print(f"Test {i}: FAIL - input={inp!r} unexpected error: {e}")

    # Print summary of the explicit tests
    print(f"\nSummary: {passed}/{total} tests passed.")

    # ---------- Large data performance / correctness check ----------
    # Now perform a larger batch conversion to ensure performance and correctness at scale
    # We'll convert the full valid range 1..3999 once and verify count and basic sanity
    try:
        # Prepare list of all valid inputs as a stress sanity test
        large_inputs = list(range(1, 4000))  # 3999 items total
        # Convert all numbers to Roman using list comprehension for speed and clarity
        large_outputs = [int_to_roman(x) for x in large_inputs]
        # Basic sanity checks: length must match and none of outputs should be empty
        if len(large_outputs) == len(large_inputs) and all(len(s) > 0 for s in large_outputs):
            # If checks pass, print PASS summary for the large input test
            print("Large data test: PASS - converted 1..3999 successfully.")
        else:
            # If any output is empty or counts mismatch, mark as fail
            print("Large data test: FAIL - mismatch or empty outputs detected.")
    except Exception as e:
        # If any unexpected exception happens during large run, print FAIL and exception
        print(f"Large data test: FAIL - exception occurred: {e}")

    # Optional: timed performance check to show how fast conversions happen (informational)
    import time  # import placed here because it's only needed for this timing block
    start = time.time()  # record start time
    # Perform the conversion many times to simulate heavier load; adjust multiplier if needed
    repeat = 10  # repeat 10 times converting 3999 numbers => ~39,990 conversions
    for _ in range(repeat):
        # convert full range; list comprehension keeps it fast
        _ = [int_to_roman(x) for x in large_inputs]
    elapsed = time.time() - start  # compute elapsed seconds
    # Print elapsed time so user can judge performance (no pass/fail, informational)
    print(f"Performance: {repeat * len(large_inputs)} conversions in {elapsed:.3f} seconds.")

# Entrypoint for script execution; runs tests when script is executed directly
if __name__ == "__main__":
    # Call run_tests to execute all checks and print results to console
    run_tests()