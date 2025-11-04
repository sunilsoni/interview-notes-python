# Import 'literal_eval' from the 'ast' module to safely evaluate string lists like "[1,2,3]" into Python lists
from ast import literal_eval

# Import the 're' module for regular expression operations
import re


# Define a function 'StockPicker' that finds the maximum profit from buying and selling a stock once
def StockPicker(arr):
    # --- STEP 1: Parse the input data ---
    # If input is a string (like "[10,12,4,5,9]"), we need to extract numbers from it
    if isinstance(arr, str):
        try:
            # Try to safely convert string to a list using literal_eval
            # Example: "[10,12,4]" → [10, 12, 4]
            prices = list(map(int, literal_eval(arr)))
        except Exception:
            # If literal_eval fails (maybe malformed input), use regex to find all integer numbers
            # re.findall(r'-?\d+', arr) → finds both positive and negative integers
            prices = list(map(int, re.findall(r'-?\d+', arr)))
    else:
        # If already a list, directly assign it
        prices = arr

    # --- STEP 2: Initialize tracking variables ---
    # Start with an infinite minimum price (used to track the lowest price seen so far)
    min_price = float('inf')
    # Track the maximum profit (initially 0 because no transaction yet)
    max_profit = 0

    # --- STEP 3: Iterate through each price to calculate the maximum profit ---
    for price in prices:
        # If we find a smaller price than previous minimum, update min_price
        if price < min_price:
            min_price = price
        else:
            # Otherwise, calculate the profit if we sell at this price
            profit = price - min_price
            # If this profit is greater than the current max, update it
            if profit > max_profit:
                max_profit = profit

    # --- STEP 4: Determine final result ---
    # Convert max_profit to string if positive; otherwise return "-1" for no profit possible
    result = str(max_profit) if max_profit > 0 else "-1"

    # --- STEP 5: Filter result using a challenge token (custom requirement) ---
    # Define a token string (set of characters to remove from result)
    token = "p8xdf5atc6"
    # Create a set of lowercase characters from the token for quick lookup
    token_set = set(token.lower())
    # Remove all characters from 'result' that appear in the token (case-insensitive)
    filtered = ''.join(ch for ch in result if ch.lower() not in token_set)

    # If filtering removes everything, return "EMPTY"; otherwise return filtered string
    return filtered if filtered else "EMPTY"


# --- STEP 6: Run the function ---
# Call StockPicker with user input and print the output
# Example input: "[10,12,4,5,9]" → Output: "5" (max profit = 9-4)
print(StockPicker(input()))