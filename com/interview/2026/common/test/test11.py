import sys


def is_valid_palindrome_one_deletion(s: str) -> bool:
    """
    Checks if 's' is a palindrome, allowing ONE character deletion.
    Handles middle characters by moving pointers inward.
    """

    # Logic: Start at the very ends.
    left = 0
    right = len(s) - 1

    # Logic: The loop moves us from the outside -> INWARD to the middle.
    while left < right:

        # Logic: Check the current pair.
        if s[left] != s[right]:
            # --- PROBLEM FOUND ---
            # It doesn't matter if this happens at the start or deep in the middle.
            # We are here now. We have two choices:

            # Choice A: Delete the character at 'left'
            # We skip 'left' by passing (left + 1) and 'right' to the helper.
            # Effectively checking: Is the string valid without s[left]?
            skip_left = check_rest_of_string(s, left + 1, right)

            # Choice B: Delete the character at 'right'
            # We skip 'right' by passing 'left' and (right - 1).
            # Effectively checking: Is the string valid without s[right]?
            skip_right = check_rest_of_string(s, left, right - 1)

            # Logic: If either choice works, we are good!
            return skip_left or skip_right

        # --- NO PROBLEM FOUND ---
        # Logic: If they match, we essentially "discard" these characters.
        # We move both pointers closer to the center.
        left += 1
        right -= 1

    # Logic: If we met in the middle without issues, it's a valid palindrome.
    return True


def check_rest_of_string(s, left, right):
    """
    Helper: Checks if the substring from 'left' to 'right' is a palindrome.
    This runs strict checks (no deletions allowed).
    """
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


# ---------------------------------------------------------
# Test Method
# ---------------------------------------------------------

def run_tests():
    print("--- Testing Middle Deletion Logic ---")

    # Example: "radkar" -> remove 'k' -> "radar" (Palindrome)
    # The mismatch happens at index 2 ('d') and index 3 ('k')
    input_str = "radkar"
    result = is_valid_palindrome_one_deletion(input_str)
    print(f"Input: {input_str} | Result: {result} (Expected: True)")

    # Example: "abca" -> remove 'c' -> "aba"
    input_str2 = "abca"
    result2 = is_valid_palindrome_one_deletion(input_str2)
    print(f"Input: {input_str2}   | Result: {result2} (Expected: True)")


if __name__ == "__main__":
    run_tests()