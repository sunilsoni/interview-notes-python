def solution(fragments, accessCode):
    s = str(accessCode)
    cnt = {}
    a = [str(x) for x in fragments]
    for x in a: cnt[x] = cnt.get(x, 0) + 1
    ans = 0
    for x in a:
        if s.startswith(x):
            r = s[len(x):]
            if r:
                ans += cnt.get(r, 0) - (1 if r == x else 0)
    return ans

def _chk(i, got, exp):
    print(f"Test{i}: {'PASS' if got==exp else 'FAIL'}")

def main():
    tests = [
        ([1, 212, 12, 12], 1212, 3),
        ([11, 11, 110], 11011, 2),
        ([777, 7, 777, 77, 77], 7777, 6),
        ([1, 2, 3], 12, 1),
        ([12, 1, 2, 12], 1212, 2),
    ]
    for i,(f,c,e) in enumerate(tests,1):
        _chk(i, solution(f,c), e)

    n = 30000
    f = [12]*(n//2) + [12]*(n - n//2)
    _chk(len(tests)+1, solution(f, 1212), n*(n-1))

if __name__ == "__main__":
    main()