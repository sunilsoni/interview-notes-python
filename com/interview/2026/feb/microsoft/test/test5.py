import bisect
import threading  # 1. Import the threading module
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


# The interface remains exactly the same as requested
class ILogger(ABC):
    @abstractmethod
    def add_log(self, timestamp: datetime, message: str, level: str = "INFO") -> None:
        pass

    @abstractmethod
    def get_logs(self, start: datetime, end: datetime, level: Optional[str] = None) -> List[str]:
        pass


class ThreadSafeFastLogger(ILogger):

    def __init__(self):
        self.timestamps = []
        self.logs = []

        # 2. Create a Lock object. This is our "traffic light" to manage threads.
        self.lock = threading.Lock()

    def add_log(self, timestamp: datetime, message: str, level: str = "INFO") -> None:
        log_entry = (timestamp, message, level)

        # 3. We use the 'with' statement to acquire the lock. 
        # While inside this block, NO OTHER THREAD can run add_log or get_logs.
        with self.lock:
            # We safely update both lists. 
            # Because of the lock, these two operations are now "atomic" (they happen together or not at all).
            self.timestamps.append(timestamp)
            self.logs.append(log_entry)

        # 4. As soon as the code exits the 'with' block, Python automatically releases the lock!

    def get_logs(self, start: datetime, end: datetime, level: Optional[str] = None) -> List[str]:
        # 5. We also must lock the reading process. 
        # If we don't, we might try to read the lists while another thread is halfway through adding a log.
        with self.lock:
            # All the search logic remains safely inside the lock block
            start_index = bisect.bisect_left(self.timestamps, start)
            end_index = bisect.bisect_right(self.timestamps, end)

            matching_messages = []

            for i in range(start_index, end_index):
                log_ts, log_msg, log_lvl = self.logs[i]

                if level is None or log_lvl == level:
                    matching_messages.append(log_msg)

            # We hand back the finalized list. 
            # The lock is instantly released the moment we hit 'return'.
            return matching_messages