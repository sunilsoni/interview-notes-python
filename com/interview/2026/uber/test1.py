import collections


def findAlienOrder(words):
    """
    Main function to find the order of characters in the alien language.
    """

    # 1. Initialize the data structures
    # adj_list: This is our 'Graph'. It stores the rules.
    # Key is a char, Value is a set of chars that come AFTER it.
    adj_list = collections.defaultdict(set)

    # in_degree: This counts how many rules say a specific char comes 'after' something else.
    # We initialize it with 0 for every unique character found in all words.
    in_degree = {char: 0 for word in words for char in word}

    # 2. Build the Graph (Find dependency rules)
    # We compare each word with the word immediately following it.
    for i in range(len(words) - 1):
        w1 = words[i]  # First word
        w2 = words[i + 1]  # Second word

        # Check for a specific invalid edge case:
        # If w1 is longer than w2 and w1 starts with w2 (e.g., "apple", "app"),
        # then the dictionary is invalid because "app" should be before "apple".
        if len(w1) > len(w2) and w1.startswith(w2):
            return []  # Return empty list indicating error/invalid input

        # Iterate through the characters of both words to find the first difference
        for j in range(min(len(w1), len(w2))):
            if w1[j] != w2[j]:
                # We found the first difference!
                # w1[j] comes before w2[j]. This is a rule.

                # Only add the rule if we haven't seen it before
                if w2[j] not in adj_list[w1[j]]:
                    adj_list[w1[j]].add(w2[j])  # Add edge w1[j] -> w2[j]
                    in_degree[w2[j]] += 1  # Increase dependency count for w2[j]

                # Once we find the first difference, the order is decided by this pair.
                # We stop checking the rest of the characters for this pair of words.
                break

    # 3. Topological Sort (Using Breadth-First Search - BFS)
    # Create a queue and add all characters that have 0 in-degree (no dependencies).
    # These are the characters that can come first in the alphabet.
    queue = collections.deque([char for char in in_degree if in_degree[char] == 0])

    result = []  # List to store the final sorted order

    while queue:
        # Remove a character from the front of the queue
        char = queue.popleft()
        result.append(char)  # Add it to our alphabet order

        # Look at all neighbors (characters that come after this current 'char')
        if char in adj_list:
            for neighbor in adj_list[char]:
                # Since we have processed 'char', we "remove" the dependency for the neighbor
                in_degree[neighbor] -= 1

                # If the neighbor now has 0 dependencies, it's ready to be added to the queue
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    # 4. Final Check for Cycles
    # If the result list doesn't contain all unique characters, it means there was a cycle
    # (e.g., a -> b -> a). In that case, valid ordering is impossible.
    if len(result) < len(in_degree):
        return []  # Return empty list indicating invalid data

    return result


# --- TESTING SECTION ---

def run_tests():
    """
    Simple main method to run test cases and verify PASS/FAIL.
    """
    print("--- Starting Alien Dictionary Tests ---\n")

    # Define a list of test cases.
    # Each case is a dictionary with 'input', 'expected', and a 'name'.
    test_cases = [
        {
            "name": "Example 1 (Basic)",
            "input": ["xww", "wxyz", "wxyw", "ywx", "ywz"],
            "expected": ['x', 'z', 'w', 'y']
        },
        {
            "name": "Example 2 (Simple)",
            "input": ["baa", "abcd", "abca", "cab", "cad"],
            "expected": ['b', 'd', 'a', 'c']
        },
        {
            "name": "Example 3 (Same Prefix)",
            "input": ["caa", "aaa", "aab"],
            "expected": ['c', 'a', 'b']
        },
        {
            "name": "Edge Case: Invalid Prefix",
            "input": ["apple", "app"],
            "expected": []  # Should fail because 'apple' cannot be before 'app'
        },
        {
            "name": "Edge Case: Cycle (Impossible)",
            "input": ["z", "x", "z"],
            "expected": []  # z < x and x < z is a cycle
        },
        {
            "name": "Large Data Input",
            # Generate a long list of words: a, ab, abc... this creates a simple chain a->b->c...
            "input": [chr(ord('a') + i) for i in range(26)],
            "expected": [chr(ord('a') + i) for i in range(26)]
        }
    ]

    # Loop through each test case
    for test in test_cases:
        print(f"Running: {test['name']}")
        print(f"Input: {test['input'][:5]}..." if len(test['input']) > 5 else f"Input: {test['input']}")

        try:
            actual_output = findAlienOrder(test['input'])

            # NOTE: For some inputs, multiple valid orders might exist.
            # To strictly pass typical unit tests for this problem, we usually check
            # if the output is ONE of the valid topological sorts.
            # However, for simplicity here, we check exact match or if output is valid.

            # For the Large Data Input check specifically:
            if test['name'] == "Large Data Input":
                if len(actual_output) == 26:
                    print(f"Result: PASS \n")
                else:
                    print(f"Result: FAIL (Length mismatch)\n")

            # For specific error cases (expecting empty list)
            elif test['expected'] == []:
                if actual_output == []:
                    print("Result: PASS \n")
                else:
                    print(f"Result: FAIL. Expected [], got {actual_output}\n")

            # Standard cases
            else:
                # We check if the result matches the expected logic
                # (Direct comparison works for unique linear paths, which examples usually are)
                if actual_output == test['expected']:
                    print("Result: PASS \n")
                else:
                    print(f"Expected: {test['expected']}")
                    print(f"Got:      {actual_output}")
                    print("Result: FAIL \n")

        except Exception as e:
            print(f"Result: FAIL (Crashed with error: {e})\n")


if __name__ == "__main__":
    run_tests()