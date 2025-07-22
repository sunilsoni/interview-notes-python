def main():
    def createBST():
        # Same BST creation code...
        pass

    root = createBST()

    # Now we need to find the actual nodes to pass
    def findNode(root, value):
        if not root:
            return None
        if root.val == value:
            return root
        if value < root.val:
            return findNode(root.left, value)
        return findNode(root.right, value)

    # Test cases using nodes
    test_cases = [
        {"p": findNode(root, 2), "q": findNode(root, 8), "expected": 6},
        {"p": findNode(root, 2), "q": findNode(root, 4), "expected": 2},
        # ... other test cases
    ]

    for i, test in enumerate(test_cases, 1):
        result = findLCA(root, test["p"], test["q"]).val
        # ... rest of the testing code
def findLCA(root, p, q):
    # Base case: if root is None or matches either p or q
    if not root or root == p or root == q:  # Compare nodes, not values
        return root

    # If p and q are both smaller than root, LCA must be in left subtree
    if p.val < root.val and q.val < root.val:  # Compare .val
        return findLCA(root.left, p, q)

    # If p and q are both larger than root, LCA must be in right subtree
    if p.val > root.val and q.val > root.val:  # Compare .val
        return findLCA(root.right, p, q)

    # If one value is smaller and other is larger, root is the LCA
    return root
