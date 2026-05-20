def processFIXTransactions(fixTransactions):
    # Create an empty dictionary to store the running net totals for each asset
    net_positions = {}

    # Loop through each individual transaction string in our input list
    for transaction in fixTransactions:

        # Split the transaction string by the pipe character '|' to isolate tag=value pairs
        pairs = transaction.split('|')

        # Initialize placeholder variables to hold the extracted data for the current transaction
        side = ""
        asset = ""
        quantity = 0.0

        # Loop through each isolated key-value pair
        for pair in pairs:

            # Split the pair by the equals sign '=' to separate the tag number from its actual value
            tag_value = pair.split('=')

            # Ensure the split actually produced exactly two items (a tag and a value) to avoid errors
            if len(tag_value) == 2:

                # Assign the first part to our 'tag' variable
                tag = tag_value[0]

                # Assign the second part to our 'value' variable
                value = tag_value[1]

                # Check if the tag is '54', which represents the side of the trade
                if tag == '54':
                    # Save the value (BUY or SELL) to our side variable
                    side = value

                # Check if the tag is '48', which represents the asset name
                elif tag == '48':
                    # Save the value (e.g., Google, Vodafone) to our asset variable
                    asset = value

                # Check if the tag is '38', which represents the quantity of shares
                elif tag == '38':
                    # Convert the string value to a float (decimal) and save it
                    quantity = float(value)

        # Check if we successfully found an asset name in this transaction string
        if asset != "":

            # If this is the first time we are seeing this asset, add it to the dictionary with a starting value of 0.0
            if asset not in net_positions:
                net_positions[asset] = 0.0

            # Check if the trade side was a BUY
            if side == 'BUY':
                # Add the quantity to our running total for this asset
                net_positions[asset] += quantity

            # Check if the trade side was a SELL
            elif side == 'SELL':
                # Subtract the quantity from our running total for this asset
                net_positions[asset] -= quantity

    # Create an empty list to store the final, formatted trade strings
    results = []

    # Extract all the asset names (keys) from the dictionary and sort them alphabetically
    sorted_assets = sorted(net_positions.keys())

    # Loop through each alphabetically sorted asset name
    for asset in sorted_assets:

        # Retrieve the final calculated net quantity for the current asset
        net_qty = net_positions[asset]

        # If the net quantity perfectly cancelled out to exactly 0, we don't need to make a trade
        if net_qty == 0:
            # Skip the rest of the loop and move to the next asset
            continue

        # Determine the final side: if the net quantity is greater than 0, it's a BUY. Otherwise, it's a SELL.
        final_side = 'BUY' if net_qty > 0 else 'SELL'

        # Get the absolute value of the quantity to remove any negative signs (e.g., -50 becomes 50)
        abs_qty = abs(net_qty)

        # Check if the decimal quantity is actually a whole number (e.g., 50.0)
        if abs_qty.is_integer():
            # Convert it to an integer and then to a string to drop the .0 (e.g., "50")
            formatted_qty = str(int(abs_qty))
        else:
            # If it has decimals, simply convert the decimal number to a string (e.g., "50.5")
            formatted_qty = str(abs_qty)

        # Combine the side, asset, and quantity together with commas
        trade_string = final_side + "," + asset + "," + formatted_qty

        # Add the completed string to our results list
        results.append(trade_string)

    # Join all the strings in the results list together using a newline character '\n'
    final_output = '\n'.join(results)

    # Return the final multi-line text block
    return final_output


if __name__ == '__main__':
    # Define a helper function to test and print pass/fail results simply
    def run_test(test_name, input_data, expected_output):
        # Call the main processing function with the input data
        result = processFIXTransactions(input_data)

        # Compare the result directly against the expected output
        if result == expected_output:
            # If they match exactly, print PASS
            print(f"{test_name}: PASS")
        else:
            # If they differ, print FAIL and show why
            print(f"{test_name}: FAIL")
            print("Expected:\n" + expected_output)
            print("Got:\n" + result)


    # Test Case 1: Simple input from the problem description
    test1_input = [
        "54=BUY|48=Vodafone|38=100|52=20220920",
        "54=SELL|115=CITI|48=Google|38=50"
    ]
    test1_expected = "SELL,Google,50\nBUY,Vodafone,100"
    run_test("Test Case 1 (Simple)", test1_input, test1_expected)

    # Test Case 2: Complex netting from the problem description
    test2_input = [
        "54=BUY|48=Vodafone|38=100|52=20220920",
        "54=SELL|115=CITI|48=Google|38=50",
        "54=BUY|48=Microsoft|49=BLK|38=50",
        "22=2|54=SELL|48=Vodafone|38=80",
        "54=BUY|452=13|48=Microsoft|38=150"
    ]
    test2_expected = "SELL,Google,50\nBUY,Microsoft,200\nBUY,Vodafone,20"
    run_test("Test Case 2 (Complex Netting)", test2_input, test2_expected)

    # Test Case 3: Exact cancellation (Net 0) and decimals
    test3_input = [
        "54=BUY|48=Apple|38=15.5",
        "54=SELL|48=Apple|38=15.5",  # This should cancel Apple out entirely
        "54=SELL|48=Tesla|38=20.25"
    ]
    test3_expected = "SELL,Tesla,20.25"
    run_test("Test Case 3 (Zero Cancellation & Decimals)", test3_input, test3_expected)

    # Test Case 4: Handling large data sets
    # We will generate 10,000 transactions programmatically to ensure it processes quickly
    test4_input = []
    for _ in range(5000):
        # Add 5000 buys of 10 shares each
        test4_input.append("54=BUY|48=Amazon|38=10")
        # Add 5000 sells of 5 shares each
        test4_input.append("54=SELL|48=Amazon|38=5")
    # Expected result: 5000 * 10 = 50,000 BUY. 5000 * 5 = 25,000 SELL. Net = 25000 BUY.
    test4_expected = "BUY,Amazon,25000"
    run_test("Test Case 4 (Large Data - 10k items)", test4_input, test4_expected)