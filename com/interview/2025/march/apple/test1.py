class ResultFetcher:
    def __init__(self) -> None:
        self.current_page = 0  # tracks the current page number to start fetching from
        self.buffer = []  # buffer to hold leftover results from previous fetch calls

    def fetch(self, num_results: int) -> list[int]:
        results = []  # final result list to be returned

        # Keep fetching until we have enough results or there's nothing left
        while len(results) < num_results:
            # if buffer has enough items, we directly consume from buffer
            if len(self.buffer) >= num_results - len(results):
                # slice enough elements from buffer
                results += self.buffer[: num_results - len(results)]
                # update buffer to remove elements we've already consumed
                self.buffer = self.buffer[num_results - len(results) :]
                break  # we've gathered enough results, exit the loop

            # buffer doesn't have enough, consume what's left
            results += self.buffer
            self.buffer = []  # clear buffer after consuming

            # fetch next page from external API
            page_data = fetch_page(self.current_page)

            # if API returns no further results, exit
            if not page_data["results"]:
                break

            # update current_page pointer for next fetch
            self.current_page = page_data["next_page"] or self.current_page

            # update buffer with fetched results
            self.buffer += page_data["results"]

        return results