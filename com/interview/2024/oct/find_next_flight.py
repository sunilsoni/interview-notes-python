class Solution:
    def find_next_flight(self, departures, current_time):
        for departure in departures:
            if departure >= current_time:
                return departure
        return departures[0] + 2000  # Next day's first flight

    def calculate_round_trips(self, a2b, b2a, trips):
        current_time = 0
        for _ in range(trips):
            # A to B
            departure_time = self.find_next_flight(a2b, current_time)
            current_time = departure_time + 100  # 100 minutes flight time

            # B to A
            departure_time = self.find_next_flight(b2a, current_time)
            current_time = departure_time + 100  # 100 minutes flight time

        return current_time

    def solution(self, a2b, b2a, trips):
        return self.calculate_round_trips(a2b, b2a, trips)

def main():
    sol = Solution()

    # Test cases
    test_cases = [
        ([0, 200, 500], [99, 210, 450], 1, 310),
        ([109, 200, 500], [99, 210, 600], 2, 700),
        ([5, 206], [105, 306], 2, 406),
        ([0, 100, 200], [50, 150, 250], 3, 550),
        ([0], [0], 1, 200),
        ([0, 1000], [1100, 2000], 1, 2100),
    ]

    for i, (a2b, b2a, trips, expected) in enumerate(test_cases, 1):
        result = sol.solution(a2b, b2a, trips)
        print(f"Test case {i}:")
        print(f"Input: a2b = {a2b}, b2a = {b2a}, trips = {trips}")
        print(f"Output: {result}")
        print(f"Expected: {expected}")
        print("Pass" if result == expected else "Fail")
        print()

if __name__ == "__main__":
    main()
