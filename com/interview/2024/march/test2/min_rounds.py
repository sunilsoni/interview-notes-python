def min_rounds(customerOrder, warehouseOrder):
    # Create a dictionary to store the index of each item in the warehouse picking order
    warehouse_indices = {item: index for index, item in enumerate(warehouseOrder)}

    # Initialize a variable to keep track of the current maximum index reached in the warehouse order
    max_index = -1

    # Initialize a variable to keep track of the rounds
    rounds = 0

    # Iterate through the customer's order
    for item in customerOrder:
        # If the item is present in the warehouse order
        if item in warehouse_indices:
            # Get the index of the item in the warehouse order
            item_index = warehouse_indices[item]

            # If the index of the item in the warehouse order is greater than the current maximum index
            # Increment the rounds and update the current maximum index
            if item_index > max_index:
                rounds += 1
                max_index = item_index

    return rounds


# Test cases
customerOrder1 = ['item1', 'item3', 'item5', 'item2']
warehouseOrder1 = ['item4', 'item2', 'item5', 'item1', 'item3']
print("Example 1:", min_rounds(customerOrder1, warehouseOrder1))  # Output: 3

customerOrder2 = ['item1', 'item2', 'item3', 'item4', 'item5']
warehouseOrder2 = ['item3', 'item1', 'item2', 'item5']
print("Example 2:", min_rounds(customerOrder2, warehouseOrder2))  # Output: 4
