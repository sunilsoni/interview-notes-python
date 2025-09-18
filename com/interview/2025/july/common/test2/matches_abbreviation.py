def matches_abbreviation(word: str, abbr: str) -> bool:
    # i = index in abbr, j = index in word
    i, j = 0, 0

    # Process until either string is exhausted
    while i < len(abbr) and j < len(word):
        if abbr[i].isdigit():
            # Reject leading zero
            if abbr[i] == '0':
                return False
            num = 0
            # Build the skip count
            while i < len(abbr) and abbr[i].isdigit():
                num = num * 10 + int(abbr[i])
                i += 1
            # Advance the word pointer by that many letters
            j += num
        else:
            # Must match the letter (case-insensitive)
            if abbr[i].lower() != word[j].lower():
                return False
            i += 1
            j += 1

    # True only if both pointers are exactly at the end
    return i == len(abbr) and j == len(word)


def main():
    test_cases = [
        ("meta",      "m2a",      True),
        ("internationalization", "i18n", True),
        ("intern",    "i18n",     False),
        ("facebook",  "f6k",      True),
        ("focus",     "f6k",      False),
        ("Facebook",  "F2eb2k",   True),
        ("Facebook",  "g",        True),
        # Large-data tests
        ("a"*1_000_000 + "b", "1000000b", True),
        ("a"*1_000_000 + "b", "1000000a", False),
    ]

    for idx, (word, abbr, expected) in enumerate(test_cases, start=1):
        result = matches_abbreviation(word, abbr)
        status = "PASS" if result == expected else f"FAIL (got {result})"
        print(f"Test {idx}: {status}")

if __name__ == "__main__":
    main()