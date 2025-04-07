import time
import random
from typing import Optional


# Simulated exception from the flaky API.
class ThirdPartyFailure(Exception):
    pass


# Constants defining maximum results and page size.
MAX_RESULTS = 103
PAGE_SIZE = 10


def fetch_page(page_number: int) -> list[int]:
    """
    Simulates a paginated API call that may fail about 30% of the time.
    On success, returns up to PAGE_SIZE integers.
    On failure, raises ThirdPartyFailure.
    """
    print(f"Fetching page {page_number}")

    # Simulate flakiness: ~30% chance to fail.
    if random.random() < 0.3:
        raise ThirdPartyFailure(f"API flake on page {page_number}")

    # Calculate the starting and ending indices for this page.
    start = page_number * PAGE_SIZE
    end = min(start + PAGE_SIZE, MAX_RESULTS)

    # If start is beyond MAX_RESULTS, return an empty list (no more results).
    if start >= MAX_RESULTS:
        print("Reached maximum results. No more pages available.")
        return []

    results = list(range(start, end))
    print(f"Fetched results from page {page_number}: {results}")
    return results


class ResultFetcher:
    def __init__(self) -> None:
        # Track the current page; start at page 0.
        self.current_page: Optional[int] = 0
        # Hold the results from the last successfully fetched page.
        self.current_page_results: list[int] = []
        # Pointer to the next unread result in the current page's results.
        self.current_index: int = 0
        print("Initialized ResultFetcher.")

    def fetch(self, num_results: int) -> list[int]:
        """
        Returns up to 'num_results' items by repeatedly calling the flaky fetch_page.
        Implements retry logic for each page fetch.
        """
        results: list[int] = []
        print(f"Starting fetch for {num_results} results.")

        # Continue until we've collected enough results.
        while len(results) < num_results:
            # If current page's results are exhausted, fetch the next page.
            if self.current_index >= len(self.current_page_results):
                if self.current_page is not None:
                    # Attempt to safely fetch the current page.
                    page_results = self._safe_fetch_page(self.current_page)
                    if page_results is None:
                        print(f"Failed to fetch page {self.current_page} after retries. Stopping.")
                        break

                    self.current_page_results = page_results
                    self.current_index = 0

                    # If the fetched page returns no results, no more data exists.
                    if not self.current_page_results:
                        print(f"No results returned from page {self.current_page}. No more data.")
                        self.current_page = None
                        break

                    # Prepare for the next page.
                    self.current_page += 1
                else:
                    print("No more pages to fetch (current_page is None).")
                    break

            # Determine how many results can be taken from the current page.
            available = len(self.current_page_results) - self.current_index
            needed = num_results - len(results)
            to_take = min(available, needed)

            # Append the slice of results from the current page.
            segment = self.current_page_results[self.current_index:self.current_index + to_take]
            results.extend(segment)
            print(f"Added {to_take} results: {segment} (Total collected: {len(results)})")
            self.current_index += to_take

        print(f"Fetch complete. Returning results: {results}")
        return results

    def _safe_fetch_page(self, page_number: int, max_retries: int = 5, delay: float = 0.5) -> Optional[list[int]]:
        """
        Attempts to fetch a page using the flaky fetch_page function.
        Retries up to max_retries times before returning None on failure.
        """
        for attempt in range(1, max_retries + 1):
            try:
                print(f"Attempt {attempt} to fetch page {page_number}...")
                page_results = fetch_page(page_number)
                print(f"Successfully fetched page {page_number}: {page_results}")
                return page_results
            except ThirdPartyFailure as e:
                print(f"Error fetching page {page_number}: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
        # If all attempts fail, return None.
        return None


def test_case(test_case_number: int, actual: list[int], expected: list[int]) -> None:
    """
    Simple test helper that compares the actual results with the expected results.
    """
    if actual == expected:
        print(f"Test Case {test_case_number}: SUCCESS")
    else:
        print(f"Test Case {test_case_number}: FAILED")
        print(f"Expected {expected}. Got {actual}")


if __name__ == "__main__":
    # Create an instance of ResultFetcher and run test cases.
    fetcher = ResultFetcher()
    test_case(1, fetcher.fetch(5), list(range(5)))
    test_case(2, fetcher.fetch(2), list(range(5, 7)))
    test_case(3, fetcher.fetch(7), list(range(7, 14)))
    test_case(4, fetcher.fetch(103), list(range(14, 103)))
    test_case(5, fetcher.fetch(10), [])

    # Reinitialize to test fetching all available results in one call.
    fetcher = ResultFetcher()
    test_case(6, fetcher.fetch(200), list(range(103)))
