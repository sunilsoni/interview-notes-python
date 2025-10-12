def solution(text):
    count = 0
    for w in text.split():
        if w and w[0].lower() == w[-1].lower():
            count += 1
    return count


def main():
    tests = [
        ("Level dEmaND noNe", 2),
        ("", 0),
        ("b Bb aAa", 3),
        ("A", 1),
        ("ab ba cc ddE", 1),
        ("   a   bB   cC  d   ", 4),
        ("Aa aaA bcdD", 2),
    ]

    for text, expected in tests:
        print("PASS" if solution(text) == expected else "FAIL")

    words = []
    expect = 0
    for i in range(50000):
        if i % 2 == 0:
            words.append("abA")
            expect += 1
        else:
            words.append("ab")
    large_text = " ".join(words)
    print("Large input test passed:", str(solution(large_text) == expect).lower())


if __name__ == "__main__":
    main()