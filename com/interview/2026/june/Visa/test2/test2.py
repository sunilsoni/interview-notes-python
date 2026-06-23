# We use defaultdict so missing keys automatically start with 0.
from collections import defaultdict


# This function converts week text like "Week10" into number 10.
def week_number(week):
    # Remove the word "Week" from the input string.
    number_part = week.replace("Week", "")

    # Convert the remaining value into an integer.
    return int(number_part)


# This function calculates cumulative quantity by site and MPN.
def calculate_cumulative_qty(data):
    # Sort data by site, then MPN, then numeric week number.
    sorted_data = sorted(data, key=lambda row: (row[0], row[1], week_number(row[2])))

    # This dictionary stores running total for each (site, mpn).
    totals = defaultdict(int)

    # This list stores final output rows.
    result = []

    # Loop through every row after sorting.
    for site, mpn, week, qty in sorted_data:
        # Create a group key because cumulative total is separate for each site and mpn.
        key = (site, mpn)

        # Add current row quantity into that group's running total.
        totals[key] += qty

        # Add the final row with cumulative quantity.
        result.append((site, mpn, week, qty, totals[key]))

    # Return final calculated result.
    return result


# This helper function prints output in readable format.
def print_result(result):
    # Print table header.
    print("site   mpn   week    qty   cumulative_qty")

    # Print separator line.
    print("------------------------------------------")

    # Loop through each output row.
    for site, mpn, week, qty, cumulative_qty in result:
        # Print each row in simple table format.
        print(f"{site:<6} {mpn:<5} {week:<7} {qty:<5} {cumulative_qty}")


# This helper function compares actual output with expected output.
def check(test_name, actual, expected):
    # Compare actual result with expected result.
    if actual == expected:
        # Print PASS when both are same.
        print(f"{test_name}: PASS")
    else:
        # Print FAIL when result is different.
        print(f"{test_name}: FAIL")

        # Print expected output for debugging.
        print("Expected:")

        # Show expected result.
        print(expected)

        # Print actual output for debugging.
        print("Actual:")

        # Show actual result.
        print(actual)


# This function runs all test cases.
def run_tests():
    # Test case 1: Basic sorted data.
    data1 = [
        ("Site1", "MPN1", "Week1", 100),
        ("Site1", "MPN1", "Week2", 90),
        ("Site1", "MPN1", "Week3", 111),
    ]

    # Expected output for test case 1.
    expected1 = [
        ("Site1", "MPN1", "Week1", 100, 100),
        ("Site1", "MPN1", "Week2", 90, 190),
        ("Site1", "MPN1", "Week3", 111, 301),
    ]

    # Run test case 1.
    check("Test 1 - Basic sorted data", calculate_cumulative_qty(data1), expected1)

    # Test case 2: Data is not sorted.
    data2 = [
        ("Site1", "MPN1", "Week3", 111),
        ("Site1", "MPN1", "Week1", 100),
        ("Site1", "MPN1", "Week2", 90),
    ]

    # Expected output should be sorted by week before cumulative calculation.
    expected2 = [
        ("Site1", "MPN1", "Week1", 100, 100),
        ("Site1", "MPN1", "Week2", 90, 190),
        ("Site1", "MPN1", "Week3", 111, 301),
    ]

    # Run test case 2.
    check("Test 2 - Unsorted weeks", calculate_cumulative_qty(data2), expected2)

    # Test case 3: Multiple MPN values.
    data3 = [
        ("Site1", "MPN2", "Week2", 240),
        ("Site1", "MPN1", "Week2", 90),
        ("Site1", "MPN2", "Week1", 230),
        ("Site1", "MPN1", "Week1", 100),
    ]

    # Expected output should calculate separately for MPN1 and MPN2.
    expected3 = [
        ("Site1", "MPN1", "Week1", 100, 100),
        ("Site1", "MPN1", "Week2", 90, 190),
        ("Site1", "MPN2", "Week1", 230, 230),
        ("Site1", "MPN2", "Week2", 240, 470),
    ]

    # Run test case 3.
    check("Test 3 - Multiple MPNs", calculate_cumulative_qty(data3), expected3)

    # Test case 4: Week10 should come after Week2, not before Week2.
    data4 = [
        ("Site1", "MPN1", "Week10", 200),
        ("Site1", "MPN1", "Week2", 90),
        ("Site1", "MPN1", "Week1", 100),
    ]

    # Expected output uses numeric week sorting.
    expected4 = [
        ("Site1", "MPN1", "Week1", 100, 100),
        ("Site1", "MPN1", "Week2", 90, 190),
        ("Site1", "MPN1", "Week10", 200, 390),
    ]

    # Run test case 4.
    check("Test 4 - Week10 numeric sorting", calculate_cumulative_qty(data4), expected4)

    # Test case 5: Multiple sites and MPNs.
    data5 = [
        ("Site2", "MPN1", "Week1", 50),
        ("Site1", "MPN1", "Week1", 100),
        ("Site2", "MPN1", "Week2", 60),
        ("Site1", "MPN1", "Week2", 90),
    ]

    # Expected output should calculate separately for Site1 and Site2.
    expected5 = [
        ("Site1", "MPN1", "Week1", 100, 100),
        ("Site1", "MPN1", "Week2", 90, 190),
        ("Site2", "MPN1", "Week1", 50, 50),
        ("Site2", "MPN1", "Week2", 60, 110),
    ]

    # Run test case 5.
    check("Test 5 - Multiple sites", calculate_cumulative_qty(data5), expected5)

    # Test case 6: Empty input.
    data6 = []

    # Expected output is also empty.
    expected6 = []

    # Run test case 6.
    check("Test 6 - Empty input", calculate_cumulative_qty(data6), expected6)

    # Test case 7: Large data input.
    data7 = []

    # Create large data for 1000 sites, 5 MPNs, and 13 weeks.
    for site_no in range(1000):
        # Create site name.
        site = f"Site{site_no}"

        # Loop through 5 products.
        for mpn_no in range(5):
            # Create MPN name.
            mpn = f"MPN{mpn_no}"

            # Loop through 13 weeks.
            for week_no in range(13, 0, -1):
                # Add data in reverse week order to test sorting.
                data7.append((site, mpn, f"Week{week_no}", 1))

    # Calculate output for large data.
    result7 = calculate_cumulative_qty(data7)

    # Expected number of rows is 1000 * 5 * 13.
    expected_count = 1000 * 5 * 13

    # Check large data row count.
    if len(result7) == expected_count:
        # Print PASS when row count is correct.
        print("Test 7 - Large data row count: PASS")
    else:
        # Print FAIL when row count is wrong.
        print("Test 7 - Large data row count: FAIL")

    # Check final cumulative value for one group.
    sample_rows = [row for row in result7 if row[0] == "Site0" and row[1] == "MPN0"]

    # Last row for 13 weeks should have cumulative value 13 because each qty is 1.
    if sample_rows[-1][-1] == 13:
        # Print PASS when cumulative value is correct.
        print("Test 7 - Large data cumulative value: PASS")
    else:
        # Print FAIL when cumulative value is wrong.
        print("Test 7 - Large data cumulative value: FAIL")


# Main method starts here.
if __name__ == "__main__":
    # Run all test cases first.
    run_tests()

    # Print a blank line for readability.
    print()

    # Sample input from the question.
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

    # Calculate cumulative quantity for sample data.
    output = calculate_cumulative_qty(data)

    # Print sample output.
    print_result(output)