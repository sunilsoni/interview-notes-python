import bisect
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional


# The interface remains exactly the same as requested
class ILogger(ABC):
    @abstractmethod
    def add_log(self, timestamp: datetime, message: str, level: str = "INFO") -> None:
        pass

    @abstractmethod
    def get_logs(self, start: datetime, end: datetime, level: Optional[str] = None) -> List[str]:
        pass


# Our upgraded, highly efficient logger
class FastLogger(ILogger):

    def __init__(self):
        # We create a list specifically to hold ONLY timestamps so we can search them super fast.
        self.timestamps = []
        # We create a parallel list to hold the actual complete log data (timestamp, message, level).
        self.logs = []

    def add_log(self, timestamp: datetime, message: str, level: str = "INFO") -> None:
        # We add the isolated timestamp to our fast-search list.
        self.timestamps.append(timestamp)

        # We bundle the full log details together into a tuple.
        log_entry = (timestamp, message, level)

        # We add the bundled tuple to our main storage list at the exact same index position.
        self.logs.append(log_entry)

    def get_logs(self, start: datetime, end: datetime, level: Optional[str] = None) -> List[str]:
        # bisect_left uses binary search to instantly find the FIRST index where the timestamp is >= start.
        start_index = bisect.bisect_left(self.timestamps, start)

        # bisect_right uses binary search to instantly find the FIRST index where the timestamp is > end.
        end_index = bisect.bisect_right(self.timestamps, end)

        # We prepare an empty list to hold the final messages we want to send back.
        matching_messages = []

        # Instead of looping through ALL logs, we ONLY loop from our calculated start_index to end_index.
        for i in range(start_index, end_index):

            # We grab the log tuple from our main list using the current index 'i'.
            log_ts, log_msg, log_lvl = self.logs[i]

            # We check if the user did not specify a level, OR if the log's level matches the requested level.
            if level is None or log_lvl == level:
                # If the level matches, we add the message string to our results list.
                matching_messages.append(log_msg)

        # We hand back the finalized list of messages to the user.
        return matching_messages


def run_tests():
    print("Starting FastLogger tests...\n")
    logger = FastLogger()
    base_time = datetime(2026, 1, 1, 12, 0, 0)

    # --- TEST CASE 1 & 2: Basic functionality & Level Filtering ---
    try:
        logger.add_log(base_time, "Boot", "INFO")
        logger.add_log(base_time + timedelta(minutes=5), "Low Disk", "WARNING")
        logger.add_log(base_time + timedelta(minutes=10), "Crash", "ERROR")

        all_logs = logger.get_logs(base_time, base_time + timedelta(minutes=15))
        warn_logs = logger.get_logs(base_time, base_time + timedelta(minutes=15), level="WARNING")

        if len(all_logs) == 3 and len(warn_logs) == 1:
            print("Test 1 & 2 (Basics & Filtering): PASS")
        else:
            print("Test 1 & 2 (Basics & Filtering): FAIL")
    except Exception as e:
        print(f"Tests 1 & 2 FAIL due to error: {e}")

    # --- TEST CASE 3: Massive Data Input (1 Million Logs) ---
    try:
        massive_logger = FastLogger()
        start_massive = datetime(2026, 2, 1, 0, 0, 0)

        print("Generating 1,000,000 logs... (This takes a moment)")
        # Insert 1,000,000 logs
        for i in range(1000000):
            massive_logger.add_log(start_massive + timedelta(seconds=i), f"Msg {i}", "INFO")

        # Try to retrieve a 5-second window from deep inside the 1 million logs
        search_start = start_massive + timedelta(seconds=950000)
        search_end = start_massive + timedelta(seconds=950004)

        # Because of binary search, this lookup will happen in roughly 20 steps instead of 1,000,000!
        results = massive_logger.get_logs(search_start, search_end)

        if len(results) == 5 and results[0] == "Msg 950000":
            print("Test 3 (Massive Data - 1 Million logs lookup): PASS")
        else:
            print("Test 3 (Massive Data - 1 Million logs lookup): FAIL")
    except Exception as e:
        print(f"Test 3 FAIL due to error: {e}")


if __name__ == "__main__":
    run_tests()