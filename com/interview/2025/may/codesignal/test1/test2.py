def solution(alienCode: str) -> int:
    n = len(alienCode)
    count = 0
    for i in range(n):
        for j in range(i, n):
            # skip substrings with leading zero, except "0" itself
            if j > i and alienCode[i] == '0':
                continue
            num = int(alienCode[i:j+1])
            if num % 3 == 0:
                count += 1
    return count

if __name__ == "__main__":
    tests = [
        ("456", 3),
        ("6666", 10),
        ("303", 5),
        ("12", 1),               # edge: minimal length
        ("9999999999", 55),      # max-length: all digits '9'
    ]

    for inp, exp in tests:
        got = solution(inp)
        result = "PASS" if got == exp else "FAIL"
        print(f"Input: {inp:>10}  Expected: {exp:>2}  Got: {got:>2}  → {result}")