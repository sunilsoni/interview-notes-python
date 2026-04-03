# Import deque for an efficient, fast queue
from collections import deque


# --- 1. THE NODE CLASS ---
class Member:
    # We define our Node class exactly as discussed: an integer ID and a name.
    def __init__(self, member_id, name):
        self.member_id = member_id  # Unique integer (e.g., 1, 2, 3)
        self.name = name  # The person's display name

    # This helps us see the name and ID clearly when printing or debugging
    def __repr__(self):
        return f"[{self.member_id}] {self.name}"


# --- 2. THE SEARCH ALGORITHM ---
def get_connection_distance(network_graph, start_id, target_id):
    # We now check if the IDs exist in our network graph
    if start_id not in network_graph or target_id not in network_graph:
        return -1

    # If the start ID is the same as the target ID, distance is 0 steps
    if start_id == target_id:
        return 0

    # Our queue now holds tuples of: (current_member_id, current_distance)
    # We start with the starting ID at distance 0
    search_queue = deque([(start_id, 0)])

    # Our visited set tracks the unique IDs we've already checked
    # This prevents infinite loops if two people are mutual friends
    visited = set([start_id])

    # Keep searching as long as there are IDs in the queue
    while search_queue:
        # Pull the next ID and its distance from the front of the line
        current_id, current_distance = search_queue.popleft()

        # If we found the target ID, we are done! Return the distance.
        if current_id == target_id:
            return current_distance

        # Look up the friends list using the current ID
        for friend_id in network_graph.get(current_id, []):
            # Check if we haven't visited this ID yet
            if friend_id not in visited:
                # Mark them as visited
                visited.add(friend_id)
                # Add the friend's ID to the back of the queue, adding 1 to the distance
                search_queue.append((friend_id, current_distance + 1))

    # If the queue empties out and we never found the target ID, they aren't connected
    return -1


# --- 3. TESTING ---
def main():
    # Create our unique Member nodes
    bob = Member(1, "Bob")
    alice_1 = Member(2, "Alice")  # The first Alice
    john = Member(3, "John")
    frank = Member(4, "Frank")
    alice_2 = Member(5, "Alice")  # A completely different Alice!

    # Build the network using their unique IDs, not their names!
    # Format: { member_id: [list of friend_ids] }
    graph = {
        bob.member_id: [alice_1.member_id, john.member_id],
        alice_1.member_id: [bob.member_id, frank.member_id],
        john.member_id: [bob.member_id],
        frank.member_id: [alice_1.member_id],
        alice_2.member_id: []  # The second Alice is isolated in this network
    }

    print("--- Testing Unique ID Graph ---")

    # Test 1: Bob looking for the first Alice (Should be 1 step)
    dist1 = get_connection_distance(graph, bob.member_id, alice_1.member_id)
    print(f"Distance from {bob.name} to {alice_1.name} (ID {alice_1.member_id}): {dist1} step(s).")

    # Test 2: Bob looking for the second Alice (Should be -1, no connection)
    dist2 = get_connection_distance(graph, bob.member_id, alice_2.member_id)
    print(f"Distance from {bob.name} to {alice_2.name} (ID {alice_2.member_id}): {dist2} step(s).")


if __name__ == "__main__":
    main()