import sys
from collections import deque

# Define a Message class to carry data between nodes.
class Message:
    def __init__(self, msg_type, count):
        """
        msg_type: "COUNT" or "RESULT"
        count: integer value representing current count or final total
        """
        self.msg_type = msg_type
        self.count = count

class Node:
    def __init__(self, index, total_nodes):
        """
        index: integer position of this node in the line [0 .. total_nodes-1]
        total_nodes: total number of nodes in the entire system
        """
        self.index = index
        self.total_nodes = total_nodes

        # Queues for incoming messages from left and right neighbors.
        self.queue_left = deque()
        self.queue_right = deque()

        # This will hold the final total once we know it (after RESULT arrives).
        self.final_count = None

        # Flags to track if we've already forwarded COUNT or RESULT.
        self.count_received = False
        self.result_received = False

    def isLeftMost(self):
        """Return True if this node is the leftmost (index == 0)."""
        return self.index == 0

    def isRightMost(self):
        """Return True if this node is the rightmost (index == total_nodes - 1)."""
        return self.index == self.total_nodes - 1

    def sendLeft(self, msg):
        """
        Simulate sending a message to the left neighbor.
        Returns -1 if no left neighbor exists, otherwise 0 for success.
        """
        if self.isLeftMost():
            return -1
        # Enqueue into left neighbor’s queue_right (because the neighbor would receive from its right).
        nodes[self.index - 1].queue_right.append(msg)
        return 0

    def sendRight(self, msg):
        """
        Simulate sending a message to the right neighbor.
        Returns -1 if no right neighbor exists, otherwise 0 for success.
        """
        if self.isRightMost():
            return -1
        # Enqueue into right neighbor’s queue_left (because the neighbor would receive from its left).
        nodes[self.index + 1].queue_left.append(msg)
        return 0

    def onReceiveLeft(self, msg):
        """
        Callback when a message arrives from left neighbor.
        This will be called by the simulation loop when we process queue_left.
        """
        # If this is a COUNT message and we haven't handled COUNT yet:
        if msg.msg_type == "COUNT" and not self.count_received:
            self.count_received = True
            # Increment count to include this node itself.
            new_count = msg.count + 1

            # If I'm rightmost, switch to Phase 2. Otherwise, forward to the right.
            if self.isRightMost():
                # Store the total count in this node.
                self.final_count = new_count
                # Start Phase 2: send RESULT back to the left neighbor.
                result_msg = Message("RESULT", new_count)
                self.sendLeft(result_msg)
            else:
                # Forward COUNT to the right, with updated count.
                count_msg = Message("COUNT", new_count)
                self.sendRight(count_msg)

        # If this is a RESULT message (coming from the right to go left):
        elif msg.msg_type == "RESULT" and not self.result_received:
            self.result_received = True
            # Store the total in this node.
            self.final_count = msg.count
            # If not the leftmost node, forward RESULT to the left.
            if not self.isLeftMost():
                result_msg = Message("RESULT", msg.count)
                self.sendLeft(result_msg)
            # If I am leftmost, I'm done. Everyone has the total now.
            # (No further action needed.)

    def onReceiveRight(self, msg):
        """
        Callback when a message arrives from right neighbor.
        In our algorithm, we never expect COUNT from right, so only RESULT arrives from right.
        """
        # This will handle RESULT messages coming from the right in Phase 2.
        if msg.msg_type == "RESULT" and not self.result_received:
            self.result_received = True
            self.final_count = msg.count
            # If not the leftmost, forward RESULT to left
            if not self.isLeftMost():
                result_msg = Message("RESULT", msg.count)
                self.sendLeft(result_msg)
            # If I'm leftmost, I'm done.

    def maybe_start(self):
        """
        Called once at the very beginning of the simulation.
        The leftmost node initiates Phase 1 by sending COUNT=1 to the right.
        """
        if self.isLeftMost():
            # Special case: if there's only one node, it is both leftmost and rightmost.
            if self.isRightMost():
                # N = 1. Set final_count immediately.
                self.final_count = 1
            else:
                # Start counting phase by sending COUNT=1 to the right neighbor.
                msg = Message("COUNT", 1)
                self.sendRight(msg)

    def process_queues(self):
        """
        Process all incoming messages in queue_left and queue_right.
        Each call can produce more messages onto neighbors' queues.
        Returns True if we processed anything, False if both queues were empty.
        """
        did_work = False

        # Process everything coming from the left
        while self.queue_left:
            did_work = True
            msg = self.queue_left.popleft()
            self.onReceiveLeft(msg)

        # Process everything coming from the right
        while self.queue_right:
            did_work = True
            msg = self.queue_right.popleft()
            self.onReceiveRight(msg)

        return did_work


# Global list of nodes, indexed by position. We'll initialize in main() below.
nodes = []

def run_simulation(n):
    """
    Create n nodes in a line, run the two-phase algorithm, and return True if every node's
    final_count == n, False otherwise.
    """
    global nodes
    nodes = [Node(i, n) for i in range(n)]

    # Step 1: Let each node call maybe_start() so the leftmost node sends COUNT=1.
    for node in nodes:
        node.maybe_start()

    # Step 2: Repeatedly process all queues until no node has any messages left.
    # We'll loop until for an entire pass no node did any work.
    while True:
        did_any_work = False
        for node in nodes:
            if node.process_queues():
                did_any_work = True
        if not did_any_work:
            break

    # Step 3: Verify that each node has final_count == n.
    all_ok = True
    for node in nodes:
        # If final_count is None or not equal to n, algorithm failed.
        if node.final_count != n:
            all_ok = False
            break

    return all_ok


if __name__ == "__main__":
    # Example invocation: accept test sizes from command line or run defaults.
    test_sizes = [1, 2, 5, 10, 100, 1000]

    # If user passed sizes as arguments, parse them:
    if len(sys.argv) > 1:
        try:
            test_sizes = [int(arg) for arg in sys.argv[1:]]
        except ValueError:
            print("Invalid arguments. Provide integers only.")
            sys.exit(1)

    # For each test size, run the simulation and print PASS/FAIL.
    for size in test_sizes:
        result = run_simulation(size)
        if result:
            print(f"Test N={size}: PASS")
        else:
            print(f"Test N={size}: FAIL")