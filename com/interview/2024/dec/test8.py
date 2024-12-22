from collections import deque


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def spiral_order(root):
    if not root:
        return []
    result = []
    dq = deque([root])
    left_to_right = True  # Start as True so first level is normal, second level reversed, etc.
    while dq:
        level_size = len(dq)
        level_vals = []
        for _ in range(level_size):
            node = dq.popleft()
            level_vals.append(node.val)
            if node.left:
                dq.append(node.left)
            if node.right:
                dq.append(node.right)

        # If left_to_right is False, reverse the level values before adding
        if left_to_right:
            result.extend(level_vals)
        else:
            result.extend(level_vals[::-1])

        left_to_right = not left_to_right
    return result


if __name__ == "__main__":
    # Build the given test tree
    #            1
    #         /     \
    #        2       3
    #     /  \     /  \
    #    4    5   6    7
    #   /  \
    #  8    9
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)
    root.left.left.left = Node(8)
    root.left.left.right = Node(9)

    # Expected: 1 3 2 4 5 6 7 9 8
    print(" ".join(map(str, spiral_order(root))))
