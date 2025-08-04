# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val            # Node's value
        self.left = left          # Left child (TreeNode or None)
        self.right = right        # Right child (TreeNode or None)

def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Finds the LCA of nodes p and q in a BST rooted at 'root'.
    """
    # Traverse from the root downwards
    current = root
    while current:
        # If both p and q are smaller than current, go left
        if p.val < current.val and q.val < current.val:
            current = current.left
        # If both p and q are greater than current, go right
        elif p.val > current.val and q.val > current.val:
            current = current.right
        else:
            # We've found the split point: this is the LCA
            return current
    return None  # In a valid BST with p and q present, this won't be reached

def build_bst_from_list(vals):
    """
    Builds a BST by inserting values from the list in order.
    Returns the root of the BST.
    """
    if not vals:
        return None
    root = TreeNode(vals[0])
    for v in vals[1:]:
        insert_into_bst(root, v)
    return root

def insert_into_bst(root: TreeNode, val: int):
    """
    Inserts 'val' into the BST rooted at 'root'.
    """
    current = root
    while True:
        if val < current.val:
            # go left
            if current.left:
                current = current.left
            else:
                current.left = TreeNode(val)
                return
        else:
            # go right (duplicates go right by convention)
            if current.right:
                current = current.right
            else:
                current.right = TreeNode(val)
                return

def main():
    """
    Runs test cases for lowestCommonAncestor and prints PASS/FAIL.
    """
    test_cases = []
    # Example tree from problem statement
    vals = [6,2,8,0,4,7,9,3,5]
    root = build_bst_from_list(vals)

    # Prepare nodes p and q references by searching
    def find(node, val):
        """ Helper to find a node by value. """
        while node:
            if val == node.val:
                return node
            node = node.left if val < node.val else node.right
        return None

    # Provided examples
    test_cases.append((2, 8, 6))
    test_cases.append((2, 4, 2))
    test_cases.append((0, 5, 2))
    # Edge case: both nodes are the same
    test_cases.append((3, 3, 3))
    # Skewed tree large input test
    skew_vals = list(range(1, 10001))  # 1→2→3→...→10000 (all right children)
    skew_root = build_bst_from_list(skew_vals)
    test_cases.append((1, 10000, 1))     # LCA is the root in a right-skewed tree

    all_passed = True
    for p_val, q_val, expected in test_cases:
        # pick right root for the test
        tree_root = skew_root if max(p_val, q_val) > 9 else root
        p_node = find(tree_root, p_val)
        q_node = find(tree_root, q_val)
        lca = lowestCommonAncestor(tree_root, p_node, q_node)
        result = lca.val if lca else None
        if result == expected:
            print(f"Test ({p_val}, {q_val}) → Expected {expected}, Got {result}: PASS")
        else:
            print(f"Test ({p_val}, {q_val}) → Expected {expected}, Got {result}: FAIL")
            all_passed = False

    if all_passed:
        print("✅ All tests passed.")
    else:
        print("❌ Some tests failed.")

if __name__ == "__main__":
    main()