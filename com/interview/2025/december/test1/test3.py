from itertools import permutations


def solve(left_words, target):
    """
    Solve any cryptarithmetic puzzle.

    Examples:
        solve(["VADA", "PAV"], "TIKKI")
        solve(["SEND", "MORE"], "MONEY")
        solve(["FISH", "CURRY"], "FUNNY")
    """

    # Step 1: Find all unique letters
    letters = set()
    for word in left_words:
        for char in word:
            letters.add(char)
    for char in target:
        letters.add(char)

    letters = list(letters)
    print(f"Puzzle: {' + '.join(left_words)} = {target}")
    print(f"Letters: {letters} ({len(letters)} unique)")

    # Check if solvable
    if len(letters) > 10:
        print("ERROR: More than 10 letters - impossible!")
        return None

    # Step 2: Find first letters (cannot be 0)
    first_letters = set()
    for word in left_words:
        first_letters.add(word[0])
    first_letters.add(target[0])
    print(f"Cannot be zero: {first_letters}")

    # Step 3: Try all permutations
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    count = 0

    for perm in permutations(digits, len(letters)):
        count += 1

        # Create mapping: letter -> digit
        mapping = {}
        for i in range(len(letters)):
            mapping[letters[i]] = perm[i]

        # Skip if first letter is 0
        skip = False
        for letter in first_letters:
            if mapping[letter] == 0:
                skip = True
                break
        if skip:
            continue

        # Convert word to number
        def to_number(word):
            num = 0
            for char in word:
                num = num * 10 + mapping[char]
            return num

        # Calculate left side sum
        left_sum = 0
        for word in left_words:
            left_sum += to_number(word)

        # Calculate right side
        right_num = to_number(target)

        # Check if equal
        if left_sum == right_num:
            print(f"\nSOLUTION FOUND! (iteration {count})")
            print(f"Mapping: {mapping}")

            # Show numbers
            nums = []
            for word in left_words:
                n = to_number(word)
                nums.append(n)
                print(f"  {word} = {n}")

            print(f"  {target} = {right_num}")
            print(f"  Check: {' + '.join(map(str, nums))} = {sum(nums)}")

            return mapping

    print(f"\nNo solution found after {count} iterations")
    return None


# ============================================
# TEST ALL EXAMPLES FROM THE PROBLEM
# ============================================

print("=" * 50)
solve(["VADA", "PAV"], "TIKKI")

print("\n" + "=" * 50)
solve(["FISH", "CURRY"], "FUNNY")

print("\n" + "=" * 50)
solve(["THIS", "IS", "TOO"], "BEER")

print("\n" + "=" * 50)
solve(["SEND", "MORE"], "MONEY")