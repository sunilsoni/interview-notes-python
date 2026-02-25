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


# Our robust, out-of-order proof logger
class RobustLogger(ILogger):

    def __init__(self):
        # We keep our fast-search list for timestamps.
        self.timestamps = []
        # We keep our parallel list for the full log data.
        self.logs = []

    def add_log(self, timestamp: datetime, message: str, level: str = "INFO") -> None:
        # Instead of appending to the end, we find the EXACT index where this timestamp SHOULD go to keep the list sorted.
        # bisect_right finds this chronological index instantly.
        insert_index = bisect.bisect_right(self.timestamps, timestamp)

        # Now, we insert the timestamp right into that calculated slot.
        # This shifts any newer logs one position to the right to make room.
        self.timestamps.insert(insert_index, timestamp)

        # We bundle the full log details together into a tuple.
        log_entry = (timestamp, message, level)

        # We insert the bundled tuple into our main storage list at the EXACT SAME calculated index.
        # This guarantees our timestamps list and our logs list match perfectly.
        self.logs.insert(insert_index, log_entry)

    def get_logs(self, start: datetime, end: datetime, level: Optional[str] = None) -> List[str]:
        # The retrieval logic remains identically fast to our previous version!

        # Find the FIRST index where the timestamp is >= start.
        start_index = bisect.bisect_left(self.timestamps, start)

        # Find the FIRST index where the timestamp is > end.
        end_index = bisect.bisect_right(self.timestamps, end)

        # Prepare an empty list for the final results.
        matching_messages = []

        # Loop ONLY through the slice of logs that fall in our time window.
        for i in range(start_index, end_index):

            # Grab the log tuple from our main list using the current index.
            log_ts, log_msg, log_lvl = self.logs[i]

            # Check if we need to filter by a specific level.
            if level is None or log_lvl == level:
                # Add the matching message to our final results.
                matching_messages.append(log_msg)

        # Hand back the final list.
        return matching_messages