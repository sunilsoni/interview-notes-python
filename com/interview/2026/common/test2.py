def solution(departure_times, current_time):
    # Convert HH:MM to total minutes
    def to_min(t):
        h, m = map(int, t.split(':'))
        return h * 60 + m

    now = to_min(current_time)
    last_bus = -1

    # Times are chronological; find the latest one strictly before 'now'
    for dt in departure_times:
        bus_min = to_min(dt)
        if bus_min < now:
            last_bus = bus_min
        else:
            break

    return now - last_bus if last_bus != -1 else -1


def test():
    test_cases = [
        # Provided examples
        (["12:30", "14:00", "19:55"], "14:30", 30),
        (["00:00", "14:00", "19:55"], "00:00", -1),
        (["12:30", "14:00", "19:55"], "14:00", 90),
        # Edge cases: No buses before time
        (["08:00", "09:00"], "07:59", -1),
        # Edge cases: Last bus of the day
        (["08:00", "23:58"], "23:59", 1),
        # Large data simulation
        ([f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 15)], "23:59", 14)
    ]

    for i, (deps, curr, expected) in enumerate(test_cases):
        result = solution(deps, curr)
        status = "PASS" if result == expected else f"FAIL (Got {result}, Expected {expected})"
        print(f"Test Case {i + 1}: {status}")


if __name__ == "__main__":
    test()