import time
from threading import Thread, Lock, Event


class RateLimiter:
    def __init__(self, rate_per_second):
        """
        rate_per_second: number of tokens (requests) allowed per second.
        """
        self.rate = rate_per_second

        # Start with a 'full' bucket (float to allow fractional increments)
        self.tokens = float(rate_per_second)

        # Track the last time we refilled tokens
        self.last_refill = time.time()

        # A lock to protect concurrent access to 'self.tokens'
        # (Fixes the race condition problem)
        self.lock = Lock()

        # An event to signal the background thread to stop gracefully
        self.stop_event = Event()

        # We'll store the refill thread here once we start it
        self.refill_thread = None

    def start(self):
        """
        Start the background thread that continuously refills tokens.
        """
        self.refill_thread = Thread(target=self._add_tokens, daemon=True)
        self.refill_thread.start()

    def stop(self):
        """
        Signal the background thread to stop and wait for it to finish.
        """
        self.stop_event.set()
        if self.refill_thread is not None:
            self.refill_thread.join()

    def _add_tokens(self):
        """
        Continuously add tokens according to how much time has passed,
        until 'stop_event' is set.

        This implements the 'token bucket' approach by calculating how
        many tokens to add based on elapsed time, rather than resetting
        them all at once every second.
        """
        while not self.stop_event.is_set():
            # Sleep briefly to avoid busy looping. This also helps
            # distribute token refills more smoothly (rather than
            # waiting a full second).
            time.sleep(0.01)

            now = time.time()
            with self.lock:
                # Calculate how much time has passed since we last refilled
                elapsed = now - self.last_refill
                self.last_refill = now

                # Tokens to add is rate * elapsed_time
                tokens_to_add = elapsed * self.rate

                # Increase tokens but do not exceed the max (self.rate)
                self.tokens = min(self.rate, self.tokens + tokens_to_add)

    def check(self):
        """
        Check if a request is allowed:
        - Returns True (and decrements a token) if allowed.
        - Returns False if no tokens are available.
        """
        with self.lock:
            # Only allow if we have at least 1 token
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                return False


def send_request(rate_limiter, idx):
    """
    Simulates a request being sent and checks if it is allowed
    by the rate limiter.
    """
    # Just add a small delay so the requests don't happen instantaneously
    time.sleep(0.05)

    # Use the rate limiter to see if we're allowed to proceed
    if rate_limiter.check():
        status = "accepted"
    else:
        status = "rejected"

    print(f"Request {idx} -> {status}")


if __name__ == "__main__":
    # Example usage of the rate limiter
    rate_limiter = RateLimiter(rate_per_second=5)
    rate_limiter.start()

    # Create multiple threads to simulate concurrent requests
    threads = []
    for i in range(20):
        t = Thread(target=send_request, args=(rate_limiter, i))
        t.start()
        threads.append(t)

    # Wait for all request threads to finish
    for t in threads:
        t.join()

    # Gracefully stop the rate limiter's refill thread
    rate_limiter.stop()
