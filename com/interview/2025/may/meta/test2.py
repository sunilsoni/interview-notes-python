from typing import Optional


def rearrange_digits(number: int) -> Optional[int]:
    """
    Return the smallest non‐negative integer formed by all the odd digits
    in `number`. If there are no odd digits, return None.
    """
    # 1. Work with absolute value so negatives are treated like positives
    abs_number = abs(number)

    # 2. Convert to string to iterate each digit
    digit_str = str(abs_number)

    # 3. Filter: keep only odd characters
    odd_digits = [ch for ch in digit_str if int(ch) % 2 == 1]

    # 4. If empty, no odd digits → can't form a number
    if not odd_digits:
        return None

    # 5. Sort ascending to get the smallest possible combination
    odd_digits.sort()

    # 6. Recombine and convert to int to drop any leading zeros
    result = int("".join(odd_digits))

    return result


def main():
    # Standard test cases
    test_cases = [
        (690321, 139),
        (10430,   13),
        (2024,   None),
        (0,      None),
        (-2,     None),
        (-3,      3),
        (-58,     5),
        (-79,    79),
        (-1717,1177),
    ]

    print("Running standard test cases:")
    for idx, (inp, expected) in enumerate(test_cases, 1):
        out = rearrange_digits(inp)
        status = "PASS" if out == expected else "FAIL"
        print(f"  Test {idx}: in={inp}, exp={expected}, got={out} → {status}")

    # Large-data test: 1,000-digit number made of odd digits '9','7','5','3','1'
    large_str = "97531" * 200  # 5 × 200 = 1,000 digits
    large_num = int(large_str)
    out = rearrange_digits(large_num)
    print("\nLarge-data test (1,000 digits):")
    if out is not None and len(str(out)) == len(large_str):
        print(f"  PASS – output length {len(str(out))}")
    else:
        print("  FAIL – incorrect or missing output")

if __name__ == "__main__":
    main()