# Modified function to implement rate limiting status check for the requests
def get_request_status(requests):
    # Constants for the rate limiter
    MAX_REQUESTS_PER_5_SECONDS = 2
    MAX_REQUESTS_PER_30_SECONDS = 5

    # Store the timestamps of successful requests for each domain
    successful_requests = {}

    # List to hold the result status of each request
    results = []

    # Iterate through each request and determine its status
    for i, domain in enumerate(requests):
        # If domain is not in the dictionary, add it with an empty list
        if domain not in successful_requests:
            successful_requests[domain] = []

        # Get the current time (index)
        current_time = i

        # Filter out requests that are outside of the 30-second window
        successful_requests[domain] = [
            t for t in successful_requests[domain] if current_time - t < 30
        ]

        # Count the number of requests in the last 5 seconds
        requests_in_last_5_seconds = sum(t >= current_time - 5 for t in successful_requests[domain])

        # If the number of requests in the last 5 seconds and 30 seconds are under the limit
        if requests_in_last_5_seconds < MAX_REQUESTS_PER_5_SECONDS and len(
                successful_requests[domain]) < MAX_REQUESTS_PER_30_SECONDS:
            # Add the current time to the successful requests for this domain
            successful_requests[domain].append(current_time)
            # Append the success status message to the results list
            results.append({"status": 200, "message": "OK"})
        else:
            # Append the failure status message to the results list
            results.append({"status": 429, "message": "Too many requests"})

    return results


# Sample input from the user's screenshots
sample_requests = [
    "www.abc.com", "www.hd.com", "www.abc.com", "www.pqr.com",
    "www.abc.com", "www.pqr.com", "www.pqr.com",
    "www.hr.com", "www.hr.com", "www.hr.com", "www.hr.com"
]

# Get the status for each sample input
sample_output = get_request_status(sample_requests)
print(sample_output)
