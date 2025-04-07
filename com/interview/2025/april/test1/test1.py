from typing import TypedDict, Optional


# ---------------------------
# External API and Constants
# ---------------------------

# Define the expected structure for the API's response using TypedDict.
class FetchPageResult(TypedDict):
    next_page: Optional[int]  # The next page number; None if there are no more pages.
    results: list[int]  # The list of integers returned on the current page.


# Constants for testing (DO NOT change these)
MAX_RESULTS = 103  # Total number of available results.
PAGE_SIZE = 10  # Number of results per API call.


# This function simulates a paginated API.
def fetch_page(page: int) -> FetchPageResult:
    # If the starting index for this page is equal to or exceeds MAX_RESULTS,
    # return an empty list and indicate no next page.
    if page * PAGE_SIZE >= MAX_RESULTS:
        return {"next_page": None, "results": []}

    # Otherwise, return a chunk of results starting at page * PAGE_SIZE.
    return {
        "next_page": page + 1,  # The next page to be fetched.
        "results": list(
            range(page * PAGE_SIZE, min(MAX_RESULTS, (page + 1) * PAGE_SIZE))
        ),
    }


# ---------------------------
# Implementation of ResultFetcher
# ---------------------------
class ResultFetcher:
    def __init__(self) -> None:
        # Initialize the starting page for fetching (page 0).
        self.current_page = 0
        # Initialize an empty buffer to store results fetched from the API
        # that have not yet been returned to the caller.
        self.buffer = []

    def fetch(self, num_results: int) -> list[int]:
        # This list will hold the results to be returned.
        fetched_results = []

        # Continue fetching until we've collected the desired number of results
        # or until the API has no more results.
        while len(fetched_results) < num_results:
            # If the internal buffer is empty, we need to fetch a new page.
            if not self.buffer:
                # If there are no more pages to fetch (current_page is None),
                # break out of the loop because the API is exhausted.
                if self.current_page is None:
                    break

                # Call the external paginated API with the current page number.
                page_result = fetch_page(self.current_page)

                # If the API returns an empty list of results,
                # update current_page to None and break out of the loop.
                if not page_result["results"]:
                    self.current_page = None
                    break

                # Add the new results to the internal buffer.
                self.buffer.extend(page_result["results"])

                # Update the current page number using the API's 'next_page' value.
                # This will be None if there are no further pages.
                self.current_page = page_result["next_page"]

            # Determine the number of additional results needed to meet the request.
            remaining_needed = num_results - len(fetched_results)

            # Extract as many results from the buffer as needed (or all if there are fewer).
            to_take = self.buffer[:remaining_needed]
            # Add the extracted results to the list of fetched results.
            fetched_results.extend(to_take)
            # Remove the results that were just used from the buffer.
            self.buffer = self.buffer[remaining_needed:]

        # Return the list of results collected.
        # Note: This list may contain fewer than 'num_results' items if the API is exhausted.
        return fetched_results


# ---------------------------
# Test Code
# ---------------------------
def test_case(test_case: int, actual: list[int], expected: list[int]) -> None:
    # Check if the actual output matches the expected output.
    if actual == expected:
        print(f"Test Case {test_case}: SUCCESS")
    else:
        print(f"Test Case {test_case}: FAILED")
        print(f"Expected {expected}. Got {actual}")


if __name__ == "__main__":
    # Create a ResultFetcher instance to test sequential fetching.
    fetcher = ResultFetcher()

    # Test 1: Fetch first 5 results. Expect [0, 1, 2, 3, 4]
    test_case(1, fetcher.fetch(5), list(range(5)))

    # Test 2: Fetch next 2 results. Expect [5, 6]
    test_case(2, fetcher.fetch(2), list(range(5, 7)))

    # Test 3: Fetch next 7 results. Expect [7, 8, 9, 10, 11, 12, 13]
    test_case(3, fetcher.fetch(7), list(range(7, 14)))

    # Test 4: Attempt to fetch 103 results.
    # Since 14 results have been already returned, expect the rest: [14, 15, ..., 102]
    test_case(4, fetcher.fetch(103), list(range(14, 103)))

    # Test 5: Further fetch should return an empty list (API exhausted).
    test_case(5, fetcher.fetch(10), [])

    # Test 6: A new fetcher instance should start from the beginning.
    fetcher = ResultFetcher()
    # Requesting 200 results should return all available results, i.e., [0, 1, ..., 102]
    test_case(6, fetcher.fetch(200), list(range(103)))