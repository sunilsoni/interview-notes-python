class LoadBalancer:

    def solution(self, serversPowers, events):
        num_servers = len(serversPowers)
        requests_count = [0] * num_servers
        capacity_left = serversPowers[:]
        failed_servers = set()
        current_server = 0

        for event in events:
            if event.startswith("REQUEST"):
                # Find the next available server with capacity and that is not failed
                while current_server in failed_servers or capacity_left[current_server] == 0:
                    current_server = (current_server + 1) % num_servers

                # Process the request on the current server
                requests_count[current_server] += 1
                capacity_left[current_server] -= 1

                # Move to the next server (cyclically)
                current_server = (current_server + 1) % num_servers

            elif event.startswith("FAIL"):
                # Mark the specified server as failed
                fail_index = int(event.split()[1])
                failed_servers.add(fail_index)

            # Check if all non-failed servers are at full capacity
            if all(capacity_left[i] == 0 or i in failed_servers for i in range(num_servers)):
                # Reset the capacity of non-failed servers
                for i in range(num_servers):
                    if i not in failed_servers:
                        capacity_left[i] = serversPowers[i]

        # Find the server with the highest number of requests
        max_requests = max(requests_count)
        result_server = max(i for i, count in enumerate(requests_count) if count == max_requests)

        return result_server


# Test cases
if __name__ == "__main__":
    lb = LoadBalancer()

    # Test case 1: Original failing case
    serversPowers = [2, 3]
    events = ["REQUEST", "REQUEST"]
    print(lb.solution(serversPowers, events))  # Expected output: 0

    # Test case 2: Test from the prompt
    serversPowers = [1, 2, 1, 2, 1]
    events = ["REQUEST", "REQUEST", "FAIL 2", "REQUEST", "FAIL 3", "REQUEST", "REQUEST"]
    print(lb.solution(serversPowers, events))  # Expected output: 1

    # Test case 3: All servers have different capacities
    serversPowers = [3, 3, 3]
    events = ["REQUEST", "REQUEST", "REQUEST", "REQUEST", "REQUEST", "REQUEST", "REQUEST"]
    print(lb.solution(serversPowers, events))  # Expected output: 2

    # Test case 4: Servers fail after a few requests
    serversPowers = [2, 2, 2]
    events = ["REQUEST", "REQUEST", "FAIL 1", "REQUEST", "FAIL 2", "REQUEST"]
    print(lb.solution(serversPowers, events))  # Expected output: 0

    # Test case 5: Server 0 processes all requests
    serversPowers = [5, 1]
    events = ["REQUEST", "REQUEST", "REQUEST", "REQUEST", "REQUEST"]
    print(lb.solution(serversPowers, events))  # Expected output: 0
