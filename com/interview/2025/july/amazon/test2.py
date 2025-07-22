# Definition of TreeNode class for BST
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None


def findLCA(root, p, q):
    # Base case: if root is None or matches either p or q
    if not root or root.val == p or root.val == q:
        return root

    # If p and q are both smaller than root, LCA must be in left subtree
    if p < root.val and q < root.val:
        return findLCA(root.left, p, q)

    # If p and q are both larger than root, LCA must be in right subtree
    if p > root.val and q > root.val:
        return findLCA(root.right, p, q)

    # If one value is smaller and other is larger, root is the LCA
    return root


def main():
    # Helper function to create BST
    def createBST():
        root = TreeNode(6)
        root.left = TreeNode(2)
        root.right = TreeNode(8)
        root.left.left = TreeNode(0)
        root.left.right = TreeNode(4)
        root.right.left = TreeNode(7)
        root.right.right = TreeNode(9)
        root.left.right.left = TreeNode(3)
        root.left.right.right = TreeNode(5)
        return root

    # Create test cases
    test_cases = [
        {"p": 2, "q": 8, "expected": 6},
        {"p": 2, "q": 4, "expected": 2},
        {"p": 0, "q": 5, "expected": 2},
        # Additional edge cases
        {"p": 3, "q": 5, "expected": 4},
        {"p": 7, "q": 9, "expected": 8},
    ]

    # Run test cases
    root = createBST()
    for i, test in enumerate(test_cases, 1):
        result = findLCA(root, test["p"], test["q"]).val
        status = "PASS" if result == test["expected"] else "FAIL"
        print(f"Test {i}: {status}")
        print(f"Input: p={test['p']}, q={test['q']}")
        print(f"Expected: {test['expected']}, Got: {result}\n")


# Run the tests
if __name__ == "__main__":
    main()
