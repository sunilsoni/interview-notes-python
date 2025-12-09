from json import dumps, loads
import sys
from typing import List


def decode(words: List[str], message: str) -> str:
    def get_signature(word):
        if len(word) == 0:
            return ('', '', '')
        if len(word) == 1:
            return (word[0], word[0], '')
        if len(word) == 2:
            return (word[0], word[1], '')
        return (word[0], word[-1], ''.join(sorted(word[1:-1])))

    word_lookup = {}  # FIXED: was word_lobkup
    for w in words:
        sig = get_signature(w)
        word_lookup[sig] = w  # Must match variable name above

    msg_words = message.split(' ')
    decoded = []

    for mw in msg_words:
        sig = get_signature(mw)
        if sig in word_lookup:
            decoded.append(word_lookup[sig])
        else:
            decoded.append(mw)

    return ' '.join(decoded)


def main():
    test_cases = [
        {
            "words": ["ball", "funny", "hello", "message", "is", "this"],
            "message": "hlelo tihs masegse is fnnuy",
            "expected": "hello this message is funny"
        },
        {
            "words": ["a", "i", "hello"],
            "message": "a i hlelo",
            "expected": "a i hello"
        },
        {
            "words": ["orange", "apple", "banana"],
            "message": "oagnre alppe bnanaa",
            "expected": "orange apple banana"
        },
        {
            "words": ["ab", "cd", "ef"],
            "message": "ab cd ef",
            "expected": "ab cd ef"
        },
        {
            "words": ["test"],
            "message": "tset",
            "expected": "test"
        },
        {
            "words": ["programming", "is", "fun"],
            "message": "prgamniomrg is fun",
            "expected": "programming is fun"
        },
        {
            "words": ["x", "y", "z"],
            "message": "x y z",
            "expected": "x y z"
        },
        {
            "words": ["hello", "world", "this", "is", "a", "test", "message"],
            "message": "hlelo wlrod tihs is a tset mseasge",
            "expected": "hello world this is a test message"
        },
        {
            "words": ["aa", "bb", "cc"],
            "message": "aa bb cc",
            "expected": "aa bb cc"
        },
    ]

    all_passed = True
    for idx, tc in enumerate(test_cases):
        result = decode(tc["words"], tc["message"])
        status = "PASS" if result == tc["expected"] else "FAIL"
        print(f"Test {idx + 1}: {status}")
        if status == "FAIL":
            all_passed = False
            print(f"  Expected: {tc['expected']}")
            print(f"  Got: {result}")

    print()
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")


if __name__ == "__main__":
    main()