def game(s: str) -> str:
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
    while stack and stack[-1][1] >= 2:
        stack.pop()
    parts = []
    for ch, cnt in stack:
        parts.append(ch * cnt)
    return "".join(parts)

def main():
    tests = [
        ("abbba", ""),          # abbba -> bbb removed -> aa -> removed -> ""
        ("azxxzy", "ay"),       # classic example -> "ay"
        ("a", "a"),
        ("", ""),
        ("aa", ""),
        ("ab", "ab"),
        ("abba", ""),           # abba -> bb removed -> aa -> removed -> ""
        ("abccba", ""),         # cc removed -> abba -> bb removed -> aa -> removed -> ""
        ("abcca", "aba"),       # cc removed -> aba
        ("bbb", ""),            # full run removed
        # large test: "a" + 100k "b" + "a" -> middle removed -> "aa" -> removed -> ""
        ("a" + ("b" * 100_000) + "a", ""),
    ]

    passed = failed = 0
    for i, (inp, expected) in enumerate(tests, 1):
        out = game(inp)
        if out == expected:
            print(f"Test {i}: PASS input_len={len(inp)} expected_len={len(expected)}")
            passed += 1
        else:
            print(f"Test {i}: FAIL input_len={len(inp)} expected={repr(expected)} got={repr(out)}")
            failed += 1

    print(f"\nSummary: {passed} passed, {failed} failed out of {len(tests)}")

if __name__ == "__main__":
    main()
