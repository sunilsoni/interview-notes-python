class FrequentElement:
    def find_most_frequent(self, data):
        """
        Finds the most frequent element in a list.

        Args:
            data: A list of elements.

        Returns:
            The most frequent element, or None if the list is empty.
        """
        if not data:  # Check if the list is empty.
            return None

        counts = {}  # Initialize a dictionary to store element counts.
        for element in data:  # Iterate through each element in the list.
            if element in counts:  # Check if the element is already in the counts dictionary.
                counts[element] += 1  # Increment the count if it exists.
            else:
                counts[element] = 1  # Initialize the count to 1 if it doesn't exist.

        most_frequent = None  # Initialize the most frequent element to None.
        max_count = 0  # Initialize the maximum count to 0.

        for element, count in counts.items():  # Iterate through the element counts.
            if count > max_count:  # Check if the current count is greater than the maximum count.
                max_count = count  # Update the maximum count.
                most_frequent = element  # Update the most frequent element.

        return most_frequent  # Return the most frequent element.

    def run_tests(self):
        """
        Runs test cases to validate the find_most_frequent method.
        """
        test_cases = [
            ([1, 3, 2, 1, 4, 1, 3, 3, 3], 3),
            ([1, 1, 1, 2, 2], 1),
            ([1], 1),
            ([], None),
            ([1, 2, 3, 4, 5], 1), # if all unique, return the first one.
            ([5, 5, 5, 5, 5, 1, 1, 1, 1, 1, 2, 2], 5), # Test case with large count difference
            ([1, 1, 1, 2, 2, 2, 3, 3, 3], 1), # if there are multiple most frequent, return the first one.
            list(range(10000)) + [9999]*10001, 9999 # large data test case.
        ]

        results = []
        for data, expected in test_cases:
            actual = self.find_most_frequent(data)
            if actual == expected:
                results.append("PASS")
            else:
                results.append(f"FAIL: Expected {expected}, got {actual}")

        for result in results:
            print(result)

# Example usage and testing
frequent_element = FrequentElement()
frequent_element.run_tests()