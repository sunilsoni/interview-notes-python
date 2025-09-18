def custom_sort(s: str, order: str) -> str:
    # Create a mapping from each character in 'order' to its position (0,1,2,...)
    order_index = {}
    for idx, ch in enumerate(order):
        order_index[ch] = idx           # e.g. order="bca" → {'b':0, 'c':1, 'a':2}

    # Count how many times each character appears in 's'
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1  # increment count for ch

    # Build the result in two phases
    result_chars = []

    # Phase 1: append chars that are in 'order', in that exact sequence
    for ch in order:
        if ch in freq:
            count = freq[ch]
            result_chars.extend([ch] * count)  # add 'ch' count times
            del freq[ch]                # remove it so we don't process it again

    # Phase 2: append any remaining chars (those not in 'order'),
    # sorted lexicographically by their character value
    for ch in sorted(freq.keys()):
        count = freq[ch]
        result_chars.extend([ch] * count)  # add each leftover char count times

    # Join the list of characters into the final string and return it
    return ''.join(result_chars)


def main():
    # Define test cases with expected outputs
    test_cases = [
        { 's': "abcab",      'order': "bca", 'expected': "bbcaa"  },
        { 's': "",           'order': "abc", 'expected': ""       },
        { 's': "xyz",        'order': "abc", 'expected': "xyz"    },
        { 's': "food",       'order': "of",  'expected': "oofd"   },
        # Large-data test: one million 'a's; checking length only
        { 's': "a" * 1_000_000, 'order': "a", 'expected': None    },
    ]

    for i, case in enumerate(test_cases, start=1):
        s      = case['s']
        order  = case['order']
        exp    = case['expected']
        output = custom_sort(s, order)

        # For huge test, just verify length and basic character count
        if exp is None:
            result = "PASS" if len(output) == len(s) and output.count(order[0]) == s.count(order[0]) else "FAIL"
        else:
            result = "PASS" if output == exp else f"FAIL (got {output!r})"

        print(f"Test {i}: {result}")


if __name__ == "__main__":
    main()