import threading
import time


class SnowflakeIDGenerator:
    def __init__(self, machine_id, epoch=1288834974657):
        self.machine_id = machine_id
        self.epoch = epoch
        self.sequence = 0
        self.lock = threading.Lock()

        self.timestamp_bits = 41
        self.machine_id_bits = 10
        self.sequence_bits = 12
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)

    def generate_id(self):
        with self.lock:
            current_timestamp = int(time.time() * 1000) - self.epoch
            if self.sequence >= self.max_sequence:
                self.sequence = 0
                time.sleep(0.001)  # Wait for next millisecond.
                current_timestamp = int(time.time() * 1000) - self.epoch

            self.sequence += 1
            snowflake_id = (current_timestamp << (self.machine_id_bits + self.sequence_bits)) | \
                           (self.machine_id << self.sequence_bits) | \
                           self.sequence
            return snowflake_id


# Example usage
machine_id = 1
generator = SnowflakeIDGenerator(machine_id)
print(generator.generate_id())
