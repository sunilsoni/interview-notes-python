from collections import Counter
from itertools import combinations

"""You are given an array S made of N strings and an integer K. Choose at most K letters from the alphabet that will allow you to build as many strings from array S as possible. Any of the chosen letters can be used multiple times when building the strings.
What is the maximum number of strings from S that can be built?
Write a function:
def solution (S, K)
that, given an array S and an integer K, returns the maximum number of strings from S that can be built.
Examples:
1. Given S = ['"abc", "abb", "cb", "a", "bbb"] and K = 2, the function should return
3. Strings "abb",
', "a" and "bbb" can be built using the two letters 'a' and 'b'.
2. Given S = ["adf", "jbh", "jegj", "eij", "adf"] and K = 3, the function should
return 2. Two strings "adf" can be built using three letters 'a', 'd' and 'f".

2. Given S = ["adf", "jibh", "jegj", "eiji", "adf"] and K = 3, the function should
return 2. Two strings "adf" can be built using three letters 'a', 'd' and 'f'.
3. Given S = ['"abcd", "efgh"] and K = 3, the function should return 0. It is not
possible to build any string from S using at most three letters.
4. Given S = ['"bc", "edf", "fe", "dge", "abcd"] and K = 4, the function should
return 3. Strings "edf", "fde" and "dge" can be built using the four letters 'd', 'e,
'f' and 'g'.
Write an efficient algorithm for the following assumptions:
• N is an integer within the range [1.50,000];
• Kis an integer within the range [1..10l;
• each string in S has a length within the range [1.15];
• each string in S is made from only the first ten lowercase letters of the alphabet (a-j").

"""

def solution(S, K):
    # Count the frequency of each letter in all strings
    letter_counts = Counter(''.join(S))

    # Get unique letters used in all strings
    unique_letters = set(''.join(S))

    max_strings = 0

    # Try all combinations of K letters
    for letter_combo in combinations(unique_letters, min(K, len(unique_letters))):
        count = sum(1 for s in S if set(s).issubset(letter_combo))
        max_strings = max(max_strings, count)

    return max_strings


def test_cases():
    test_cases = [
        (["abc", "abb", "cb", "a", "bbb"], 2, 3),
        (["adf", "jbh", "jegj", "eij", "adf"], 3, 2),
        (["adf", "jibh", "jegj", "eiji", "adf"], 3, 2),
        (["abcd", "efgh"], 3, 0),
        (["bc", "edf", "fe", "dge", "abcd"], 4, 3),
        # Additional test cases
        (["a", "b", "c", "d", "e"], 1, 1),
        (["aa", "bb", "cc", "dd", "ee"], 5, 5),
        (["abcdefghij"] * 50000, 10, 50000),  # Large input test
    ]

    for i, (S, K, expected) in enumerate(test_cases, 1):
        result = solution(S, K)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test case {i}: {status}")
        print(f"  Input: S = {S[:5]}{'...' if len(S) > 5 else ''}, K = {K}")
        print(f"  Expected: {expected}, Got: {result}")
        print()


if __name__ == "__main__":
    test_cases()
