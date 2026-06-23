# Function to calculate cumulative quantities
def calculate_cumulative_qty(data):
    # This list will hold our final processed rows
    output_data = []

    # We define a helper function to determine how to sort each row
    def get_sort_key(row):
        # Extract the site name from the first position of the row tuple
        site = row[0]
        # Extract the MPN name from the second position of the row tuple
        mpn = row[1]
        # Extract the week string (e.g., 'Week10') from the third position
        week_str = row[2]
        # Replace the word 'Week' with an empty string to isolate the number
        week_num_str = week_str.replace('Week', '')
        # Convert the isolated number string into an actual integer for correct math sorting
        week_num = int(week_num_str)
        # Return a tuple that Python will use to sort: first by site, then mpn, then week number
        return (site, mpn, week_num)

    # Create a new list containing the sorted data using our custom sorting logic
    sorted_data = sorted(data, key=get_sort_key)

    # Initialize a variable to keep track of the running total
    running_sum = 0
    # Initialize a variable to remember the last Site and MPN we looked at
    previous_group = None

    # Start a loop to go through each row in our newly sorted data
    for row in sorted_data:
        # Unpack the row tuple into individual easy-to-read variables
        site, mpn, week, qty = row
        # Group the site and mpn together to define our current product category
        current_group = (site, mpn)

        # Check if the current product category is different from the previous one
        if current_group != previous_group:
            # If it is a new product, reset the running sum to start with the current quantity
            running_sum = qty
            # Update the previous_group tracker to be this new product category
            previous_group = current_group
        # If the product category is the exactly the same as the last row
        else:
            # Add the current quantity to our running total
            running_sum = running_sum + qty

        # Create a new tuple containing the original data plus our calculated running sum
        new_row = (site, mpn, week, qty, running_sum)
        # Add this completed new row to our final output list
        output_data.append(new_row)

    # Once the loop finishes processing all rows, return the final output list
    return output_data


# Main method to handle test cases and verify pass/fail status
def main():
    # Define the provided sample test case data, left unsorted to test sorting logic
    test_data_1 = [
        ('Site1', 'MPN1', 'Week1', 100),
        ('Site1', 'MPN1', 'Week3', 111),
        ('Site1', 'MPN1', 'Week2', 90),
        ('Site1', 'MPN1', 'Week5', 120),
        ('Site1', 'MPN1', 'Week4', 200),
        ('Site1', 'MPN1', 'Week10', 200),
        ('Site1', 'MPN1', 'Week11', 300),
        ('Site1', 'MPN2', 'Week2', 240),
        ('Site1', 'MPN2', 'Week1', 230),
    ]

    # Define what the correct output should look like for test_data_1
    expected_output_1 = [
        ('Site1', 'MPN1', 'Week1', 100, 100),
        ('Site1', 'MPN1', 'Week2', 90, 190),
        ('Site1', 'MPN1', 'Week3', 111, 301),
        ('Site1', 'MPN1', 'Week4', 200, 501),
        ('Site1', 'MPN1', 'Week5', 120, 621),
        ('Site1', 'MPN1', 'Week10', 200, 821),
        ('Site1', 'MPN1', 'Week11', 300, 1121),
        ('Site1', 'MPN2', 'Week1', 230, 230),
        ('Site1', 'MPN2', 'Week2', 240, 470)
    ]

    # Run our function on the first test data
    result_1 = calculate_cumulative_qty(test_data_1)
    # Check if the result perfectly matches our expected output
    if result_1 == expected_output_1:
        # Print success message if they match
        print("Test Case 1 (Standard Data): PASS")
    # If they do not match
    else:
        # Print failure message
        print("Test Case 1 (Standard Data): FAIL")

    # Generate a large dataset to test performance and memory limits
    large_test_data = []
    # Loop 100 times to create 100 different MPNs
    for mpn_idx in range(1, 101):
        # Create an MPN string name
        mpn_name = f'MPN{mpn_idx}'
        # Loop 13 times to create data for 13 weeks for each MPN
        for week_idx in range(13, 0, -1):
            # Append the generated row to our large data list with a fixed quantity of 10
            large_test_data.append(('Site1', mpn_name, f'Week{week_idx}', 10))

    # Run our function on the large dataset
    large_result = calculate_cumulative_qty(large_test_data)

    # Extract the very last row of the processed large dataset to verify logic
    last_row = large_result[-1]
    # The last row should be MPN100, Week13, qty 10, cumulative 130 (13 weeks * 10)
    if last_row == ('Site1', 'MPN100', 'Week13', 10, 130):
        # Print success message if the final calculation is correct
        print("Test Case 2 (Large Data - 1300 rows): PASS")
    # If the final calculation is incorrect
    else:
        # Print failure message
        print("Test Case 2 (Large Data - 1300 rows): FAIL")


# Standard Python boilerplate to run the main function when the script executes
if __name__ == "__main__":
    # Call the main function
    main()