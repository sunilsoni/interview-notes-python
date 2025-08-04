# Import required libraries
import random  # For generating random numbers for dice rolls
import re  # For regular expression pattern matching


def parse_dice_notation(dice_str):
    """
    Parses and evaluates a dice notation string (e.g., "3d6+2")

    Args:
        dice_str (str): A string in XdS±M format where:
            X = number of dice
            d = literal 'd' or 'D'
            S = number of sides on each die
            ±M = optional modifier (can be positive or negative)

    Returns:
        int: The total of all dice rolls plus modifier

    Raises:
        ValueError: If the input string format is invalid
    """

    # STEP 1: Input Normalization
    # Convert to lowercase and remove all whitespace to handle inputs like "3D6 + 2"
    # This makes the parsing more forgiving of different input styles
    dice_str = dice_str.lower().replace(" ", "")

    # STEP 2: Pattern Definition and Validation
    # Define regex pattern to match dice notation:
    # ^ - start of string
    # (\d+) - one or more digits (number of dice)
    # d - literal 'd'
    # (\d+) - one or more digits (number of sides)
    # ([-+]\d+)? - optional modifier (plus or minus followed by digits)
    # $ - end of string
    pattern = r'^(\d+)d(\d+)([-+]\d+)?$'

    # Try to match the pattern against our input string
    match = re.match(pattern, dice_str)
    if not match:
        raise ValueError(f"Invalid dice notation format: {dice_str}")

    # STEP 3: Extract Components
    # Convert matched strings to integers for calculation
    try:
        # Extract number of dice from first capture group
        num_dice = int(match.group(1))
        if num_dice <= 0:
            raise ValueError("Number of dice must be positive")

        # Extract number of sides from second capture group
        sides = int(match.group(2))
        if sides <= 0:
            raise ValueError("Number of sides must be positive")

        # Extract modifier from third capture group (if it exists)
        modifier = match.group(3)

        # Convert modifier to integer, default to 0 if no modifier
        mod_value = int(modifier) if modifier else 0

    except ValueError as e:
        raise ValueError(f"Error parsing numbers: {str(e)}")

    # STEP 4: Roll Dice and Calculate Result
    try:
        # Generate random rolls for each die
        rolls = []
        for _ in range(num_dice):
            roll = random.randint(1, sides)  # Generate number between 1 and number of sides
            rolls.append(roll)

        # Calculate final result
        total = sum(rolls) + mod_value

        # Store roll details for debugging (optional)
        roll_details = {
            'individual_rolls': rolls,
            'modifier': mod_value,
            'total': total
        }

        return total

    except Exception as e:
        raise ValueError(f"Error during dice rolling: {str(e)}")


def test_dice_roller():
    """
    Comprehensive test function to verify dice roller functionality
    Tests various input formats and edge cases
    """
    # Test case structure: (input, expected_result_type)
    test_cases = [
        # Standard cases
        ("3d6+2", "valid"),  # Basic case with positive modifier
        ("1D20", "valid"),  # Upper case D
        ("2d6-1", "valid"),  # Negative modifier
        ("4d6", "valid"),  # No modifier
        ("1d100", "valid"),  # Large sided die

        # Edge cases
        ("d20", "invalid"),  # Missing number of dice
        ("2d", "invalid"),  # Missing sides
        ("2x6", "invalid"),  # Wrong separator
        ("0d6", "invalid"),  # Zero dice
        ("2d0", "invalid"),  # Zero sides
        ("abc", "invalid"),  # Complete nonsense
        ("2d6++", "invalid"),  # Invalid modifier
    ]

    print("Running Dice Notation Parser Tests\n")
    print("=" * 50)

    # Process each test case
    for test_input, expected_type in test_cases:
        print(f"\nTesting: {test_input}")
        print(f"Expected Type: {expected_type}")

        try:
            result = parse_dice_notation(test_input)
            if expected_type == "valid":
                print(f"✓ SUCCESS: Result = {result}")
            else:
                print(f"✗ FAIL: Should have raised error but got {result}")
        except ValueError as e:
            if expected_type == "invalid":
                print(f"✓ SUCCESS: Correctly caught invalid input")
            else:
                print(f"✗ FAIL: {str(e)}")

        print("-" * 30)


def example_usage():
    """
    Demonstrates typical usage of the dice roller with detailed output
    """
    print("\nDetailed Example Usage:")
    print("=" * 50)

    example = "3d6+2"
    print(f"Rolling: {example}")
    try:
        result = parse_dice_notation(example)
        print(f"Result: {result}")
        print("Note: Each roll will be different due to randomness")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Run tests and example
    test_dice_roller()
    example_usage()
