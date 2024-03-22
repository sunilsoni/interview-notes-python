import collections
from collections import defaultdict
from collections import deque


def getRequestStatus(requests):
    domain_counts = collections.defaultdict(lambda: deque(maxlen=30))  # Set maxlen to 30 for timestamps

    def check_limits(domain):
        count_5s = sum(1 for timestamp in domain_counts[domain] if timestamp > i - 5)
        count_30s = sum(1 for timestamp in domain_counts[domain] if timestamp > i - 30)
        return count_5s < 2 and count_30s < 5

    result = []
    for i, domain in enumerate(requests):
        if check_limits(domain):
            domain_counts[domain].append(i)  # Update timestamps for accepted requests
            result.append("{status: 200, message: OK}")
        else:
            result.append("{status: 429, message: Too many requests}")

    return result


def getRequestStatus1(requests):
    # Dictionary to store the timestamps of last requests from each domain
    last_request_time = defaultdict(list)

    # List to store the status of each request
    result = []

    # Function to check if a request can be processed based on the rate limiting rules
    def can_process_request(domain, current_time):
        # Number of requests allowed within 5 seconds and 30 seconds
        requests_within_5s = 2
        requests_within_30s = 5

        # Check if there are more than 2 requests within 5 seconds
        if len(last_request_time[domain]) >= requests_within_5s:
            if current_time - last_request_time[domain][-requests_within_5s] < 5:
                return False

        # Check if there are more than 5 requests within 30 seconds
        if len(last_request_time[domain]) >= requests_within_30s:
            if current_time - last_request_time[domain][-requests_within_30s] < 30:
                return False

        return True

    # Process each request
    for request in requests:
        current_time = len(result)  # Time starts from 0

        # Extract domain from the request
        domain = request.strip()

        # Check if the request can be processed
        if can_process_request(domain, current_time):
            result.append("{status: 200, message: OK}")
            last_request_time[domain].append(current_time)
        else:
            result.append("{status: 429, message: Too many requests}")

    return result


# Test the function
requests = ['www.aebebca.com', 'www.cccbeae.com', 'www.acaaaed.com', 'www.acaaaed.com', 'www.cccdacb.com',
            'www.aebebca.com', 'www.cccbeae.com', 'www.acaaaed.com', 'www.acaaaed.com', 'www.cccbeae.com',
            'www.cccdacb.com', 'www.cccdacb.com', 'www.aebebca.com', 'www.aebebca.com', 'www.aebebca.com',
            'www.acaaaed.com', 'www.aebebca.com', 'www.cccbeae.com', 'www.cccdacb.com', 'www.aebebca.com',
            'www.acaaaed.com', 'www.cccbeae.com', 'www.cccbeae.com', 'www.aebebca.com', 'www.cccdacb.com',
            'www.acaaaed.com', 'www.cccbeae.com', 'www.acaaaed.com', 'www.eeebebb.com', 'www.cccdacb.com',
            'www.aebebca.com', 'www.eeebebb.com', 'www.aebebca.com', 'www.aebebca.com', 'www.cccdacb.com',
            'www.acaaaed.com', 'www.cccbeae.com', 'www.cccbeae.com', 'www.cccbeae.com', 'www.eeebebb.com',
            'www.aebebca.com', 'www.aebebca.com', 'www.acaaaed.com', 'www.eeebebb.com', 'www.cccdacb.com',
            'www.cccdacb.com', 'www.acaaaed.com', 'www.eeebebb.com', 'www.cccbeae.com', 'www.aebebca.com',
            'www.eeebebb.com', 'www.acaaaed.com', 'www.acaaaed.com', 'www.cccbeae.com', 'www.acaaaed.com',
            'www.cccdacb.com', 'www.cccbeae.com']

print(getRequestStatus(requests))
