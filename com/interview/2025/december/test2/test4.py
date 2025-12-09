import sys
import math
from contextlib import redirect_stdout


def filter_words(words, letters):
    letter_set = set(letters)
    result = []
    for word in words:
        for ch in word:
            if ch in letter_set:
                result.append(word)
                break
    return result


def main():
    test_cases = [
        {
            "words": ['the', 'dog', 'got', 'a', 'bone'],
            "letters": 'ae',
            "expected": ['the', 'a', 'bone']
        },
        {
            "words": [],
            "letters": 'abc',
            "expected": []
        },
        {
            "words": ['hello', 'world'],
            "letters": '',
            "expected": []
        },
        {
            "words": ['apple', 'banana', 'cherry'],
            "letters": 'a',
            "expected": ['apple', 'banana']
        },
        {
            "words": ['dog', 'fish', 'bird'],
            "letters": 'xyz',
            "expected": []
        },
        {
            "words": ['a', 'b', 'c', 'd'],
            "letters": 'ac',
            "expected": ['a', 'c']
        },
        {
            "words": ['cat', 'bat', 'rat', 'dog'],
            "letters": 'aeiou',
            "expected": ['cat', 'bat', 'rat', 'dog']
        },
        {
            "words": ['xyz', 'pqr', 'mno'],
            "letters": 'o',
            "expected": ['mno']
        },
        {
            "words": ['test' + chr(97 + (i % 26)) for i in range(50000)],
            "letters": 'ae',
            "expected": [w for w in ['test' + chr(97 + (i % 26)) for i in range(50000)] if 'a' in w or 'e' in w]
        },
        {
            "words": ['a' * 10000, 'b' * 10000, 'c' * 10000],
            "letters": 'ac',
            "expected": ['a' * 10000, 'c' * 10000]
        },
    ]

    all_passed = True
    for idx, tc in enumerate(test_cases):
        result = filter_words(tc["words"], tc["letters"])
        status = "PASS" if result == tc["expected"] else "FAIL"
        print(f"Test {idx + 1}: {status}")
        if status == "FAIL":
            all_passed = False
            if len(tc["expected"]) < 20:
                print(f"  Expected: {tc['expected']}")
                print(f"  Got: {result}")
            else:
                print(f"  Expected length: {len(tc['expected'])}, Got length: {len(result)}")

    print()
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")


if __name__ == "__main__":
    main()