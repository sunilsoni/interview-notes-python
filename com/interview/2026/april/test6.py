def extractErrorLogs(logs):
    # Create an empty list to store the logs that meet our filtering criteria
    filtered_logs = []

    # Loop through every single log entry in the provided 2D array
    for log in logs:
        # Extract the status string, which is always located at index 2
        status = log[2]

        # Check if the status is strictly equal to "ERROR" or "CRITICAL"
        if status == "ERROR" or status == "CRITICAL":
            # If the condition is met, add this entire log entry to our filtered list
            filtered_logs.append(log)

    # Define a helper function to act as our custom sorting logic (the "key")
    def get_sort_key(log):
        # Grab the date string from the log, located at index 0 (e.g., "01-01-2023")
        date_str = log[0]

        # Grab the time string from the log, located at index 1 (e.g., "14:00")
        time_str = log[1]

        # Split the date string using the dash '-' to separate day, month, and year
        # This assigns "01" to day, "01" to month, and "2023" to year
        day, month, year = date_str.split('-')

        # Return a tuple ordered from largest time unit to smallest (Year, Month, Day, Time)
        # Python will use this tuple to compare logs. It checks Year first, then Month, etc.
        # This bypasses the need for the datetime module entirely.
        return (year, month, day, time_str)

    # Sort the filtered list in-place using our custom key function
    # Python's sort is naturally 'stable', meaning if two logs return the exact same
    # tuple from get_sort_key, they will stay in the exact order they originally appeared.
    filtered_logs.sort(key=get_sort_key)

    # Return the final array which is now both filtered and correctly sorted
    return filtered_logs


def run_tests():
    print("Starting Tests...\n")

    # --- TEST CASE 1: Standard Example from Screenshot ---
    logs1 = [
        ["01-01-2023", "14:00", "ERROR", "failed"],
        ["01-01-2023", "15:00", "INFO", "established"],
        ["01-01-2023", "01:30", "ERROR", "failed"]
    ]
    expected1 = [
        ["01-01-2023", "01:30", "ERROR", "failed"],
        ["01-01-2023", "14:00", "ERROR", "failed"]
    ]
    result1 = extractErrorLogs(logs1)
    if result1 == expected1:
        print("Test Case 1 (Standard): PASS")
    else:
        print("Test Case 1 (Standard): FAIL")
        print(f"Expected: {expected1}\nGot: {result1}")

    # --- TEST CASE 2: Filtering CRITICAL and Stability Check ---
    # Testing multiple items on the exact same date and time to ensure original order is kept
    logs2 = [
        ["31-12-2023", "23:59", "CRITICAL", "system down"],  # Should be last
        ["15-05-2022", "12:00", "ERROR", "disk full 1"],  # Same time as below
        ["15-05-2022", "12:00", "ERROR", "disk full 2"],  # Same time as above
        ["15-05-2022", "12:00", "INFO", "ignore me"],  # Should be filtered out
        ["01-01-2020", "00:00", "CRITICAL", "kernel panic"]  # Should be first
    ]
    expected2 = [
        ["01-01-2020", "00:00", "CRITICAL", "kernel panic"],
        ["15-05-2022", "12:00", "ERROR", "disk full 1"],
        ["15-05-2022", "12:00", "ERROR", "disk full 2"],
        ["31-12-2023", "23:59", "CRITICAL", "system down"]
    ]
    result2 = extractErrorLogs(logs2)
    if result2 == expected2:
        print("Test Case 2 (Stability & CRITICAL): PASS")
    else:
        print("Test Case 2 (Stability & CRITICAL): FAIL")

    # --- TEST CASE 3: Large Data Simulation ---
    # Generating 100,000 logs to ensure no stack overflows or timeout issues
    logs3 = []
    for i in range(100000):
        # Alternate between ERROR and INFO
        status = "ERROR" if i % 2 == 0 else "INFO"
        # Make the date tick upwards so they are technically in order already
        # We just want to make sure it processes 100k records quickly
        logs3.append(["01-01-2024", "12:00", status, "msg"])

    import time
    start_time = time.time()
    result3 = extractErrorLogs(logs3)
    end_time = time.time()

    # Half of 100,000 should be filtered
    if len(result3) == 50000 and (end_time - start_time) < 1.0:
        print("Test Case 3 (Large Data - 100k rows): PASS (Processed in {:.4f} seconds)".format(end_time - start_time))
    else:
        print("Test Case 3 (Large Data): FAIL")


if __name__ == '__main__':
    run_tests()