import collections


def getRequestStatus(requests):
    domain_counts = collections.defaultdict(collections.deque)

    def check_limits(domain):
        count_5s = 0
        count_30s = 0
        for timestamp in domain_counts[domain]:
            if timestamp >= i - 5:
                count_5s += 1
            if timestamp >= i - 30:
                count_30s += 1
        return count_5s < 2 and count_30s < 5

    result = []
    for i, domain in enumerate(requests):
        if check_limits(domain):
            domain_counts[domain].append(i)  # Update timestamps for accepted requests
            result.append("{status: 200, message: OK}")
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
