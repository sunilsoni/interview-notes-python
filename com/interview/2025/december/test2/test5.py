def add_drama(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == '!':
            j = i
            while j < n and text[j] == '!':
                j += 1
            out.append('!' * (j - i + 1))
            i = j
        elif c == '.':
            out.append('!')
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def main():
    tests = [
        {
            "input": "Roses are red. Oranges are orange! Yeah!!!",
            "expected": "Roses are red! Oranges are orange!! Yeah!!!!"
        },
        {
            "input": "",
            "expected": ""
        },
        {
            "input": "Hello....World!!!",
            "expected": "Hello!!!!World!!!!"
        },
        {
            "input": "No drama here",
            "expected": "No drama here"
        },
        {
            "input": "!!!...!",
            "expected": "!!!!!!!!!"  # corrected: 9 exclamation marks
        }
    ]

    large = "a" * 200000 + "!!!" + "." * 100000
    expected_large = "a" * 200000 + "!!!!" + "!" * 100000
    tests.append({"input": large, "expected": expected_large})

    for idx, t in enumerate(tests, 1):
        res = add_drama(t["input"])
        print("Test", idx, "PASS" if res == t["expected"] else "FAIL")


if __name__ == "__main__":
    main()
