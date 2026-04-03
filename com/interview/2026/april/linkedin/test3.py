from collections import deque


# --- 1. THE NODE CLASS ---
class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name


# --- 2. THE OPTIMIZED SEARCH ALGORITHM ---
def get_bidirectional_distance(graph, start_id, target_id):
    # Safety checks: Do they exist? Are they the same person?
    if start_id not in graph or target_id not in graph:
        return -1
    if start_id == target_id:
        return 0

    # SETUP: We now need TWO queues. One starting from You, one starting from the Target.
    start_queue = deque([start_id])
    target_queue = deque([target_id])

    # SETUP: We use Dictionaries instead of Sets for our "Visited" trackers.
    # We need to remember: { member_id : distance_from_their_starting_point }
    # Why? Because when the two search parties finally meet, we have to add their distances together!
    start_visited = {start_id: 0}
    target_visited = {target_id: 0}

    # --- HELPER FUNCTION ---
    # This function handles looking at just ONE person from whichever queue we tell it to.
    def expand_search_party(active_queue, active_visited, other_visited):
        # Pull the next person from the front of the active line
        current_id = active_queue.popleft()
        current_distance = active_visited[current_id]

        # Look through all of their friends
        for friend_id in graph.get(current_id, []):

            # THE MAGIC MOMENT: Did we just bump into the other search party?
            if friend_id in other_visited:
                # We found the connecting link!
                # Total Distance = (My distance to this friend) + 1 (the handshake) + (Their distance to this friend)
                return current_distance + 1 + other_visited[friend_id]

            # If we haven't seen this friend yet on our side, add them to our tracking
            if friend_id not in active_visited:
                active_visited[friend_id] = current_distance + 1
                active_queue.append(friend_id)

        # If we didn't find an intersection this turn, return -1 to keep the loop going
        return -1

    # --- THE CORE ENGINE ---
    # Keep searching as long as BOTH lines have people in them.
    # If one line goes empty, it means we hit a dead end and they aren't connected.
    while start_queue and target_queue:

        # THE MASSIVE OPTIMIZATION: Always expand the smaller line.
        # If the target is a celebrity with 30 million friends, and you have 100,
        # len(start_queue) will be smaller, so the computer will safely search your friends first.
        if len(start_queue) <= len(target_queue):
            # Send the search party from the Start side
            intersection_result = expand_search_party(start_queue, start_visited, target_visited)
        else:
            # Send the search party from the Target side
            intersection_result = expand_search_party(target_queue, target_visited, start_visited)

        # If the helper function found the intersection, it will return a positive number.
        if intersection_result != -1:
            return intersection_result

    # If the loops finish and they never meet, there is no connection.
    return -1


# --- 3. TESTING THE SCENARIO ---
def main():
    # Let's create a scenario where "You" are trying to connect to "Bill Gates"
    you = Member(1, "You")
    friend_a = Member(2, "Friend A")
    friend_b = Member(3, "Friend B")
    mutual_connection = Member(4, "Tech Recruiter")
    bill_gates = Member(5, "Bill Gates")

    # Bill Gates' millions of followers (we will just make 5 fake ones for this test)
    follower_1 = Member(101, "Follower 1")
    follower_2 = Member(102, "Follower 2")
    follower_3 = Member(103, "Follower 3")
    follower_4 = Member(104, "Follower 4")
    follower_5 = Member(105, "Follower 5")

    # Build the network graph
    graph = {
        # Your small circle
        you.member_id: [friend_a.member_id, friend_b.member_id],
        friend_a.member_id: [you.member_id],
        friend_b.member_id: [you.member_id, mutual_connection.member_id],

        # The bridge
        mutual_connection.member_id: [friend_b.member_id, bill_gates.member_id],

        # Bill Gates' massive circle
        bill_gates.member_id: [
            mutual_connection.member_id,
            follower_1.member_id, follower_2.member_id,
            follower_3.member_id, follower_4.member_id, follower_5.member_id
        ],

        follower_1.member_id: [bill_gates.member_id],
        follower_2.member_id: [bill_gates.member_id],
        follower_3.member_id: [bill_gates.member_id],
        follower_4.member_id: [bill_gates.member_id],
        follower_5.member_id: [bill_gates.member_id],
    }

    print("--- Running Optimized Bidirectional Search ---")
    distance = get_bidirectional_distance(graph, you.member_id, bill_gates.member_id)

    print(f"Distance from You to Bill Gates: {distance} steps.")
    # Path is: You(1) -> Friend B(3) -> Tech Recruiter(4) -> Bill Gates(5) = 3 steps!


if __name__ == "__main__":
    main()