from collections import defaultdict, deque  # Used for graph storage and queue operations


def alien_order(words):
    graph = defaultdict(set)  # graph[u] -> characters that must come after u
    indegree = {}             # indegree[ch] -> number of prerequisites for ch
    has_rule = False          # Tracks whether we found at least one ordering rule

    # Step 1: Collect all unique characters
    for word in words:                # Loop through each word
        for ch in word:               # Loop through each character
            if ch not in indegree:    # If character is new
                indegree[ch] = 0      # Initialize indegree to zero

    # Step 2: Compare adjacent words to extract ordering rules
    for i in range(len(words) - 1):   # Compare word[i] and word[i+1]
        w1 = words[i]
        w2 = words[i + 1]

        # Invalid prefix case: longer word before its own prefix
        if len(w1) > len(w2) and w1.startswith(w2):
            return "INVALID INPUT (Prefix conflict)"

        min_len = min(len(w1), len(w2))

        for j in range(min_len):      # Compare character by character
            c1 = w1[j]
            c2 = w2[j]

            if c1 != c2:              # First difference gives a rule
                has_rule = True       # We found at least one valid ordering rule
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    indegree[c2] += 1
                break                 # Stop after first difference

    # Step 3: If no rules exist, ordering cannot be determined
    if not has_rule:
        return "INSUFFICIENT INFORMATION"

    # Step 4: Topological sort (Kahn’s algorithm)
    queue = deque()

    for ch in indegree:
        if indegree[ch] == 0:
            queue.append(ch)

    order = []

    while queue:
        ch = queue.popleft()
        order.append(ch)

        for nxt in graph[ch]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    # Step 5: Detect cycle (invalid ordering)
    if len(order) != len(indegree):
        return "INVALID INPUT (Cycle detected)"

    return order


def main():
    # Example 1: Single word (insufficient information)
    words = ["abc","xyz"]

    print("Input words:", words)
    result = alien_order(words)
    print("Output:", result)


if __name__ == "__main__":
    main()
