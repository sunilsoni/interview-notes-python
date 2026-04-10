import math


def get_filtered_mean(data, threshold=2):
    """
    Calculates the mean of a list after removing outliers.
    Outliers are defined as being more than 'threshold' standard deviations from the mean.
    """
    if not data:
        return 0.0

    # 1. Calculate the initial mean (mu)
    n = len(data)
    initial_mean = sum(data) / n

    # 2. Calculate the Standard Deviation (sigma)
    # Formula: sqrt( sum((x - mean)^2) / n )
    variance = sum((x - initial_mean) ** 2 for x in data) / n
    std_dev = math.sqrt(variance)

    # Handle the case where all numbers are the same (std_dev = 0)
    if std_dev == 0:
        return initial_mean

    # 3. Filter the list
    # Keep x if: (mean - threshold * std_dev) < x < (mean + threshold * std_dev)
    filtered_data = [
        x for x in data
        if abs(x - initial_mean) <= (threshold * std_dev)
    ]

    # 4. Return the mean of the filtered list
    return sum(filtered_data) / len(filtered_data)


# Example usage:
numbers = [10, 12, 11, 13, 12, 100, 11, 12, 11]  # 100 is a clear outlier
print(f"Filtered Mean: {get_filtered_mean(numbers)}")