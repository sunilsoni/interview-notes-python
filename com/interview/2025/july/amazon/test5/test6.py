from collections import defaultdict, Counter  # defaultdict groups log lines by user; Counter counts triplets efficiently
from typing import List, Tuple, Dict, Iterable, Optional  # Type hints for clarity and maintainability
import time  # For measuring performance on large datasets
import random  # To generate large synthetic test data deterministically
import string  # For generating random page names safely


# Define a type alias for a single log entry for readability.
# Each entry is (timestamp, customerId, page). timestamp can be int or sortable string.
LogEntry = Tuple[object, str, str]  # object allows int/datetime/str; we only need to sort & compare


def extract_triplets_per_user(logs: List[LogEntry]) -> Iterable[Tuple[Tuple[str, str, str], int]]:
    """
    Yields ((p1, p2, p3), count) pairs for all consecutive 3-page sequences per user.
    We do the counting per user first to avoid storing all triplets individually.

    This function:
      1) Groups rows by customerId
      2) Sorts each user's rows by (timestamp, original_index) to make order stable
      3) Slides a window of size 3 over that user's ordered pages
      4) Counts triplets within that user, then yields (triplet, count) for aggregation upstream
    """
    # Build a per-user list of (timestamp, page, original_index) to ensure stable sorting when timestamps tie.
    grouped: Dict[str, List[Tuple[object, str, int]]] = defaultdict(list)  # userId -> list of (timestamp, page, idx)

    # Enumerate with index to preserve original order among equal timestamps.
    for idx, (ts, uid, page) in enumerate(logs):  # iterate all log entries once: O(N)
        grouped[uid].append((ts, page, idx))  # group the visit under the user; keep original index for tie-break

    # For each user, produce triplet counts
    for uid, visits in grouped.items():  # iterate per user; total elements across users still N
        # Sort visits by (timestamp, original_index) to ensure deterministic in-order behavior
        visits.sort(key=lambda x: (x[0], x[2]))  # O(n_u log n_u) per user; stable order even if timestamps equal

        # Extract just the pages in time order for sliding window
        pages = [p for _, p, _ in visits]  # Build a simple list of page names for this user

        # If fewer than 3 visits, there are no 3-page sequences for this user
        if len(pages) < 3:  # Quick guard to avoid unnecessary work
            continue  # Move to next user

        # Count all overlapping triplets for this user with a sliding window of size 3
        user_counter: Counter = Counter()  # local counter per user, avoids pushing millions of items upward directly
        for i in range(len(pages) - 2):  # for each starting index where a 3-length window fits
            triplet = (pages[i], pages[i + 1], pages[i + 2])  # construct the ordered 3-page sequence
            user_counter[triplet] += 1  # increment frequency for this user

        # Yield (triplet, count) pairs so caller can aggregate across all users without storing per-user pages
        for triplet, cnt in user_counter.items():  # iterate unique triplets for this user
            yield triplet, cnt  # stream out counts to keep memory reasonable for very large inputs


def find_top_3_page_sequences(
    logs: List[LogEntry],
    top_n: Optional[int] = None,
    return_all_max: bool = True
) -> List[Tuple[Tuple[str, str, str], int]]:
    """
    Aggregates 3-page sequence frequencies across users and returns the most frequent ones.

    Parameters:
      logs: list of (timestamp, customerId, page) tuples
      top_n: if provided, return the top-N sequences by frequency (ties broken lexicographically).
      return_all_max: if True and top_n is None, return all sequences tied for maximum frequency.

    Returns:
      List of (triplet, count) sorted by:
        - descending count
        - then lex order of the triplet (stable tie-breaking)
    """
    # Aggregate counts across all users by consuming the per-user stream
    global_counter: Counter = Counter()  # global frequency counter across all users

    # Accumulate counts; this folds per-user counts into the global counter
    for triplet, cnt in extract_triplets_per_user(logs):  # iterate streamed (triplet, count) pairs
        global_counter[triplet] += cnt  # add user-specific count into global total

    # If there are no triplets at all (e.g., all users have <3 visits), return empty list
    if not global_counter:  # quick exit for empty result
        return []  # nothing to report

    # Transform to a list sorted by (-count, triplet) for deterministic output
    items = sorted(global_counter.items(), key=lambda x: (-x[1], x[0]))  # descending frequency, then lexicographic triplet

    # If caller wants top-N, return that slice
    if top_n is not None:  # explicit top-N mode
        return items[:top_n]  # top-N sequences by frequency

    # Otherwise, by default return all sequences tied for max frequency
    if return_all_max:  # default behavior
        max_count = items[0][1]  # highest frequency among all triplets
        # Collect all items whose count equals the max
        return [item for item in items if item[1] == max_count]  # all ties for the top
    else:
        # If no return_all_max and no top_n, return the single best
        return items[:1]  # just the most frequent one


def pretty_triplet(tri: Tuple[str, str, str]) -> str:
    """Helper to format a triplet nicely as 'A -> B -> C'."""
    return f"{tri[0]} -> {tri[1]} -> {tri[2]}"  # simple readable arrow-form for console output


def run_single_test(
    name: str,
    logs: List[LogEntry],
    expect_any_of: List[List[Tuple[Tuple[str, str, str], int]]],
    top_n: Optional[int] = None,
    return_all_max: bool = True,
    verbose: bool = False
) -> bool:
    """
    Runs one test:
      - Executes the finder
      - Compares output against one or more acceptable expected lists (to allow tie variants)
      - Prints PASS/FAIL

    Parameters:
      name: label for the test
      logs: input log entries
      expect_any_of: list of acceptable expected outputs (each is a list[(triplet, count)])
      top_n, return_all_max: passed to find_top_3_page_sequences
      verbose: if True, prints detailed outputs

    Returns:
      True if test passes; False otherwise.
    """
    # Run the algorithm under test with given knobs
    result = find_top_3_page_sequences(logs, top_n=top_n, return_all_max=return_all_max)  # compute actual result

    # Optionally show detailed info
    if verbose:  # extra debugging output when needed
        print(f"[{name}] Result:")
        for tri, c in result:
            print(f"  {pretty_triplet(tri)}  count={c}")

    # Compare against any acceptable expected list
    for expected in expect_any_of:  # iterate all acceptable expectations
        if result == expected:  # exact list equality (order and counts)
            print(f"TEST {name}: PASS")  # success path
            return True  # early return on pass

    # If none matched, print fail with a small diff
    print(f"TEST {name}: FAIL")  # test failed
    print("  Expected any of:")
    for e in expect_any_of:
        print("   -", [(pretty_triplet(t), c) for t, c in e])
    print("  But got:")
    print("   -", [(pretty_triplet(t), c) for t, c in result])
    return False  # signal failure


def build_large_synthetic_dataset(
    num_users: int,
    pages_pool: List[str],
    visits_per_user: int,
    seed: int = 42
) -> List[LogEntry]:
    """
    Create a large synthetic dataset for performance testing.
    We also embed a known frequent pattern so we can assert correctness.

    Strategy:
      - For each user, generate a random walk of pages with a bias to include a specific 'hot' pattern.
      - Timestamps increase by 1 to keep order simple and sortable ints.

    Returns:
      logs: list of (timestamp, userId, page)
    """
    # Fix the RNG seed for reproducibility across runs
    random.seed(seed)  # deterministic generation

    logs: List[LogEntry] = []  # collect all synthetic log entries here

    # Define a hot pattern we want to appear very frequently
    hot = ("A", "B", "C")  # the planted most-common triplet
    # We’ll bias generation so that for many users, parts of their sequence include A->B->C chunks.

    ts = 0  # global, monotonically increasing timestamp
    for u in range(num_users):  # loop over users
        uid = f"user_{u}"  # user id string
        pages = []  # build this user's page sequence

        i = 0  # index over this user's visit count
        while i < visits_per_user:  # create visits_per_user events
            # With some probability, inject the hot pattern to ensure it's dominant
            if i <= visits_per_user - 3 and random.random() < 0.25:  # 25% chance to inject and enough room left
                pages.extend(list(hot))  # add A, B, C in order
                i += 3  # we just added three visits
            else:
                # Otherwise, add a random page from the pool
                pages.append(random.choice(pages_pool))  # random non-hot page
                i += 1  # added one visit

        # Now create log entries for this user's pages
        for p in pages:  # for each page visit in order
            logs.append((ts, uid, p))  # create the log tuple
            ts += 1  # ensure global timestamp always increases so dataset is globally time-sorted

    return logs  # return the synthetic dataset


def main():
    """Simple main: builds test cases, runs them, prints PASS/FAIL, and does a large-data run."""
    # -----------------------------
    # Small / Medium test cases
    # -----------------------------
    tests_passed = True  # track cumulative result

    # 1) Single user, exactly one triple
    logs1 = [
        (1, "u1", "A"),
        (2, "u1", "B"),
        (3, "u1", "C"),
    ]  # only one 3-page sequence: (A,B,C)
    expect1 = [[(( "A","B","C"), 1)]]  # only (A,B,C) with count 1
    tests_passed &= run_single_test("SingleUserOneTriple", logs1, expect1)

    # 2) Single user, overlapping triples
    logs2 = [
        (10, "u1", "A"),
        (11, "u1", "B"),
        (12, "u1", "C"),
        (13, "u1", "D"),
    ]  # Triples: (A,B,C), (B,C,D)
    # Both appear once; both tied for max=1. We return all tied (two items), sorted lexicographically by triplet.
    expect2 = [[
        (("A","B","C"), 1),
        (("B","C","D"), 1),
    ]]
    tests_passed &= run_single_test("SingleUserOverlapping", logs2, expect2)

    # 3) Multiple users, counts aggregate
    logs3 = [
        (1, "u1", "A"), (2, "u1", "B"), (3, "u1", "C"),
        (4, "u2", "A"), (5, "u2", "B"), (6, "u2", "C"),
        (7, "u3", "B"), (8, "u3", "C"), (9, "u3", "D"),
    ]  # (A,B,C)=2, (B,C,D)=1
    expect3 = [[
        (("A","B","C"), 2),  # unique max
    ]]
    tests_passed &= run_single_test("MultiUserAggregate", logs3, expect3)

    # 4) Unsorted input: same user shuffled timestamps
    logs4 = [
        (5, "u1", "B"),
        (3, "u1", "A"),
        (7, "u1", "C"),
        (9, "u1", "D"),
    ]  # After sort by time: A,B,C,D -> triples: (A,B,C), (B,C,D)
    expect4 = [[
        (("A","B","C"), 1),
        (("B","C","D"), 1),
    ]]
    tests_passed &= run_single_test("UnsortedInputPerUser", logs4, expect4)

    # 5) Users with <3 visits should be ignored safely
    logs5 = [
        (1, "u1", "A"), (2, "u1", "B"),  # only 2 visits -> no triples
        (3, "u2", "X"), (4, "u2", "Y"), (5, "u2", "Z"),  # one triple
    ]
    expect5 = [[
        (("X","Y","Z"), 1),
    ]]
    tests_passed &= run_single_test("UsersWithFewerThan3", logs5, expect5)

    # 6) Tie for max among multiple sequences across users
    logs6 = [
        (1, "u1", "A"), (2, "u1", "B"), (3, "u1", "C"),
        (4, "u2", "B"), (5, "u2", "C"), (6, "u2", "D"),
        (7, "u3", "A"), (8, "u3", "B"), (9, "u3", "C"),
        (10, "u4", "B"), (11, "u4", "C"), (12, "u4", "D"),
    ]  # (A,B,C)=2, (B,C,D)=2 -> tie; we return both sorted by triplet
    expect6 = [[
        (("A","B","C"), 2),
        (("B","C","D"), 2),
    ]]
    tests_passed &= run_single_test("GlobalTie", logs6, expect6)

    # 7) Same timestamp tie-breaking by original order
    logs7 = [
        (100, "u1", "A"),
        (100, "u1", "B"),  # same ts as previous, but comes after in input -> we keep this order
        (101, "u1", "C"),
        (101, "u1", "D"),
    ]  # Ordered by (ts, original_idx) -> A,B,C,D -> triples: (A,B,C), (B,C,D)
    expect7 = [[
        (("A","B","C"), 1),
        (("B","C","D"), 1),
    ]]
    tests_passed &= run_single_test("SameTimestampStableOrder", logs7, expect7)

    # 8) top_n usage: request top 1 only
    logs8 = [
        (1, "u1", "A"), (2, "u1", "B"), (3, "u1", "C"),
        (4, "u2", "A"), (5, "u2", "B"), (6, "u2", "C"),
        (7, "u3", "B"), (8, "u3", "C"), (9, "u3", "D"),
    ]  # top is (A,B,C)=2
    expect8 = [[
        (("A","B","C"), 2),
    ]]
    tests_passed &= run_single_test("TopN=1", logs8, expect8, top_n=1, return_all_max=False)

    # 9) No triplets at all -> empty result
    logs9 = [
        (1, "u1", "A"),
        (2, "u2", "B"),
        (3, "u3", "C"),
    ]  # nobody has 3 visits
    expect9 = [[]]  # expect empty list
    tests_passed &= run_single_test("NoTriplets", logs9, expect9)

    # 10) Duplicate pages allowed; consecutive duplicates form valid sequences
    logs10 = [
        (1, "u1", "A"),
        (2, "u1", "A"),
        (3, "u1", "B"),
        (4, "u1", "C"),
    ]  # pages: A,A,B,C -> triples: (A,A,B), (A,B,C)
    expect10 = [[
        (("A","A","B"), 1),
        (("A","B","C"), 1),
    ]]
    tests_passed &= run_single_test("DuplicatePagesAllowed", logs10, expect10)

    # -----------------------------
    # Large data performance test
    # -----------------------------
    pages_pool = list(string.ascii_uppercase[:10])  # pages 'A'..'J' as the pool
    # Build a large dataset: tune sizes to your environment; this is reasonable for a quick local run
    num_users = 5000  # number of users in the large test
    visits_per_user = 40  # visits per user; 5000*40=200k rows total
    large_logs = build_large_synthetic_dataset(num_users, pages_pool, visits_per_user, seed=2025)  # generate data

    # Expectation: our generator plants ('A','B','C') frequently, so it should be the top 1.
    start = time.time()  # start timing
    top1 = find_top_3_page_sequences(large_logs, top_n=1, return_all_max=False)  # run finder on big data
    elapsed = time.time() - start  # compute elapsed seconds

    # Validate: top1 should exist and its triplet should be ('A','B','C')
    expected_top = [(("A","B","C"), top1[0][1])] if top1 else []  # only compare the triplet, count is data-dependent
    if top1 and top1[0][0] == ("A","B","C"):  # check most frequent is the planted hot pattern
        print(f"TEST LargeDataTop1: PASS  (rows={len(large_logs)}, took={elapsed:.3f}s)")
    else:
        print(f"TEST LargeDataTop1: FAIL  (rows={len(large_logs)}, took={elapsed:.3f}s)")
        print("  Got:", [(pretty_triplet(t), c) for t, c in top1])
        print("  Expected most frequent triplet to be: ('A','B','C')")

    # Final summary
    print("\nALL SMALL/MED TESTS PASSED?" , "YES" if tests_passed else "NO")  # overall outcome for small/medium tests


# Entry point guard for script-style execution
if __name__ == "__main__":  # standard Python main guard
    main()  # run all tests and the large dataset performance check