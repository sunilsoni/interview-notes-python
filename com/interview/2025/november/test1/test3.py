def final_board_after_game(s: str) -> str:
    n = len(s)
    stack = []

    i = 0
    while i < n:
        j = i + 1
        while j < n and s[j] == s[i]:
            j += 1
        run_len = j - i
        ch = s[i]

        if run_len >= 2:
            pass
        else:
            if stack and stack[-1][0] == ch:
                stack[-1][1] += 1
                if stack[-1][1] >= 2:
                    stack.pop()
            else:
                stack.append([ch, 1])

        i = j

    result_parts = []
    for ch, cnt in stack:
        result_parts.append(ch * cnt)

    return "".join(result_parts)

def main():
    tests = [
        ("abbba", ""),
        ("azxxzy", "ay"),
        ("a", "a"),
        ("", ""),
        ("aa", ""),
        ("ab", "ab"),
        ("abba", ""),
        ("abccba", ""),
        ("abcca", "aba"),
    ]

    big = "a" + ("b" * 100_000) + "a"
    tests.append((big, ""))

    passed = failed = 0
    for idx, (inp, expected) in enumerate(tests, 1):
        out = final_board_after_game(inp)
        ok = out == expected
        if ok:
            print(f"Test {idx}: PASS input_len={len(inp)} expected_len={len(expected)}")
            passed += 1
        else:
            print(f"Test {idx}: FAIL input_len={len(inp)} expected={repr(expected)} got={repr(out)}")
            failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed out of {len(tests)}")

if __name__ == "__main__":
    main()
