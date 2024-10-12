class LoadBalancer:
    def __init__(self, serversPowers):
        self.powers = serversPowers
        self.capacities = serversPowers.copy()
        self.active = [True] * len(serversPowers)
        self.requests_served = [0] * len(serversPowers)
        self.current_server = 0

    def process_request(self):
        start = self.current_server
        while True:
            if self.active[self.current_server] and self.capacities[self.current_server] > 0:
                self.capacities[self.current_server] -= 1
                self.requests_served[self.current_server] += 1
                self.current_server = (self.current_server + 1) % len(self.powers)
                return
            self.current_server = (self.current_server + 1) % len(self.powers)
            if self.current_server == start:
                self.reset_capacities()

    def fail_server(self, index):
        self.active[index] = False

    def reset_capacities(self):
        for i in range(len(self.powers)):
            if self.active[i]:
                self.capacities[i] = self.powers[i]

    def get_most_served_server(self):
        max_requests = max(self.requests_served)
        for i in range(len(self.requests_served) - 1, -1, -1):
            if self.requests_served[i] == max_requests:
                return i


def solution(serversPowers, events):
    lb = LoadBalancer(serversPowers)
    for event in events:
        if event == "REQUEST":
            lb.process_request()
        elif event.startswith("FAIL"):
            server_index = int(event.split()[1])
            lb.fail_server(server_index)
    return lb.get_most_served_server()


class Solution:
    def solution(self, serversPowers, events):
        return solution(serversPowers, events)


def main():
    sol = Solution()

    # Test cases
    test_cases = [
        ([1, 2, 1, 2, 1], ["REQUEST", "REQUEST", "FAIL 2", "REQUEST", "FAIL 3", "REQUEST", "REQUEST"], 1),
        ([5, 5, 5], ["REQUEST", "REQUEST", "REQUEST", "REQUEST", "REQUEST", "REQUEST"], 1),
        ([1, 1, 1, 1], ["REQUEST", "FAIL 0", "FAIL 1", "REQUEST", "FAIL 2", "REQUEST"], 3),
        ([3, 3, 3], ["REQUEST", "REQUEST", "FAIL 0", "REQUEST", "REQUEST", "FAIL 1", "REQUEST"], 2),
    ]

    for i, (serversPowers, events, expected) in enumerate(test_cases, 1):
        result = sol.solution(serversPowers, events)
        print(f"Test case {i}:")
        print(f"Input: serversPowers = {serversPowers}, events = {events}")
        print(f"Output: {result}")
        print(f"Expected: {expected}")
        print("Pass" if result == expected else "Fail")
        print()


if __name__ == "__main__":
    main()
