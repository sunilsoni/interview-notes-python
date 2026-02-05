from collections import defaultdict, deque  # We use defaultdict for graph and deque for fast queue operations


def alien_order(words):  # This function finds a valid character order from the sorted alien dictionary
    graph = defaultdict(set)  # graph[u] will store all v such that u -> v (u comes before v)
    indegree = {}  # indegree[ch] = number of incoming edges into ch (how many chars must come before ch)

    # Step 1: Initialize indegree for every unique character we see
    for word in words:  # Loop through each word to collect all unique characters
        for ch in word:  # Loop through each character in the current word
            if ch not in indegree:  # If character not added yet, initialize it
                indegree[ch] = 0  # No incoming edges known yet

    # Step 2: Build ordering rules by comparing adjacent words
    for i in range(len(words) - 1):  # Compare word i with word i+1 because dictionary is sorted
        w1 = words[i]  # First word in the adjacent pair
        w2 = words[i + 1]  # Second word in the adjacent pair

        # Prefix invalid case: if w1 starts with w2 but w1 is longer, order is impossible
        if len(w1) > len(w2) and w1.startswith(w2):  # Example: ["abc", "ab"] is invalid
            return []  # Return empty because no valid alphabet can make this sorted

        # Find the first differing character to create one ordering rule
        min_len = min(len(w1), len(w2))  # We only compare up to the shorter word length
        for j in range(min_len):  # Walk character-by-character to find first difference
            c1 = w1[j]  # Current character in first word
            c2 = w2[j]  # Current character in second word

            if c1 != c2:  # The first mismatch gives us the ordering rule
                # Add edge c1 -> c2 if it is not already present
                if c2 not in graph[c1]:  # Prevent double-counting the same edge
                    graph[c1].add(c2)  # Record that c1 comes before c2
                    indegree[c2] += 1  # c2 now has one more prerequisite
                break  # Important: only the first differing character matters
            # If characters are the same, we continue checking the next position

    # Step 3: Topological sort using Kahn's algorithm
    queue = deque()  # Queue of nodes with indegree 0 (no prerequisites)
    for ch in indegree:  # Check every known character
        if indegree[ch] == 0:  # If it has no prerequisites
            queue.append(ch)  # It can be placed first (or early) in the ordering

    order = []  # This list will store the final character order

    while queue:  # Continue until we have processed all reachable nodes
        ch = queue.popleft()  # Take a character with indegree 0
        order.append(ch)  # Append it to the final ordering because it is valid to place now

        for nxt in graph[ch]:  # For each character that must come after ch
            indegree[nxt] -= 1  # We "remove" the edge ch -> nxt by reducing indegree
            if indegree[nxt] == 0:  # If nxt now has no prerequisites left
                queue.append(nxt)  # It is ready to be placed in the ordering

    # Step 4: If we did not place all characters, there is a cycle (contradiction)
    if len(order) != len(indegree):  # Cycle means some nodes could never reach indegree 0
        return []  # Return empty ordering

    return order  # Return a valid alien alphabet order as a list of characters


def is_valid_alien_order(words, order):  # This checks if 'order' truly works for the given sorted word list
    if order == []:  # If order is empty, it might be correct only if the dictionary is invalid
        # We cannot easily prove invalidity here without recomputing, so we treat empty as "valid only if algorithm returned it"
        return False  # For testing, empty should fail unless expected is specifically empty

    rank = {}  # rank[ch] = position of ch in the alien order
    for i, ch in enumerate(order):  # Build rank mapping to compare characters quickly
        rank[ch] = i  # Store numeric rank

    # Collect all unique chars from words to ensure order includes them all
    all_chars = set()  # Set of all unique characters in dictionary
    for w in words:  # Loop through words
        for ch in w:  # Loop through chars in word
            all_chars.add(ch)  # Add char to the set

    if set(order) != all_chars:  # Order must contain exactly the unique characters
        return False  # If missing or extra characters, it is not a valid answer

    # Compare each adjacent pair to ensure word[i] <= word[i+1] under this alien order
    for i in range(len(words) - 1):  # Adjacent pairs define sorted property
        w1 = words[i]  # First word
        w2 = words[i + 1]  # Next word

        # Compare w1 and w2 using alien ranking
        min_len = min(len(w1), len(w2))  # Only compare shared length
        decided = False  # Track whether we found a difference and decided ordering

        for j in range(min_len):  # Walk character by character
            c1 = w1[j]  # Char from first word
            c2 = w2[j]  # Char from second word

            if c1 != c2:  # If we find first difference
                if rank[c1] > rank[c2]:  # If c1 should come after c2, order is wrong
                    return False  # Not sorted correctly
                decided = True  # We successfully decided this pair ordering
                break  # Stop at first difference

        if not decided:  # If all compared chars were the same up to min_len
            if len(w1) > len(w2):  # Then shorter must come first, otherwise invalid
                return False  # Not sorted under this alien order

    return True  # If all adjacent checks passed, order is valid


def main():  # Main method to run tests without unit test frameworks
    test_cases = []  # We'll store (name, words, expected_empty) where expected_empty says if result must be empty

    # Provided example from prompt
    test_cases.append((
        "Example-0",
        ["xww", "wxyz", "wxyw", "ywx", "ywz"],
        False
    ))

    # Provided example 1
    test_cases.append((
        "Example-1",
        ["baa", "abcd", "abca", "cab", "cad"],
        False
    ))

    # Provided example 2 (from screenshot)
    test_cases.append((
        "Example-2",
        ["caa", "aaa", "aab"],
        False
    ))

    # Edge case: single word (any order of unique chars is fine)
    test_cases.append((
        "Edge-single-word",
        ["zxy"],
        False
    ))

    # Edge case: duplicate words (still fine)
    test_cases.append((
        "Edge-duplicates",
        ["abc", "abc", "abc"],
        False
    ))

    # Edge case: invalid prefix (must return [])
    test_cases.append((
        "Edge-invalid-prefix",
        ["abc", "ab"],
        True
    ))

    # Edge case: cycle (a < b and b < a)
    # "ab" < "ba" gives a < b, and "ba" < "ab" gives b < a (cycle)
    test_cases.append((
        "Edge-cycle",
        ["ab", "ba", "ab"],
        True
    ))

    # Large data test: many words consistent with known order a < b < c < ... < j
    # We build words so that constraints are easy and consistent
    large_words = []  # List for large test
    for i in range(2000):  # Create many words to simulate larger input
        large_words.append("a" + "b" + "c" + "d" + "e" + "f" + "g" + "h" + "i" + "j" + str(i))  # Keep prefix same then differ by suffix
    # Note: suffix digits introduce extra characters, so let's avoid digits for a clean alien alphabet test
    large_words = []  # Reset
    for i in range(2000):  # Create many words
        # Create words like "aj", "bj", "cj"... repeated patterns but sorted already
        # This doesn't add strong constraints besides a < b < c, etc. from adjacency differences
        large_words.append(chr(ord('a') + (i % 10)) + "j")  # Only letters a..j and j
    large_words.sort()  # Sort in normal order just to make a list; the algorithm will still infer some constraints
    test_cases.append((
        "Large-input",
        large_words,
        False
    ))

    # Run tests
    passed = 0  # Count how many tests passed
    for name, words, expected_empty in test_cases:  # Loop through all test cases
        result = alien_order(words)  # Compute alien order using our solution

        if expected_empty:  # If we expect no valid order
            ok = (result == [])  # Pass only if result is empty
        else:  # If we expect a valid order
            ok = is_valid_alien_order(words, result)  # Pass if the produced order truly matches the dictionary sort

        status = "PASS" if ok else "FAIL"  # Convert boolean to readable output
        print(f"{name}: {status}")  # Print test result line
        if not ok:  # If fail, print debug details
            print("  words  =", words[:10], ("...(truncated)" if len(words) > 10 else ""))  # Show sample of input
            print("  result =", result)  # Show produced ordering
            print()  # Blank line for readability
        else:  # If pass
            passed += 1  # Increase passed count

    print(f"\nSummary: {passed}/{len(test_cases)} tests passed.")  # Print final summary


if __name__ == "__main__":  # Standard Python entry point check
    main()  # Run the main function
