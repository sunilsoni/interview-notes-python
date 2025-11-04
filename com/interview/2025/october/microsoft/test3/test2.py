import requests  # To make HTTP GET requests
import math  # To round the final amount


# Function to fetch and filter transactions
def getTransactions(userId, locationId, netStart, netEnd):
    # Base URL for API endpoint
    base_url = "https://jsonmock.hackerrank.com/api/transactions/search?userId={}".format(userId)

    total_sum = 0.0  # Initialize total amount sum
    page = 1  # Start from first page

    while True:
        # Make API call for the current page
        response = requests.get(base_url + "&page=" + str(page))
        data = response.json()  # Convert response to JSON dictionary

        # Extract list of transactions
        transactions = data.get("data", [])

        # Iterate each transaction in current page
        for txn in transactions:
            # Extract location id safely (default empty dict if missing)
            loc = txn.get("location", {})
            # Extract ip address string
            ip = txn.get("ip", "")

            # Extract first byte of IP
            try:
                first_byte = int(ip.split('.')[0])
            except (ValueError, IndexError):
                continue  # Skip malformed IPs

            # Apply both filters: location match and IP range check
            if loc.get("id") == locationId and netStart <= first_byte <= netEnd:
                # Extract amount and clean it: remove '$' and commas
                amt_str = txn.get("amount", "0").replace("$", "").replace(",", "")
                try:
                    amount = float(amt_str)
                    total_sum += amount  # Add to running total
                except ValueError:
                    continue  # Skip invalid amount strings

        # Stop if last page reached
        if page >= data.get("total_pages", 0):
            break

        page += 1  # Move to next page

    # Return rounded integer total
    return int(round(total_sum))


# --------------------------------------------------------------------
# Simple testing harness (no unit test)
# --------------------------------------------------------------------
def main():
    print("Running sample test cases...\n")

    # Test Case 1 (from problem statement)
    uid = 2
    locationId = 8
    netStart = 5
    netEnd = 50
    expected_output = 8446
    result = getTransactions(uid, locationId, netStart, netEnd)
    print("Test 1:", "PASS" if result == expected_output else f"FAIL (Got {result})")

    # Edge Case 2: No matching transactions
    uid = 1
    locationId = 9999
    netStart = 200
    netEnd = 201
    result = getTransactions(uid, locationId, netStart, netEnd)
    print("Test 2:", "PASS" if result == 0 else f"FAIL (Got {result})")

    # Edge Case 3: Large IP range (stress test for pagination)
    uid = 2
    locationId = 8
    netStart = 0
    netEnd = 255
    result = getTransactions(uid, locationId, netStart, netEnd)
    print("Test 3 (Large Data): Completed ->", result)


# Run the main function
if __name__ == "__main__":
    main()
