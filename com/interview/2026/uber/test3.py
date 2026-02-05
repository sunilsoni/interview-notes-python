from collections import defaultdict, deque  # We need defaultdict for easy graph storage and deque for fast queue operations


def alien_order(words):  # This function finds the character order of the alien language
    graph = defaultdict(set)  # graph[u] contains all characters v that must come after u (u -> v)
    indegree = {}  # indegree[ch] stores how many characters must come before ch

    # Step 1: Collect every unique character so even isolated characters appear in the result
    for word in words:  # Loop through each word in the dictionary
        for ch in word:  # Loop through each character in the word
            if ch not in indegree:  # If we have not seen this character before
                indegree[ch] = 0  # Start indegree at 0 because no rules are known yet

    # Step 2: Build ordering rules by comparing adjacent words (because the list is already sorted)
    for i in range(len(words) - 1):  # Compare each word with the next word
        w1 = words[i]  # Current word
        w2 = words[i + 1]  # Next word

        # Invalid case: longer word comes before its own prefix (example: "abc" before "ab")
        if len(w1) > len(w2) and w1.startswith(w2):  # Check prefix rule violation
            return []  # Return empty list because no valid character order is possible

        min_len = min(len(w1), len(w2))  # We only compare characters up to the shorter word length

        for j in range(min_len):  # Walk through characters until we find the first difference
            c1 = w1[j]  # Character from first word
            c2 = w2[j]  # Character from second word

            if c1 != c2:  # First mismatch gives a real ordering rule
                if c2 not in graph[c1]:  # Avoid adding the same edge twice
                    graph[c1].add(c2)  # Add rule: c1 must come before c2
                    indegree[c2] += 1  # Increase indegree because c2 has one more prerequisite
                break  # Stop because ONLY the first difference matters for lexicographic order

    # Step 3: Topological sort (Kahn’s algorithm) to produce a valid character ordering
    queue = deque()  # Queue will hold characters with indegree 0 (they can appear next in order)

    for ch in indegree:  # Check every character
        if indegree[ch] == 0:  # If no prerequisites
            queue.append(ch)  # Add it to the queue to start ordering

    order = []  # This will store the final result in correct order

    while queue:  # Process until no characters are left that can be safely placed
        ch = queue.popleft()  # Take one available character
        order.append(ch)  # Add it to the final answer because it is valid now

        for nxt in graph[ch]:  # For each character that must come after ch
            indegree[nxt] -= 1  # Reduce indegree because we have placed ch already
            if indegree[nxt] == 0:  # If nxt now has no remaining prerequisites
                queue.append(nxt)  # Add nxt to the queue because it is ready to be placed

    # Step 4: If not all characters were placed, it means there is a cycle (contradiction)
    if len(order) != len(indegree):  # Cycle prevents completing the ordering
        return []  # Return empty list to signal "no valid order"

    return order  # Return the computed alien alphabet order


def is_valid_alien_order(words, order):  # This function checks if the produced order keeps the words sorted
    if order == []:  # If order is empty, we treat it as invalid for this simple test checker
        return False  # Because in this single test we expect a real order, not empty

    rank = {}  # rank will map each character to its position in the alien order
    for i, ch in enumerate(order):  # Enumerate gives both index and character
        rank[ch] = i  # Store numeric rank for fast comparisons

    # Ensure order contains exactly the same characters that appear in the input
    all_chars = set()  # Set for unique characters in words
    for w in words:  # Loop through words
        for ch in w:  # Loop through characters in word
            all_chars.add(ch)  # Add to the set

    if set(order) != all_chars:  # If missing or extra characters exist
        return False  # Then the order is not valid

    # Check each adjacent pair is in sorted order using the alien ranking
    for i in range(len(words) - 1):  # Compare each word with the next
        w1 = words[i]  # First word
        w2 = words[i + 1]  # Second word

        min_len = min(len(w1), len(w2))  # Compare only up to the shorter length
        decided = False  # Track if we found a character difference

        for j in range(min_len):  # Walk character by character
            if w1[j] != w2[j]:  # First difference decides the ordering
                if rank[w1[j]] > rank[w2[j]]:  # If w1 char ranks after w2 char
                    return False  # Then the words are not sorted correctly
                decided = True  # We successfully validated this pair
                break  # Stop at first difference

        if not decided:  # If all compared characters were the same
            if len(w1) > len(w2):  # Then shorter must come first
                return False  # Otherwise invalid ordering

    return True  # All checks passed


def main():  # Simple main method (no unit test framework)
    # Only ONE test example (as you requested)
    words = ["baa", "abcd", "abca", "cab", "cad"]  # Example dictionary already sorted in alien order

    result = alien_order(words)  # Get the alien character order from the function

    # Print the generated order so we can see it
    print("Input words:", words)  # Show input
    print("Generated character order:", result)  # Show output

    # PASS/FAIL check for this one test
    if is_valid_alien_order(words, result):  # Validate the result against the dictionary order
        print("Test Result: PASS")  # Print PASS if valid
    else:
        print("Test Result: FAIL")  # Print FAIL if invalid


if __name__ == "__main__":  # Python entry point check so main runs only when file is executed directly
    main()  # Call the main method to run the single test
