# Define a message structure to carry node count and direction information
class Message:
    def __init__(self, count=1, direction='right'):
        self.count = count
        self.direction = direction  # Direction of message movement ('right' or 'left')

# Node representation for simulating a network of nodes
class Node:
    def __init__(self, is_leftmost=False, is_rightmost=False):
        self.is_leftmost = is_leftmost  # Flag if node is leftmost
        self.is_rightmost = is_rightmost  # Flag if node is rightmost
        self.left_neighbor = None  # Reference to left neighbor
        self.right_neighbor = None  # Reference to right neighbor
        self.node_count = None  # Final node count stored here

    # Sends a message to the left neighbor node
    def send_left(self, msg):
        if self.left_neighbor:
            self.left_neighbor.on_receive_right(msg)

    # Sends a message to the right neighbor node
    def send_right(self, msg):
        if self.right_neighbor:
            self.right_neighbor.on_receive_left(msg)

    # Handles message reception from the left neighbor
    def on_receive_left(self, msg):
        if msg.direction == 'right':
            msg.count += 1  # Increment count upon receiving from left
            if self.is_rightmost:
                msg.direction = 'left'  # Change message direction at rightmost node
                self.node_count = msg.count  # Set the final count for rightmost node
                self.send_left(msg)  # Begin sending the count back
            else:
                self.send_right(msg)  # Continue sending rightward

    # Handles message reception from the right neighbor
    def on_receive_right(self, msg):
        if msg.direction == 'left':
            self.node_count = msg.count  # Set the final count
            if not self.is_leftmost:
                self.send_left(msg)  # Continue sending leftward

    # Initiates the counting process from the leftmost node
    def main(self):
        if self.is_leftmost:
            msg = Message(count=1, direction='right')
            self.send_right(msg)

# Testing function for various node network scenarios
def main():
    # Basic test with 5 nodes
    nodes = [Node(is_leftmost=(i == 0), is_rightmost=(i == 4)) for i in range(5)]
    for i in range(1, 5):
        nodes[i - 1].right_neighbor = nodes[i]
        nodes[i].left_neighbor = nodes[i - 1]

    nodes[0].main()  # Start message passing from the leftmost node

    # Verify node count correctness for basic test
    correct_count = 5
    for node in nodes:
        result = 'PASS' if node.node_count == correct_count else 'FAIL'
        print(f'Node count: {node.node_count}, Expected: {correct_count}, Result: {result}')

    # Extensive test with 1000 nodes
    large_nodes = [Node(is_leftmost=(i == 0), is_rightmost=(i == 999)) for i in range(1000)]
    for i in range(1, 1000):
        large_nodes[i - 1].right_neighbor = large_nodes[i]
        large_nodes[i].left_neighbor = large_nodes[i - 1]

    large_nodes[0].main()  # Start message passing from the leftmost node

    correct_large_count = 1000
    all_pass = all(node.node_count == correct_large_count for node in large_nodes)
    print(f'Large scenario result: {"PASS" if all_pass else "FAIL"}')

# Execute the testing function
if __name__ == '__main__':
    main()
