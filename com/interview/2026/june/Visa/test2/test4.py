# Define the function that takes the starting part name and the dataset
def get_total_quantity(parent_part, data):
    # Create an empty dictionary to act as our fast-lookup graph for parent-child relationships
    graph = {}

    # Loop through every single row (dictionary) in the provided dataset
    for row in data:
        # Extract the parent part name from the current row
        parent = row["parent_part"]
        # Extract the child part name from the current row
        child = row["child_part"]
        # Extract the required quantity to make the parent from the current row
        qty = row["qty_per"]

        # Check if the parent part does not already exist as a key in our graph dictionary
        if parent not in graph:
            # If it doesn't exist, initialize an empty list for this parent to hold its children
            graph[parent] = []

        # Append the child name and its required quantity as a tuple to the parent's list
        graph[parent].append((child, qty))

    # Create a dictionary to keep a running total of the final required quantities for each part
    results = {}

    # Create a list to act as our processing queue, starting with the root part and a multiplier of 1
    queue = [(parent_part, 1)]

    # Start a loop that will continue running as long as there are items left in our queue
    while len(queue) > 0:
        # Remove and get the first item from the queue, unpacking it into current_part and current_multiplier
        current_part, current_multiplier = queue.pop(0)

        # Check if the current part we are looking at exists in our graph (meaning it has children)
        if current_part in graph:
            # Loop through all the children and their base quantities for this specific parent part
            for child, child_base_qty in graph[current_part]:
                # Calculate the actual required quantity by multiplying the base qty by the parent's multiplier
                total_child_qty = child_base_qty * current_multiplier

                # Check if this child part hasn't been added to our final results dictionary yet
                if child not in results:
                    # If it's brand new, initialize its total count to 0 in the results dictionary
                    results[child] = 0

                # Add the calculated quantity to the child's running total in the results dictionary
                results[child] = results[child] + total_child_qty

                # Add the child and its calculated quantity to the queue so we can process its children later
                queue.append((child, total_child_qty))

    # Once the queue is completely empty, return the final populated results dictionary
    return results


# Define the main testing method to execute our pass/fail test cases
def main():
    # Define the primary test data provided in the problem description
    test_data_1 = [
        {"id": 1, "parent_part": "Part 1", "child_part": "Part 2", "qty_per": 4},
        {"id": 2, "parent_part": "Part 1", "child_part": "Part 3", "qty_per": 2},
        {"id": 3, "parent_part": "Part 2", "child_part": "Part 4", "qty_per": 1},
        {"id": 4, "parent_part": "Part 3", "child_part": "Part 5", "qty_per": 3},
        {"id": 5, "parent_part": "Part 3", "child_part": "Part 6", "qty_per": 1},
        {"id": 6, "parent_part": "Part 4", "child_part": "Part 7", "qty_per": 2},
    ]

    # Define exactly what the output should look like based on the prompt's instructions
    expected_output_1 = {
        "Part 2": 4,
        "Part 3": 2,
        "Part 4": 4,
        "Part 5": 6,
        "Part 6": 2,
        "Part 7": 8
    }

    # Execute the function using 'Part 1' as the root to test standard logic
    result_1 = get_total_quantity("Part 1", test_data_1)

    # Compare the function's output directly against our expected output
    if result_1 == expected_output_1:
        # Print a success message if the outputs match perfectly
        print("Test Case 1 (Standard BOM Explosion): PASS")
    else:
        # Print a failure message if they do not match, revealing what went wrong
        print(f"Test Case 1 (Standard BOM Explosion): FAIL. Got {result_1}")

    # Initialize an empty list to generate a massive dataset for performance testing
    large_data = []
    # Create a deep chain of 100 parts where each part requires 2 of the next part
    for i in range(1, 100):
        # Append a new dictionary representing a parent needing 2 of a child part
        large_data.append({"id": i, "parent_part": f"Part {i}", "child_part": f"Part {i + 1}", "qty_per": 2})

    # Execute the function using 'Part 1' to traverse all 100 levels of the chain
    result_2 = get_total_quantity("Part 1", large_data)

    # In a chain of 100 parts where qty doubles each step, Part 100 should require 2^99 units
    expected_final_qty = 2 ** 99

    # Check if the final part in the chain calculated the massive number correctly
    if "Part 100" in result_2 and result_2["Part 100"] == expected_final_qty:
        # Print a success message to confirm large-scale data handling and massive integer math works
        print("Test Case 2 (Large Data - 100 Deep Chain): PASS")
    else:
        # Print a failure message if the large data failed to process correctly
        print("Test Case 2 (Large Data - 100 Deep Chain): FAIL")


# Standard Python check to ensure the main function only runs if the script is executed directly
if __name__ == "__main__":
    # Call the main function to trigger all the tests
    main()