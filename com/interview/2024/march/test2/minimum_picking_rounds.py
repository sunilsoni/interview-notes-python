def minimum_picking_rounds(customer_order, warehouse_order):
    # Initialize a set from the customer's order for fast lookup and counting.
    items_to_pick = set(customer_order)
    # Variable to keep track of the number of rounds.
    rounds = 0
    # Keep track of the current progress through the warehouse order.
    current_index = 0

    # Continue until all items are picked.
    while items_to_pick:
        rounds += 1  # Start a new round
        picked_this_round = False

        # Go through the warehouse order to pick items.
        while current_index < len(warehouse_order):
            item = warehouse_order[current_index]
            if item in items_to_pick:
                items_to_pick.remove(item)
                picked_this_round = True

            # If all items are picked, end the loop early.
            if not items_to_pick:
                break
            current_index += 1

        # Reset the index if the end of the warehouse order is reached
        # and there are still items left to pick, meaning a new round starts.
        if picked_this_round and items_to_pick:
            current_index = 0

    return rounds


# Example usage
customer_order = ['item1', 'item3', 'item5', 'item2']
warehouse_order = ['item3', 'item1', 'item2', 'item5']
print(minimum_picking_rounds(customer_order, warehouse_order))
