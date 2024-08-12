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
    urls = log_content.strip().split("\n")
    return Counter(urls)


def find_top_n_urls(url_counts, n):
    """
    Finds the top N most common URLs.

    :param url_counts: A Counter object with the count of each URL.
    :param n: The number of top URLs to retrieve.
    :return: A list of tuples containing the top N URLs and their counts.
    """
    return url_counts.most_common(n)


def main(log_file_url, top_n):
    """
    Main function to execute the program.

    :param log_file_url: The URL of the log file to process.
    :param top_n: The number of top URLs to output.
    """
    log_content = download_log_file(log_file_url)
    url_counts = count_url_occurrences(log_content)
    top_urls = find_top_n_urls(url_counts, top_n)

    for url, count in top_urls:
        print(f"({url}, {count})")


# URLs of the log files
log_file_url1 = "https://public.karat.io/content/urls2.txt"

# Running the main function for the first log file with N = 15
main(log_file_url1, 15)
