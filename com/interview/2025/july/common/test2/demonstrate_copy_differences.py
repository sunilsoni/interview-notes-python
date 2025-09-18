# Importing copy module which provides deepcopy functionality
import copy


def demonstrate_copy_differences():
    # Creating a nested list to demonstrate the difference
    # Using a list with another list inside to show nested structure
    original_list = [1, [2, 3], 4]

    # Creating a shallow copy using the slice operator [:]
    # Shallow copy creates a new list but references same nested objects
    shallow_copy = original_list[:]

    # Creating a deep copy using copy.deepcopy()
    # Deep copy creates completely new copy including nested objects
    deep_copy = copy.deepcopy(original_list)

    # Modifying the nested list in original to show the difference
    original_list[1][0] = 'modified'

    return original_list, shallow_copy, deep_copy


def test_copies():
    # Test case 1: Basic nested list
    original, shallow, deep = demonstrate_copy_differences()

    print("\nTest Case 1: Basic nested list")
    print(f"Original List: {original}")
    print(f"Shallow Copy: {shallow}")
    print(f"Deep Copy: {deep}")

    # Test case 2: Large nested structure
    large_list = [[i, [i + 1, i + 2]] for i in range(1000)]
    large_shallow = large_list[:]
    large_deep = copy.deepcopy(large_list)

    # Modify first nested element
    large_list[0][1][0] = 'modified'

    print("\nTest Case 2: Large data structure")
    print(f"First element of Original: {large_list[0]}")
    print(f"First element of Shallow Copy: {large_shallow[0]}")
    print(f"First element of Deep Copy: {large_deep[0]}")

    # Verify test results
    test_passed = (
            shallow[1][0] == 'modified' and  # Shallow copy should reflect changes
            deep[1][0] == 2  # Deep copy should remain unchanged
    )

    print("\nTest Results:")
    print(f"Test {'PASSED' if test_passed else 'FAILED'}")


# Main execution
if __name__ == "__main__":
    test_copies()
