def analyze_input(input_value):
    # Check if the string is empty or just contains blank spaces to avoid errors later.
    if not input_value.strip():
        # If it's empty, return 0 for the count and an empty string for the longest word.
        return (0, '')

    # The .split() method cuts the sentence into a list of individual words wherever there is a space.
    # Example: 'Hello world' becomes ['Hello', 'world']
    words = input_value.split()

    # We use len() to find out how many items (words) are inside our new list.
    # We store this number in the variable 'word_count'.
    word_count = len(words)

    # We set up an empty string variable to keep track of the longest word we find.
    # We start with nothing so that any real word will immediately take its place.
    longest_word = ""

    # We start a 'for' loop to look at every single word in our list, one by one.
    for word in words:
        # We check if the length of the word we are currently looking at is greater than
        # the length of the longest word we have saved so far.
        if len(word) > len(longest_word):
            # If the current word IS longer, we update our 'longest_word' variable to be this new word.
            longest_word = word

    # Finally, we pack the total count and the longest word inside parentheses to return them as a pair (a tuple).
    return (word_count, longest_word)


def main():
    # Define our test cases as a list of dictionaries.
    # Each dictionary holds the input and the expected (count, longest_word) tuple.
    test_cases = [
        {
            "name": "Standard Case (From Image)",
            "input": 'This sentence is our input value',
            "expected": (6, 'sentence')
        },
        {
            "name": "Single Word Case",
            "input": 'Hello',
            "expected": (1, 'Hello')
        },
        {
            "name": "Empty String Case",
            "input": '   ',
            "expected": (0, '')
        },
        {
            "name": "Tie for Longest Word (Returns First Found)",
            "input": 'apple banana cherry',
            "expected": (3, 'banana')  # Both banana and cherry are 6 letters, banana is first
        },
        {
            "name": "Large Data Input",
            # We create a massive string with 10,000 words. "tiny " repeated 9999 times + "gigantic"
            "input": 'tiny ' * 9999 + 'gigantic',
            "expected": (10000, 'gigantic')
        }
    ]

    print("--- Running Tests ---")

    # Loop through each test case
    for test in test_cases:
        # Run our function on the test input
        result = analyze_input(test["input"])

        # Check if our result matches the expected answer
        if result == test["expected"]:
            print(f"[PASS] {test['name']}")
        else:
            print(f"[FAIL] {test['name']}")
            print(f"   Expected: {test['expected']}")
            print(f"   Got:      {result}")


# This ensures the main testing function runs when the script is executed.
if __name__ == "__main__":
    main()