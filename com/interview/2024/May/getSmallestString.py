def getSmallestString(word, substr):
    n = len(word)
    m = len(substr)

    # Check all possible positions where `substr` can fit
    best_result = None
    for start in range(n - m + 1):
        # Try to fit `substr` starting at index `start`
        possible = True
        new_word = list(word)

        # Replace '?' in `word` to match `substr`
        for i in range(m):
            if new_word[start + i] == '?':
                new_word[start + i] = substr[i]
            elif new_word[start + i] != substr[i]:
                possible = False
                break

        if not possible:
            continue

        # Replace remaining '?' with 'a' to ensure lexicographical smallness
        new_word = ['a' if x == '?' else x for x in new_word]

        # Convert list back to string
        new_word = ''.join(new_word)

        # Update the best result if it's better than the current one
        if best_result is None or new_word < best_result:
            best_result = new_word

    return best_result if best_result is not None else "-1"


# Testing the function with examples
print(getSmallestString("s?f??d?j", "abc"))  # Expected Output: -1
print(getSmallestString("??c??er", "deciph"))  # Expected Output: decipher
print(getSmallestString("as?b?e?gf", "dbk"))  # Expected Output: asdbkeagf
