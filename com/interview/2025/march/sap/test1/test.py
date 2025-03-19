class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Solution 1: Recursive Approach
def isSymmetric(root):
    if not root:
        return True

    def isMirror(left, right):
        # If both nodes are None, they're symmetric
        if not left and not right:
            return True

        # If one node is None and other isn't, they're not symmetric
        if not left or not right:
            return False

        # Check if:
        # 1. Values are equal
        # 2. Left's left matches Right's right
        # 3. Left's right matches Right's left
        return (left.val == right.val and
                isMirror(left.left, right.right) and
                isMirror(left.right, right.left))

    return isMirror(root.left, root.right)


# Solution 2: Iterative Approach using Queue
from collections import deque


def isSymmetricIterative(root):
    if not root:
        return True

    queue = deque([(root.left, root.right)])

    while queue:
        left, right = queue.popleft()

        # If both are None, continue checking other nodes
        if not left and not right:
            continue

        # If one is None or values don't match, tree is not symmetric
        if not left or not right or left.val != right.val:
            return False

        # Add the outer pair
        queue.append((left.left, right.right))
        # Add the inner pair
        queue.append((left.right, right.left))

    return True


# Test cases
def test():
    # Test Case 1: Symmetric Tree
    #     1
    #    / \
    #   2   2
    #  / \ / \
    # 3  4 4  3
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(2)
    root1.left.left = TreeNode(3)
    root1.left.right = TreeNode(4)
    root1.right.left = TreeNode(4)
    root1.right.right = TreeNode(3)
    print("Test 1:", isSymmetric(root1))  # Should print True
    print("Test 1 (Iterative):", isSymmetricIterative(root1))  # Should print True

    # Test Case 2: Non-symmetric Tree
    #     1
    #    / \
    #   2   2
    #    \   \
    #    3    3
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(2)
    root2.left.right = TreeNode(3)
    root2.right.right = TreeNode(3)
    print("Test 2:", isSymmetric(root2))  # Should print False
    print("Test 2 (Iterative):", isSymmetricIterative(root2))  # Should print False


test()
