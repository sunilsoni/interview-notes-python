def final_board_after_game(s: str) -> str:
    # Function returns the final state of the board after repeatedly removing
    # any consecutive group of identical chars of length >= 2.
    # We use run-length scanning + a stack of (char, count) to allow chain removals.

    n = len(s)  # store length once to avoid repeated len() calls (tiny optimization)
    stack = []  # stack will hold [ [char, count], ... ] for surviving groups

    i = 0  # index to scan through s
    while i < n:
        # find a maximal run of the same character starting at i
        j = i + 1  # j will move until run ends
        while j < n and s[j] == s[i]:
            j += 1
        run_len = j - i      # length of this run (>=1)
        ch = s[i]            # character of this run

        if run_len >= 2:
            # If the run length is >=2, this entire run disappears immediately.
            # Do nothing (i.e., we skip pushing it to the stack).
            # We still advance i to j and continue; later runs may merge with previous stack top.
            pass
        else:
            # run_len == 1 (single char). We need to merge it with stack top if same char,
            # because after previous deletions two equal singletons can become adjacent.
            if stack and stack[-1][0] == ch:
                # merge into previous group: increment its count
                stack[-1][1] += 1
                # if merging produced count >= 2, the whole group should vanish
                if stack[-1][1] >= 2:
                    stack.pop()  # remove that group and allow chain reactions
            else:
                # push this single-char group as (char, 1)
                stack.append([ch, 1])

        # move i forward to the next run
        i = j

    # reconstruct the final string from the stack (each group's count should be 1 here,
    # because any count >=2 would have been removed; but be general)
    result_parts = []
    for ch, cnt in stack:
        result_parts.append(ch * cnt)

    return "".join(result_parts)


def main():
    tests = [
        ("abbba", ""),            # abbba -> (bbb removed) -> aa -> removed -> ""
        ("azxxzy", "ay"),         # azxxzy -> xx removed -> azzy -> zz removed -> ay
        ("a", "a"),
        ("", ""),
        ("aa", ""),
        ("ab", "ab"),
        ("abba", ""),
        ("abccba", ""),
        ("abcca", "aba"),         # CORRECT expectation: after cc removed -> aba
    ]

    # Large performance test
    big = "a" + ("b" * 100_000) + "a"
    tests.append((big, ""))

    passed = failed = 0
    for idx, (inp, expected) in enumerate(tests, 1):
        out = final_board_after_game(inp)
        if out == expected:
            print(f"Test {idx}: PASS input_len={len(inp)} expected_len={len(expected)}")
            passed += 1
        else:
            print(f"Test {idx}: FAIL input_len={len(inp)} expected={repr(expected)} got={repr(out)}")
            failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed out of {len(tests)}")

if __name__ == "__main__":
    main()
