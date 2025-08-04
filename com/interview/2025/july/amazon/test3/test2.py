def roll_dice(dice_str):
    """
    Rolls dice and returns both individual rolls and total

    Args:
        dice_str (str): e.g., "2d6-2"

    Returns:
        tuple: (list of rolls, total)
    """
    # Clean input
    dice_str = dice_str.lower().replace(" ", "")

    # Parse components
    pattern = r'^(\d+)d(\d+)([-+]\d+)?$'
    match = re.match(pattern, dice_str)
    if not match:
        raise ValueError(f"Invalid dice notation: {dice_str}")

    # Extract values
    num_dice = int(match.group(1))
    sides = int(match.group(2))
    modifier = int(match.group(3) or 0)  # Default to 0 if no modifier

    # Roll the dice
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(rolls) + modifier

    # Return both rolls and total
    return rolls, total


# Example usage:
def demonstrate_rolls():
    test_cases = ["2d6-2", "3d6+1", "4d4"]

    for test in test_cases:
        rolls, total = roll_dice(test)
        print(f"\nRolling {test}:")
        print(f"Individual rolls: {rolls}")
        print(f"Total: {total}")


# Run demonstration
if __name__ == "__main__":
    demonstrate_rolls()
