# Example to demonstrate dictionary key behavior
def demonstrate_duplicate_keys():
    # Creating a dictionary with duplicate keys
    test_dict = {
        'a': 1,  # First value for key 'a'
        'a': 2  # Second value for key 'a' will override the first
    }

    # Print the result
    print("Dictionary with duplicate key:", test_dict)

    # Demonstrating the behavior step by step
    print("\nStep by step dictionary creation:")
    d1 = {}
    print("Initial empty dict:", d1)

    d1['a'] = 1
    print("After adding first 'a':", d1)

    d1['a'] = 2
    print("After adding second 'a':", d1)

    # Test with different data types
    test_dict2 = {
        'a': 1,
        'a': 2,
        'a': "string",
        'a': [1, 2, 3],
        'a': {'nested': 'dict'}
    }
    print("\nDictionary after multiple assignments to same key:", test_dict2)


def test_dictionary_behavior():
    print("Testing Dictionary Key Behavior...")

    # Test Case 1: Basic duplicate keys
    dict1 = {'a': 1, 'a': 2, 'b': 3}
    print("\nTest Case 1:")
    print(f"Dictionary with duplicate 'a' keys: {dict1}")
    print(f"Value of 'a': {dict1['a']}")  # Will print 2

    # Test Case 2: Multiple value types
    dict2 = {'a': 1, 'a': "string", 'a': [1, 2, 3]}
    print("\nTest Case 2:")
    print(f"Dictionary after multiple value types: {dict2}")

    # Verification
    test_results = {
        'last_value_kept': dict1['a'] == 2,
        'dict_length_correct': len(dict1) == 2  # Only 'a' and 'b' keys
    }

    print("\nTest Results:")
    for test_name, result in test_results.items():
        print(f"{test_name}: {'PASS' if result else 'FAIL'}")


if __name__ == "__main__":
    demonstrate_duplicate_keys()
    test_dictionary_behavior()
