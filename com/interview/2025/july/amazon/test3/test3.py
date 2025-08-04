import re  # import regex module for parsing dice notation
import random  # import random module to simulate dice rolls

def parse_and_roll(notation):
    """
    Parse a dice notation string 'XdS±M' and return the roll result.
    """
    notation = notation.strip()  # Remove leading/trailing whitespace
    pattern = r'(\d+)[dD](\d+)([+-]\d+)?'  # Regex: XdS±M pattern
    match = re.fullmatch(pattern, notation)  # Full-match against entire string
    if not match:
        raise ValueError(f"Invalid notation: '{notation}'")  # Invalid format error

    num_dice = int(match.group(1))  # Number of dice to roll (X)
    sides = int(match.group(2))     # Number of sides per die (S)
    modifier = int(match.group(3)) if match.group(3) else 0  # Optional ±M

    total = 0  # Initialize sum of rolls
    for _ in range(num_dice):
        total += random.randint(1, sides)  # Roll each die and accumulate

    return total + modifier  # Return final result including modifier

def main():
    # Test cases: (notation, expected_validity)
    test_cases = [
        ("2d6", True),
        ("1d20+4", True),
        ("3D8-2", True),
        (" 4d4+2 ", True),
        ("d20", False),
        ("2d", False),
        ("abc", False),
        ("10000d6", True),
    ]

    for notation, expected in test_cases:
        try:
            result = parse_and_roll(notation)  # Attempt roll
            actual = True  # No exception -> valid
        except Exception as e:
            actual = False  # Exception -> invalid
            error = e

        # Report PASS/FAIL based on expectation
        if actual == expected:
            if actual:
                print(f"PASS: '{notation}' -> {result}")
            else:
                print(f"PASS: '{notation}' correctly raised error")
        else:
            if actual:
                print(f"FAIL: '{notation}' should be invalid but returned {result}")
            else:
                print(f"FAIL: '{notation}' should be valid but raised {error}")

if __name__ == "__main__":
    main()