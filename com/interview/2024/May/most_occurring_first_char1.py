def most_occurring_first_char(word):
    if not word:
        return None, 0

    char_count = {}

    # Count occurrences of first characters
    for i, char in enumerate(word):
        if char not in char_count:
            char_count[char] = word.count(char)

    # Find the maximum count
    max_count = max(char_count.values())

    # Find characters with the maximum count
    most_frequent = [char for char, count in char_count.items() if count == max_count]

    # Return the earliest occurring character among the most frequent
    return min(most_frequent, key=word.index), max_count


def main():
    # Test cases
    test_cases = [
        "Mississippi",
        "aabbccddee",
        "abcdefg",
        "aaaaaa",
        "abcabcabc",
        "zzyyxxwwvvuu"
    ]

    for case in test_cases:
        result, count = most_occurring_first_char(case)
        print(f"Input: {case}")
        print(f"Output: {result} - {count}")
        print()


if __name__ == "__main__":
    main()
