from typing import Optional, TypedDict


# Define the API result type using Optional[int] for compatibility with earlier Python versions.
class FetchPageResult(TypedDict):
    next_page: Optional[int]  # Represents the next page number, or None if there are no more pages.
    results: list[int]  # The list of integer results on this page.


# Constants for testing.
MAX_RESULTS = 103
PAGE_SIZE = 10


def fetch_page(page: int) -> FetchPageResult:
    """
    Simulates a paginated API that returns a page of results.
    """
    if page * PAGE_SIZE >= MAX_RESULTS:
        return {"next_page": None, "results": []}
    return {
        "next_page": page + 1,
        "results": list(range(page * PAGE_SIZE, min(MAX_RESULTS, (page + 1) * PAGE_SIZE))),
    }


class ResultFetcher:
    def __init__(self) -> None:
        # Initialize the current page to start fetching from.
        self.current_page: Optional[int] = 0
        # Hold the results from the most recent page fetch.
        self.current_page_results: list[int] = []
        # A pointer indicating the next result index in the current_page_results list.
        self.current_index: int = 0

    def fetch(self, num_results: int) -> list[int]:
        """
        Returns up to 'num_results' results by sequentially fetching pages from the API.
        Instead of caching extra results in a separate structure, this method uses a pointer
        within the current page's results to track progress between calls.
        """
        results: list[int] = []  # Accumulates the results to be returned.

        # Continue until we've collected the required number of results.
        while len(results) < num_results:
            # If our pointer is at the end of the current page results,
            # fetch the next page if available.
            if self.current_index >= len(self.current_page_results):
                # If there is a valid page to fetch, get the results.
                if self.current_page is not None:
                    page_data = fetch_page(self.current_page)
                    # Update the pointer and the current page results.
                    self.current_page_results = page_data["results"]
                    self.current_index = 0
                    # Update the current_page to the next page as provided by the API.
                    self.current_page = page_data["next_page"]
                    # If no results are returned, there is nothing more to fetch.
                    if not self.current_page_results:
                        break
                else:
                    # No more pages are available.
                    break

            # Determine how many results we can take from the current page.
            available = len(self.current_page_results) - self.current_index
            needed = num_results - len(results)
            take = min(available, needed)

            # Append the slice of results from the current page.
            results.extend(self.current_page_results[self.current_index:self.current_index + take])
            # Move the pointer forward.
            self.current_index += take

        return results


# Test function to verify our solution.
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

    # Create a new instance to test fetching all results in one call.
    fetcher = ResultFetcher()
    test_case(6, fetcher.fetch(200), list(range(103)))
