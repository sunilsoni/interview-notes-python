import heapq


def merge_streams(streams):
    output_stream = []  # Initialize an empty output stream
    iterators = [(iter(stream), i) for i, stream in enumerate(streams)]  # Initialize iterators for each input stream
    heapq.heapify(iterators)  # Create a min-heap based on the first element of each iterator

    while iterators:  # Iterate until all iterators are exhausted
        iterator, stream_idx = heapq.heappop(iterators)  # Get the iterator with the smallest value
        try:
            val = next(iterator)  # Get the next element from the iterator
            output_stream.append(val)  # Append the minimum value to the output stream
            heapq.heappush(iterators, (iterator, stream_idx))  # Push the updated iterator back into the heap
        except StopIteration:
            pass  # Continue to the next iteration if the iterator is exhausted

    return output_stream


def find_files(directory, criteria):
    """
    Recursively search a directory for files matching the given criteria.

    Args:
    - directory (str): The directory to search.
    - criteria (function): A function that takes a file path as input and returns True if the file matches the criteria.

    Returns:
    - list: A list of file paths matching the criteria.
    """
    matching_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if criteria(file_path):
                matching_files.append(file_path)

    return matching_files


# Example criteria functions

def file_greater_than_1mb(file_path):
    return os.path.getsize(file_path) > 1024 * 1024  # 1MB in bytes


def file_modified_less_than_2_days_ago(file_path):
    modification_time = os.path.getmtime(file_path)
    delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(modification_time)
    return delta.days < 2


# Example usage
directory_path = "/path/to/your/directory"
# Find files greater than 1MB
large_files = find_files(directory_path, file_greater_than_1mb)
print("Files greater than 1MB:", large_files)

# Find files modified less than 2 days ago
recently_modified_files = find_files(directory_path, file_modified_less_than_2_days_ago)
print("Files modified less than 2 days ago:", recently_modified_files)


def find_files(directory, criteria):
    """
    Recursively search a directory for files matching the given criteria.

    Args:
    - directory (str): The directory to search.
    - criteria (function): A function that takes a file path as input and returns True if the file matches the criteria.

    Returns:
    - list: A list of file paths matching the criteria.
    """
    matching_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if criteria(file_path):
                matching_files.append(file_path)

    return matching_files


# Example criteria functions

def file_greater_than_1mb(file_path):
    return os.path.getsize(file_path) > 1024 * 1024  # 1MB in bytes


def file_modified_less_than_2_days_ago(file_path):
    modification_time = os.path.getmtime(file_path)
    delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(modification_time)
    return delta.days < 2


# Example usage
directory_path = "/path/to/your/directory"
# Find files greater than 1MB
large_files = find_files(directory_path, file_greater_than_1mb)
print("Files greater than 1MB:", large_files)

# Find files modified less than 2 days ago
recently_modified_files = find_files(directory_path, file_modified_less_than_2_days_ago)
print("Files modified less than 2 days ago:", recently_modified_files)


####


def find_files(directory, criteria):
    """
    Recursively search a directory for files matching the given criteria.

    Args:
    - directory (str): The directory to search.
    - criteria (function): A function that takes a file path as input and returns True if the file matches the criteria.

    Returns:
    - list: A list of file paths matching the criteria.
    """
    matching_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and criteria(file_path):  # Check if it's a file and meets criteria
                matching_files.append(file_path)

    return matching_files


# Example criteria functions

def file_greater_than_1mb(file_path):
    return os.path.getsize(file_path) > 1024 * 1024  # 1MB in bytes


def file_modified_less_than_2_days_ago(file_path):
    modification_time = os.path.getmtime(file_path)
    delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(modification_time)
    return delta.days < 2


# Example usage
directory_path = "/path/to/your/directory"
# Find files greater than 1MB
large_files = find_files(directory_path, file_greater_than_1mb)
print("Files greater than 1MB:", large_files)

# Find files modified less than 2 days ago
recently_modified_files = find_files(directory_path, file_modified_less_than_2_days_ago)
print("Files modified less than 2 days ago:", recently_modified_files)

#######
import os
import datetime


def find_files(directory, criteria):
    """
    Recursively search a directory for files matching the given criteria.

    Args:
    - directory (str): The directory to search.
    - criteria (function): A composite criteria function.

    Returns:
    - list: A list of file paths matching the criteria.
    """
    matching_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and criteria(file_path):
                matching_files.append(file_path)

    return matching_files


# Define composite criteria functions
def and_criteria(*conditions):
    def composite_criteria(file_path):
        return all(condition(file_path) for condition in conditions)

    return composite_criteria


def max_size(size):
    def criteria(file_path):
        return os.path.getsize(file_path) <= size * 1024 * 1024  # Size in megabytes converted to bytes

    return criteria


def older_than(days):
    def criteria(file_path):
        modification_time = os.path.getmtime(file_path)
        delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(modification_time)
        return delta.days >= days

    return criteria


# Example usage
directory_path = "/path/to/your/directory"
custom_criteria = and_criteria(max_size(20), older_than(2))
matching_files = find_files(directory_path, custom_criteria)
print("Matching files:", matching_files)
