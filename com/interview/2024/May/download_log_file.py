from collections import Counter

import requests


def download_log_file(file_url):
    """
    Downloads the content of a log file given its URL.

    :param file_url: The URL of the log file.
    :return: The content of the log file as a string.
    """
    response = requests.get(file_url)
    response.raise_for_status()  # Will raise an error for bad requests (4xx or 5xx)
    return response.text


def count_url_occurrences(log_content):
    """
    Counts the occurrences of each URL in the log file content.

    :param log_content: The content of the log file.
    :return: A Counter object with the count of each URL.
    """
    # Split the log content into a list of URLs and remove any leading/trailing whitespace
    urls = log_content.strip().split("\n")
    return Counter(urls)


def find_most_common_url(url_counts):
    """
    Finds the most common URL and its number of occurrences.

    :param url_counts: A Counter object with the count of each URL.
    :return: A tuple containing the most common URL and its count.
    """
    # Get the most common URL; most_common returns a list of tuples
    most_common_url, count = url_counts.most_common(1)[0]
    return most_common_url, count


def main(log_file_url):
    """
    Main function to execute the program.

    :param log_file_url: The URL of the log file to process.
    """
    # Download the log file
    log_content = download_log_file(log_file_url)

    # Count URL occurrences
    url_counts = count_url_occurrences(log_content)

    # Find the most common URL
    most_common_url, count = find_most_common_url(url_counts)

    # Output the result
    print(f"The most common URL is {most_common_url} (with {count} occurrences)")


# URLs of the log files
log_file_url1 = "https://public.karat.io/content/urls2.txt"
log_file_url2 = "https://public.karat.io/content/q015/single_url.txt"

# Running the main function for each log file
main(log_file_url1)
main(log_file_url2)
