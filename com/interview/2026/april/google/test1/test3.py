def get_deletion_order(S: str) -> list:
    # This list will store the EXACT order of indices we need to delete.
    # By knowing what to delete, we know the answers for all K without recalculating.
    deletion_order = []

    # We use a stack to keep track of the INDICES of the numbers we have seen.
    # Storing indices (0, 1, 2) is better than storing characters ('4', '9')
    # because it tells us exactly WHERE in the string the weak link is.
    stack = []

    # We calculate the total length of the sequence S.
    n = len(S)

    # We loop through the sequence exactly one time. This guarantees O(N) Time.
    for i in range(n):

        # We extract the current digit from the string using the index 'i'.
        current_digit = S[i]

        # We enter our "ruthless" while loop. We removed the "Safety Check"
        # because we are not targeting a specific K; we want to find all weak links.
        # Condition 1: 'stack' checks if the stack is not empty.
        # Condition 2: 'S[stack[-1]] < current_digit' checks if the last kept digit is smaller.
        while stack and S[stack[-1]] < current_digit:
            # We found a weak link! The previous digit is smaller than the new one.
            # We remove its index from the stack.
            popped_index = stack.pop()

            # We record this index in our deletion order. This is the first thing
            # we must delete to make the string smaller but as large as possible.
            deletion_order.append(popped_index)

        # After removing any weaker numbers, we add the current index to the stack.
        stack.append(i)

    # The string is completely processed, but we might still have numbers in the stack.
    # Because of our logic, any numbers left in the stack are perfectly descending (e.g., 9, 2).
    # To make the string smaller, we must delete the smallest remaining numbers at the end.
    while stack:
        # We pop the remaining indices one by one (this removes the right-most, smallest numbers first).
        popped_index = stack.pop()

        # We add them to the end of our deletion order list.
        deletion_order.append(popped_index)

    # We return the master list of deletions. We solved the logic for all K in one pass!
    return deletion_order


def generate_strings_from_order(S: str, deletion_order: list) -> dict:
    # THIS IS A HELPER FUNCTION FOR TESTING.
    # It proves our O(N) deletion logic creates the correct string for every K.

    # We create a dictionary to store the answers (e.g., {4: "4902", 3: "902"}).
    results = {}

    # We create a boolean list to track which characters are kept (True) and deleted (False).
    # Initially, all characters are kept.
    is_kept = [True] * len(S)

    # We start with K equal to the full length of the string.
    current_k = len(S)

    # The answer for the maximum K is just the original string.
    results[current_k] = S

    # We iterate through our step-by-step deletion order.
    for index_to_delete in deletion_order:

        # We mark the character at this specific index as False (deleted).
        is_kept[index_to_delete] = False

        # Since we deleted a character, our target length K decreases by 1.
        current_k -= 1

        # If K reaches 0, we have found all answers and can stop.
        if current_k == 0:
            break

        # We build the new string by only joining the characters that are still True.
        current_string = "".join(S[i] for i in range(len(S)) if is_kept[i])

        # We save this string in our dictionary under the current K value.
        results[current_k] = current_string

    # Return the dictionary containing all answers.
    return results


def main():
    print("--- Running Test Cases ---")

    # We will test your exact screenshot example: S = 4902
    test_string = "4902"

    # Expected results based exactly on your screenshot image
    expected_results = {
        4: "4902",
        3: "902",
        2: "92",
        1: "9"
    }

    # STEP 1: Run our O(N) algorithm to get the deletion order
    deletion_order = get_deletion_order(test_string)

    # STEP 2: Translate that deletion order into actual strings to verify
    actual_results = generate_strings_from_order(test_string, deletion_order)

    # STEP 3: Verify PASS/FAIL
    all_passed = True
    print(f"Testing S = {test_string}")
    for k in range(len(test_string), 0, -1):
        if actual_results[k] == expected_results[k]:
            print(f"PASS | K = {k} | Answer = {actual_results[k]}")
        else:
            print(f"FAIL | K = {k} | Expected = {expected_results[k]}, Got = {actual_results[k]}")
            all_passed = False

    print("\n--- Running Large Data Edge Case ---")

    # We create a massive string of 200,000 characters ("9876" repeated 50,000 times)
    large_string = "9876" * 50000

    try:
        # We run the algorithm on the massive string
        large_deletion_order = get_deletion_order(large_string)

        # If it returns a list equal to the length of the string, it successfully processed everything without crashing.
        if len(large_deletion_order) == len(large_string):
            print("PASS | Large Data Input handled successfully in O(N) time!")
        else:
            print("FAIL | Large Data Input did not process completely.")
    except Exception as e:
        print(f"FAIL | Large Data Input crashed with error: {e}")


if __name__ == "__main__":
    main()