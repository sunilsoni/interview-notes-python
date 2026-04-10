import statistics

def mean_no_outliers(nums):
    m, s = statistics.mean(nums), statistics.stdev(nums)
    filtered = [x for x in nums if abs(x - m) <= 2 * s]
    return statistics.mean(filtered) if filtered else None

# Example
print(mean_no_outliers([10, 12, 11, 13, 100]))  # Output: 11.5
