# This function extracts number from week string like "Week10".
def get_week_number(week):
    # Replace "Week" with empty string, so "Week10" becomes "10".
    week_number_text = week.replace("Week", "")

    # Convert "10" string into integer 10 for correct numeric sorting.
    return int(week_number_text)


# This function calculates cumulative quantity for each site and MPN.
def cumulative_sum(data):
    # Sort data by site, then MPN, then actual week number.
    sorted_data = sorted(data, key=lambda row: (row[0], row[1], get_week_number(row[2])))

    # This dictionary keeps running total for each site + MPN.
    final_map = {}

    # This list stores final output with cumulative quantity.
    output = []

    # Loop through every row after sorting.
    for row in sorted_data:
        # Get site from row position 0.
        site = row[0]

        # Get MPN/product from row position 1.
        mpn = row[1]

        # Get week from row position 2.
        week = row[2]

        # Get quantity from row position 3.
        qty = row[3]

        # Create unique key because cumulative should restart for every site + MPN.
        key = (site, mpn)

        # If this site + MPN is coming first time, start total from 0.
        if key not in final_map:
            # Store initial cumulative value as 0.
            final_map[key] = 0

        # Add current week quantity into running total.
        final_map[key] += qty

        # Store current row with cumulative quantity.
        output.append((site, mpn, week, qty, final_map[key]))

    # Return final output.
    return output


# This function checks actual result with expected result.
def check(test_name, actual, expected):
    # If actual output and expected output are same, test passes.
    if actual == expected:
        # Print PASS message.
        print(test_name, "PASS")
    else:
        # Print FAIL message.
        print(test_name, "FAIL")

        # Print expected output for debugging.
        print("Expected:", expected)

        # Print actual output for debugging.
        print("Actual:", actual)


# Main method starts here.
if __name__ == "__main__":
    # Sample input data.
    data = [
        ("Site1", "MPN1", "Week1", 100),
        ("Site1", "MPN1", "Week2", 90),
        ("Site1", "MPN1", "Week3", 111),
        ("Site1", "MPN1", "Week4", 200),
        ("Site1", "MPN1", "Week5", 120),
        ("Site1", "MPN1", "Week10", 200),
        ("Site1", "MPN1", "Week11", 300),

        ("Site1", "MPN2", "Week1", 230),
        ("Site1", "MPN2", "Week2", 240),
        ("Site1", "MPN2", "Week3", 120),
        ("Site1", "MPN2", "Week4", 430),
        ("Site1", "MPN2", "Week5", 222),

        ("Site1", "MPN3", "Week1", 399),
        ("Site1", "MPN3", "Week2", 122),
        ("Site1", "MPN3", "Week3", 299),
        ("Site1", "MPN3", "Week4", 232),
        ("Site1", "MPN3", "Week5", 300),
    ]

    # Expected output for basic test case.
    expected = [
        ("Site1", "MPN1", "Week1", 100, 100),
        ("Site1", "MPN1", "Week2", 90, 190),
        ("Site1", "MPN1", "Week3", 111, 301),
        ("Site1", "MPN1", "Week4", 200, 501),
        ("Site1", "MPN1", "Week5", 120, 621),
        ("Site1", "MPN1", "Week10", 200, 821),
        ("Site1", "MPN1", "Week11", 300, 1121),

        ("Site1", "MPN2", "Week1", 230, 230),
        ("Site1", "MPN2", "Week2", 240, 470),
        ("Site1", "MPN2", "Week3", 120, 590),
        ("Site1", "MPN2", "Week4", 430, 1020),
        ("Site1", "MPN2", "Week5", 222, 1242),

        ("Site1", "MPN3", "Week1", 399, 399),
        ("Site1", "MPN3", "Week2", 122, 521),
        ("Site1", "MPN3", "Week3", 299, 820),
        ("Site1", "MPN3", "Week4", 232, 1052),
        ("Site1", "MPN3", "Week5", 300, 1352),
    ]

    # Call function and store result.
    result = cumulative_sum(data)

    # Check test result.
    check("Test 1 - Sample Data:", result, expected)

    # Unsorted input test.
    unsorted_data = [
        ("Site1", "MPN1", "Week3", 111),
        ("Site1", "MPN1", "Week1", 100),
        ("Site1", "MPN1", "Week2", 90),
    ]

    # Expected result after sorting by week.
    unsorted_expected = [
        ("Site1", "MPN1", "Week1", 100, 100),
        ("Site1", "MPN1", "Week2", 90, 190),
        ("Site1", "MPN1", "Week3", 111, 301),
    ]

    # Check unsorted input.
    check("Test 2 - Unsorted Data:", cumulative_sum(unsorted_data), unsorted_expected)

    # Week10 sorting test.
    week10_data = [
        ("Site1", "MPN1", "Week10", 200),
        ("Site1", "MPN1", "Week2", 90),
        ("Site1", "MPN1", "Week1", 100),
    ]

    # Expected result should place Week10 after Week2.
    week10_expected = [
        ("Site1", "MPN1", "Week1", 100, 100),
        ("Site1", "MPN1", "Week2", 90, 190),
        ("Site1", "MPN1", "Week10", 200, 390),
    ]

    # Check Week10 numeric sorting.
    check("Test 3 - Week10 Sorting:", cumulative_sum(week10_data), week10_expected)

    # Empty input test.
    empty_data = []

    # Expected output is empty list.
    empty_expected = []

    # Check empty input.
    check("Test 4 - Empty Data:", cumulative_sum(empty_data), empty_expected)

    # Print final readable output.
    print("\nFinal Output:")

    # Print table header.
    print("site   mpn   week    qty   cumulative_qty")

    # Print separator.
    print("------------------------------------------")

    # Loop through final result.
    for site, mpn, week, qty, cumulative_qty in result:
        # Print every row in readable format.
        print(f"{site:<6} {mpn:<5} {week:<7} {qty:<5} {cumulative_qty}")