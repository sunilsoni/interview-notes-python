# We import deque (double-ended queue) from the collections library.
# A deque is much faster than a standard Python list when adding/removing items from the front,
# which is important for handling large data efficiently.
from collections import deque


def get_connection_distance(network, start_person, target_person):
    # First, check if the start or target person doesn't even exist in our network.
    # If either is missing, they can't possibly be connected, so return -1.
    if start_person not in network or target_person not in network:
        # Return -1 to indicate no connection is possible.
        return -1

    # Check if the start person is the exactly the same as the target person.
    if start_person == target_person:
        # If they are the same person, the distance is 0 steps.
        return 0

    # Create a queue to keep track of who we need to check next.
    # We store a "tuple" (a pair of values) inside the queue: (person_name, current_distance)
    # We start by adding the start_person with a distance of 0.
    search_queue = deque([(start_person, 0)])

    # Create a 'set' to keep track of people we have already checked.
    # Using a set is very fast for checking if someone is inside it (great for large data).
    # We add the start_person to the visited set so we don't go backwards.
    visited = set([start_person])

    # We start a loop that will keep running as long as there are people left in our queue to check.
    while search_queue:
        # Take the first person and their distance out from the left (front) of the queue.
        # This gives us the person we are currently looking at, and how many steps it took to reach them.
        current_person, current_distance = search_queue.popleft()

        # Check if the person we just pulled from the queue is the target we are looking for.
        if current_person == target_person:
            # If they are the target, we found the shortest path! Return the distance.
            return current_distance

        # If they are not the target, we need to look at all of their direct friends.
        # We use network.get(current_person, []) to get their friend list safely.
        for friend in network.get(current_person, []):
            # Check if we have ALREADY visited this friend. We only want to process new people.
            if friend not in visited:
                # If they are new, mark them as visited right now so we don't add them again later.
                visited.add(friend)
                # Add this new friend to the back (right) of the queue.
                # Because they are one step further away than the current person, their distance is current_distance + 1.
                search_queue.append((friend, current_distance + 1))

    # If the while loop finishes and the queue becomes empty, it means we checked everyone connected
    # but never found the target person.
    # Return -1 to indicate they are completely disconnected.
    return -1


def main():
    # --- TEST DATA SETUP ---
    # This is the exact network from the image provided
    graph = {
        "Bob": ["Alice", "John"],
        "Alice": ["Bob", "Frank", "Lucy"],
        "Frank": ["Alice"],
        "John": ["Bob", "Jenny"],
        "Jenny": ["John", "Lucy"],
        "Lucy": ["Jenny", "Alice"]
    }

    # Setting up a huge network to test the "large data" requirement
    large_graph = {str(i): [str(i + 1)] for i in range(100000)}
    large_graph["100000"] = []  # End of the line

    # --- TEST CASES ---
    # We define our test cases as a list of lists: [Network, Start, End, Expected_Result, Test_Name]
    tests = [
        [graph, "Bob", "Lucy", 2, "Normal connection (Bob to Alice to Lucy)"],
        [graph, "Frank", "Jenny", 3, "Longer connection (Frank to Alice to Lucy to Jenny)"],
        [graph, "Alice", "Frank", 1, "Direct friend connection"],
        [graph, "Bob", "Bob", 0, "Same person (distance 0)"],
        [graph, "Bob", "Zack", -1, "Target person does not exist in graph"],
        [graph, "Zack", "Bob", -1, "Start person does not exist in graph"],
        [large_graph, "0", "99999", 99999, "Large Data test (100,000 nodes in a line)"]
    ]

    # --- TEST RUNNER ---
    print("--- Running Tests ---")
    all_passed = True

    # Loop through every test case in our list
    for i, test in enumerate(tests):
        # Extract the variables from the test case list
        net, start, end, expected, name = test

        # Call our function with the test inputs
        result = get_connection_distance(net, start, end)

        # Check if our function's result matches the expected correct answer
        if result == expected:
            # If it matches, print a green PASS message
            print(f"[\033[92mPASS\033[0m] Test {i + 1}: {name}")
        else:
            # If it fails, print a red FAIL message with details
            print(f"[\033[91mFAIL\033[0m] Test {i + 1}: {name} | Expected: {expected}, Got: {result}")
            # Mark that at least one test failed
            all_passed = False

    print("---------------------")
    # Give a final summary of the test run
    if all_passed:
        print("RESULT: ALL TESTS PASSED SUCESSFULLY!")
    else:
        print("RESULT: SOME TESTS FAILED. PLEASE CHECK LOGS.")


# Standard Python line to make sure main() runs when the script is executed
if __name__ == "__main__":
    main()