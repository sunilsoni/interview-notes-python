def most_occurring_first_char(word):
    char_count = {}
    seen_chars = set()

    for char in word:
        if char not in seen_chars:
            char_count[char] = word.count(char)
            seen_chars.add(char)

    max_count = max(char_count.values())
    most_frequent = [char for char, count in char_count.items() if count == max_count]

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
