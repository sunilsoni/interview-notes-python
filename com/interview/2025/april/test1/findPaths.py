class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def findPaths(root, targetSum):
    # Store all valid paths
    result = []

    def dfs(node, currentSum, path):
        # Base case: empty node
        if not node:
            return

        # Add current node to path and sum
        currentSum += node.val
        path.append(node.val)

        # Check if it's a leaf node and sum matches target
        if not node.left and not node.right and currentSum == targetSum:
            result.append(path[:])  # Add copy of path

        # Recurse on left and right children
        dfs(node.left, currentSum, path)
        dfs(node.right, currentSum, path)

        # Backtrack: remove current node from path
        path.pop()

    dfs(root, 0, [])
    return result


# Test cases
def main():
    # Test Case 1: Basic tree
    root1 = TreeNode(5)
    root1.left = TreeNode(4)
    root1.right = TreeNode(8)
    root1.left.left = TreeNode(11)
    root1.left.left.left = TreeNode(7)
    root1.left.left.right = TreeNode(2)

    print("Test Case 1:")
    print("Target sum = 22")
    paths = findPaths(root1, 22)
    print(f"Paths found: {paths}")
    print("PASS" if len(paths) == 2 else "FAIL")

    # Test Case 2: Empty tree
    print("\nTest Case 2:")
    print("Empty tree")
    paths = findPaths(None, 0)
    print(f"Paths found: {paths}")
    print("PASS" if len(paths) == 0 else "FAIL")

    # Test Case 3: Single node
    root3 = TreeNode(1)
    print("\nTest Case 3:")
    print("Single node, target = 1")
    paths = findPaths(root3, 1)
    print(f"Paths found: {paths}")
    print("PASS" if len(paths) == 1 else "FAIL")


if __name__ == "__main__":
    main()
