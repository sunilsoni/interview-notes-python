# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import json


# Function to check the rate limiting status for the requests
def get_request_status(requests):
    # Constants for the rate limiter
    MAX_REQUESTS_PER_5_SECONDS = 2
    MAX_REQUESTS_PER_30_SECONDS = 5

    # Store the time stamps for each request for each domain
    timestamps = {}

    # Store the status of each request
    results = []

    # Process each request
    for i, domain in enumerate(requests):
        # Initialize the domain in timestamps dictionary if not present
        if domain not in timestamps:
            timestamps[domain] = []

        # Current timestamp is the index in the array (in seconds)
        current_timestamp = i

        # Remove timestamps older than 30 seconds from the start of the window
        timestamps[domain] = [
            t for t in timestamps[domain] if current_timestamp - t < 30
        ]

        # Check if the request is within the rate limits
        if len(timestamps[domain]) < MAX_REQUESTS_PER_5_SECONDS and \
                len(timestamps[domain]) < MAX_REQUESTS_PER_30_SECONDS:
            # If within the rate limit, add the current timestamp and accept the request
            timestamps[domain].append(current_timestamp)
            results.append(json.dumps({"status": 200, "message": "OK"}))
        else:
            # If rate limit is exceeded, reject the request
            results.append(json.dumps({"status": 429, "message": "Too many requests"}))

        # Remove timestamps older than 5 seconds for the next check
        timestamps[domain] = [
            t for t in timestamps[domain] if current_timestamp - t < 5
        ]

    return results


# Sample inputs from the user's screenshots
sample_requests_0 = ["www.abc.com", "www.hd.com", "www.abc.com", "www.pqr.com",
                     "www.abc.com", "www.pqr.com", "www.pqr.com"]
sample_requests_1 = ["www.hr.com", "www.hr.com", "www.hr.com", "www.hr.com"]

# Get the status for each sample input
sample_output_0 = get_request_status(sample_requests_0)
sample_output_1 = get_request_status(sample_requests_1)

print(sample_output_0)

print("sample_output_1", sample_output_1)
