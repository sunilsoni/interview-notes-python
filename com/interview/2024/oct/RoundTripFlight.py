import bisect


class RoundTripFlight:

    def find_last_round_trip_time(self, a2b, b2a, trips):
        current_time = 0

        for _ in range(trips):
            # Find the next available flight from A to B
            idx_a2b = bisect.bisect_left(a2b, current_time)
            if idx_a2b == len(a2b):  # No more flights available
                return -1
            # Update the current time to when the flight lands at B
            current_time = a2b[idx_a2b] + 100

            # Find the next available flight from B to A
            idx_b2a = bisect.bisect_left(b2a, current_time)
            if idx_b2a == len(b2a):  # No more flights available
                return -1
            # Update the current time to when the flight lands at A
            current_time = b2a[idx_b2a] + 100

        return current_time


# Test cases
if __name__ == "__main__":
    solver = RoundTripFlight()

    # Test case 1
    a2b = [0, 200, 500]
    b2a = [99, 210, 450]
    trips = 1
    print(solver.find_last_round_trip_time(a2b, b2a, trips))  # Expected output: 310

    # Test case 2
    a2b = [109, 200, 500]
    b2a = [99, 210, 600]
    trips = 2
    print(solver.find_last_round_trip_time(a2b, b2a, trips))  # Expected output: 700

    # Test case 3
    a2b = [5, 206]
    b2a = [105, 306]
    trips = 2
    print(solver.find_last_round_trip_time(a2b, b2a, trips))  # Expected output: 406
