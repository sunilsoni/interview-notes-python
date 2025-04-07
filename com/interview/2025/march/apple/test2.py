# Import Optional for type hinting of a value that can be of type int or None.
from typing import Optional, TypedDict


# Define the TypedDict for the API result.
# Replace 'int | None' with 'Optional[int]' to support Python versions below 3.10.
class FetchPageResult(TypedDict):
    next_page: Optional[int]  # Optional[int] means the value can be an int or None.
    results: list[int]  # A list of integers.


# Constants used for testing the pagination.
MAX_RESULTS = 103
PAGE_SIZE = 10


def fetch_page(page: int) -> FetchPageResult:
    """
    Simulates a paginated API.
    Returns a dictionary containing the next page number (or None if no more pages)
    and a list of integers as results.
    """
    # Check if the start index for this page is greater than or equal to MAX_RESULTS.
    if page * PAGE_SIZE >= MAX_RESULTS:
        # No more results available; return an empty list and next_page as None.
        return {"next_page": None, "results": []}

    # Return a slice of numbers representing this page.
    return {
        "next_page": page + 1,  # Next page number.
        "results": list(
            range(page * PAGE_SIZE, min(MAX_RESULTS, (page + 1) * PAGE_SIZE))
        ),
    }


# Define the ResultFetcher class to abstract the pagination.
class ResultFetcher:
    def __init__(self) -> None:
        # Initialize current_page to start from page 0.
        self.current_page: Optional[int] = 0
        # Cache to hold any extra results fetched from a page.
        self.cache: list[int] = []

    def fetch(self, num_results: int) -> list[int]:
        """
        Retrieves up to 'num_results' items by fetching and caching pages as needed.
        It abstracts away the pagination logic, so the user only needs to call this method.
        """
        results: list[int] = []  # List to accumulate the results.
        while len(results) < num_results:
            # If the cache has data, use it first.
            if self.cache:
                needed = num_results - len(results)  # Calculate how many more results are needed.
                results.extend(self.cache[:needed])  # Add needed results from the cache.
                self.cache = self.cache[needed:]  # Remove the used results from the cache.
            # If there is no cache and we have more pages to fetch:
            elif self.current_page is not None:
                page_data = fetch_page(self.current_page)  # Fetch data for the current page.
                self.current_page = page_data["next_page"]  # Update the current_page.
                self.cache.extend(page_data["results"])  # Add fetched results to the cache.
                # If no results are fetched, break out of the loop.
                if not page_data["results"]:
                    break
            else:
                # No more pages to fetch, exit the loop.
                break
        return results  # Return the accumulated results.


# Test function to verify the solution.
def test_case(test_case: int, actual: list[int], expected: list[int]) -> None:
    if actual == expected:
        print(f"Test Case {test_case}: SUCCESS")
    else:
        print(f"Test Case {test_case}: FAILED")
        print(f"Expected {expected}. Got {actual}")


# Main testing code.
if __name__ == "__main__":
    fetcher = ResultFetcher()
    test_case(1, fetcher.fetch(5), list(range(5)))
    test_case(2, fetcher.fetch(2), list(range(5, 7)))
    test_case(3, fetcher.fetch(7), list(range(7, 14)))
    test_case(4, fetcher.fetch(103), list(range(14, 103)))
    test_case(5, fetcher.fetch(10), [])

    fetcher = ResultFetcher()
    test_case(6, fetcher.fetch(200), list(range(103)))
