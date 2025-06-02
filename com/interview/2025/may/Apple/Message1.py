# Message type: count message or "result" message
class Message:
    def __init__(self, count, is_return=False):
        self.count = count
        self.is_return = is_return  # False: counting right; True: returning left

class Node:
    def __init__(self, is_leftmost, is_rightmost):
        self.is_leftmost = is_leftmost
        self.is_rightmost = is_rightmost
        self.left = None    # left neighbor (Node object)
        self.right = None   # right neighbor (Node object)
        self.total_nodes = None  # This will be set when counting is done

    # Simulate sendLeft: call onReceiveRight on neighbor
    def sendLeft(self, message):
        if self.left is not None:
            self.left.onReceiveRight(message)
            return 0
        return -1

    # Simulate sendRight: call onReceiveLeft on neighbor
    def sendRight(self, message):
        if self.right is not None:
            self.right.onReceiveLeft(message)
            return 0
        return -1

    # Message received from left neighbor
    def onReceiveLeft(self, message):
        if not message.is_return:
            # Forward count to right, incrementing
            if self.is_rightmost:
                # Rightmost node: know total count now
                self.total_nodes = message.count
                # Start return phase: send result back left
                self.sendLeft(Message(message.count, is_return=True))
            else:
                # Not rightmost: increment and pass right
                self.sendRight(Message(message.count + 1, is_return=False))
        else:
            # This is the return phase: broadcast result left
            self.total_nodes = message.count
            if not self.is_leftmost:
                self.sendLeft(message)

    # Message received from right neighbor
    def onReceiveRight(self, message):
        # Only possible in the return phase
        self.total_nodes = message.count
        if not self.is_leftmost:
            self.sendLeft(message)

    # Start the protocol (called by leftmost node)
    def start(self):
        if self.is_leftmost:
            # Start with count 1 (count itself)
            self.sendRight(Message(1, is_return=False))

def create_line_of_nodes(n):
    """
    Create a straight line of n nodes.
    """
    nodes = []
    for i in range(n):
        is_left = (i == 0)
        is_right = (i == n - 1)
        nodes.append(Node(is_left, is_right))
    for i in range(n):
        if i > 0:
            nodes[i].left = nodes[i - 1]
        if i < n - 1:
            nodes[i].right = nodes[i + 1]
    return nodes

# Simple testing method
def test_node_count(num_nodes, verbose=True):
    nodes = create_line_of_nodes(num_nodes)
    # Start protocol at leftmost node
    nodes[0].start()
    # Wait for protocol to complete: since our simulation is synchronous, it's done now
    results = [node.total_nodes for node in nodes]
    passed = all(count == num_nodes for count in results)
    if verbose:
        print(f"Test with {num_nodes} nodes: {'PASS' if passed else 'FAIL'}")
        print("Node results:", results)
    return passed

if __name__ == "__main__":
    # Provided test cases
    test_node_count(1)
    test_node_count(2)
    test_node_count(5)
    test_node_count(10)

    # Edge and large cases
    test_node_count(0)         # Edge: no nodes (should do nothing or error gracefully)
    test_node_count(1000)      # Large data test
