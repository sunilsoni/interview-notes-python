# Define class for tree node
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val      # The value at this node (0-9)
        self.left = left    # Left child node
        self.right = right  # Right child node

# Main function to calculate total sum of all root-to-leaf numbers
def sum_root_to_leaf(root):
    """
    Given the root of a binary tree, return the sum of all numbers formed by root-to-leaf paths.
    Each path creates a number by concatenating node values.
    """

    # Inner helper function for DFS traversal
    def dfs(node, current_number):
        # Base case: if the node is None, return 0 (no path)
        if not node:
            return 0

        # Update the number formed so far: shift digits left and add current
        current_number = current_number * 10 + node.val

        # If it's a leaf node, return the number formed so far
        if not node.left and not node.right:
            return current_number

        # Recursively compute sum for left and right subtrees
        left_sum = dfs(node.left, current_number)
        right_sum = dfs(node.right, current_number)

        # Return total sum from both branches
        return left_sum + right_sum

    # Start DFS from the root with current_number = 0
    return dfs(root, 0)

def main():
    # Build the test tree manually
    # Structure:
    #         2
    #        / \
    #       3   4
    #      / \
    #     1   5

    root = TreeNode(2)
    root.left = TreeNode(3)
    root.right = TreeNode(4)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(5)

    # Expected sum: 231 + 235 + 24 = 490
    expected_output = 490
    result = sum_root_to_leaf(root)

    # Print test result
    print("Test 1 - Basic Tree")
    print("Expected:", expected_output)
    print("Got     :", result)
    print("Result  :", "PASS" if result == expected_output else "FAIL")
    print("-" * 50)

    # Edge Case: Empty Tree
    root = None
    expected_output = 0
    result = sum_root_to_leaf(root)
    print("Test 2 - Empty Tree")
    print("Expected:", expected_output)
    print("Got     :", result)
    print("Result  :", "PASS" if result == expected_output else "FAIL")
    print("-" * 50)

    # Edge Case: Single Node
    root = TreeNode(9)
    expected_output = 9
    result = sum_root_to_leaf(root)
    print("Test 3 - Single Node Tree")
    print("Expected:", expected_output)
    print("Got     :", result)
    print("Result  :", "PASS" if result == expected_output else "FAIL")
    print("-" * 50)

if __name__ == "__main__":
    main()