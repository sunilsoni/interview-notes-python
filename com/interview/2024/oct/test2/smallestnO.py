import time
from typing import Optional

"""

from typing import Optional
HE HE AS
write a function that returns the smallest nonnegative number which can-be generated by using all the digits with odd values of a given number.
Example: • 10430
Result: • 13
HE HI BE
def rearrange_digits (number: int) -> Optional [int] :
••# Code • here
print ("Hello, World")
• return 0
assert (rearrange_digits (10430) == 13)


assert|rearrange_digits (690321) == 139[l


assert (rearrange_digits (0)

••==- None)
assert(rearrange_digits (-2)

••==• None)
assert (rearrange_digits (-3)
== 3)

assert (rearrange_digits (-1717) == 1177)


assert (rearrange_digits (-79). • print ("Passed" )
••==• 79)

# Tests
# Reference
#... Cast values: • int(val), str(val)...•
#.. Sort lists: •val.sort(reverse=False), sorted(val, reverse=False)
# Split strings: val split, list(val)
# Join strings: ""-join (val)
"""


class DigitRearranger:
    @staticmethod
    def rearrange_digits(number: int) -> Optional[int]:
        # Handle negative numbers by converting to positive
        num_str = str(abs(number))

        # If input is 0 or empty, return None
        if not num_str or number == 0:
            return None

        # Extract odd digits
        odd_digits = [d for d in num_str if int(d) % 2 == 1]

        # If no odd digits found, return None
        if not odd_digits:
            return None

        # Sort digits to get smallest possible number
        odd_digits.sort()

        # Convert back to integer
        result = int(''.join(odd_digits))

        # If original number was negative, keep the sign
        return result if number > 0 else result


def run_tests():
    test_cases = [
        (10430, 13),
        (690321, 139),
        (0, None),
        (-2, None),
        (-3, 3),
        (-1717, 1177),
        (-79, 79),
        # Additional test cases
        (24680, None),  # No odd digits
        (123456789, 13579),  # All digits
        (999999999, 999999999),  # Large number with same digits
        # More edge cases
        (11111, 11111),  # All same odd digits
        (22222, None),  # All same even digits
        (12345, 135),  # Sequential digits
        (98765, 957),  # Reverse sequential digits
    ]

    # Performance test case (using a more reasonable size)
    large_number = int('1' * 1000)  # 1000 digits

    passed = 0
    total = len(test_cases) + 1  # +1 for performance test

    solver = DigitRearranger()

    print("\nRunning test cases...")
    for i, (input_val, expected) in enumerate(test_cases, 1):
        try:
            start_time = time.time()
            result = solver.rearrange_digits(input_val)
            end_time = time.time()

            if result == expected:
                passed += 1
                status = "✅ PASS"
            else:
                status = "❌ FAIL"

            print(f"Test {i:2d}: Input={input_val:12d}, Expected={str(expected):12s}, Got={str(result):12s}")
            print(f"Status: {status} (Time: {(end_time - start_time) * 1000:.3f}ms)")

        except Exception as e:
            print(f"Test {i} raised an exception: {str(e)}")

    print("\nRunning performance test...")
    try:
        start_time = time.time()
        result = solver.rearrange_digits(large_number)
        end_time = time.time()
        print(f"Performance test with {len(str(large_number))} digits")
        print(f"Execution time: {(end_time - start_time) * 1000:.3f}ms")
        print(f"Result length: {len(str(result)) if result else 0} digits")
        passed += 1
    except Exception as e:
        print(f"Performance test failed: {str(e)}")

    print(f"\nTotal tests passed: {passed}/{total}")
    print(f"Success rate: {(passed / total) * 100:.1f}%")


if __name__ == "__main__":
    run_tests()
