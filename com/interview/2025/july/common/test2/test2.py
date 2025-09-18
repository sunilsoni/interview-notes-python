import fileinput

inputData = ''
for line in fileinput.input():
    inputData += line.strip()


def code_here():
    s = inputData.replace(" ", "")  # remove spaces
    n = len(s)

    # function to compute LCS (Longest Common Subsequence)
    def lcs(a, b):
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]

    # longest palindromic subsequence = lcs(s, reverse(s))
    lps = lcs(s, s[::-1])

    # min insertions = n - lps
    return n - lps


print(code_here())


# ------------------ Testing ------------------
def main():
    test_cases = {
        "alpha": 2,
        "race": 1,
        "a": 0,
        "ab": 1,
        "abc": 2,
        "madam": 0,
        "palindrome": 8,
        "": 0,
        "aabb": 0,  # can be rearranged to palindrome
        "abcdefgfedcba": 0,
    }

    for s, expected in test_cases.items():
        input_str = s.replace(" ", "")
        n = len(input_str)

        def lcs(a, b):
            m, n = len(a), len(b)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if a[i - 1] == b[j - 1]:
                        dp[i][j] = 1 + dp[i - 1][j - 1]
                    else:
                        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
            return dp[m][n]

        lps = lcs(input_str, input_str[::-1])
        result = n - lps
        status = "PASS" if result == expected else "FAIL"
        print(f"Input: {s} | Expected: {expected} | Got: {result} | {status}")


if __name__ == "__main__":
    main()