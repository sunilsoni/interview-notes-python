class LoadBalancer:

    def solution(self, serversPowers, events):
        num_servers = len(serversPowers)
        requests_count = [0] * num_servers
        capacity_left = serversPowers[:]
        failed_servers = set()

        current_server = 0

        for event in events:
            if event.startswith("REQUEST"):
                while current_server in failed_servers or capacity_left[current_server] == 0:
                    current_server = (current_server + 1) % num_servers

                requests_count[current_server] += 1
                capacity_left[current_server] -= 1

                current_server = (current_server + 1) % num_servers

            elif event.startswith("FAIL"):
                fail_index = int(event.split()[1])
                failed_servers.add(fail_index)

            # Reset capacities for non-failed servers once all are filled
            if all(capacity_left[i] == 0 or i in failed_servers for i in range(num_servers)):
                for i in range(num_servers):
                    if i not in failed_servers:
                        capacity_left[i] = serversPowers[i]

        # Find the server with the most requests processed
        max_requests = max(requests_count)
        result_server = max(i for i, count in enumerate(requests_count) if count == max_requests)

        return result_server


# Test cases
if __name__ == "__main__":
    lb = LoadBalancer()

    # Test case 1
    serversPowers = [1, 2, 1, 2, 1]
    events = ["REQUEST", "REQUEST", "FAIL 2", "REQUEST", "FAIL 3", "REQUEST", "REQUEST"]
    print(lb.solution(serversPowers, events))  # Expected output: 1
