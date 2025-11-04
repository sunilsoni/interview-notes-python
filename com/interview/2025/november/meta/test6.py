# merge_intervals_union.py
# Python3 solution with line-by-line comments and a main() test harness that prints PASS/FAIL.

from typing import List, Tuple  # import typing annotations for clarity and readability (not required at runtime)

def merge_two_sorted_interval_lists(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    # Define a function that merges two sorted, non-overlapping interval lists into one unioned list.
    # `a` and `b` are lists of [start, end], and each list is sorted by start and has no internal overlaps.

    i = 0  # pointer for list `a`; starts at the first interval in `a`
    j = 0  # pointer for list `b`; starts at the first interval in `b`
    result: List[List[int]] = []  # result list to accumulate merged intervals; initially empty

    # Loop until one of the input lists is fully consumed
    while i < len(a) and j < len(b):  # while both lists still have intervals to process
        # Choose the interval with the smaller start value to process next
        if a[i][0] <= b[j][0]:  # if next interval in `a` starts earlier or equal
            curr = a[i]  # take the current interval from `a`
            i += 1  # advance pointer `i` because we've taken this interval from `a`
        else:
            curr = b[j]  # take the current interval from `b` (it starts earlier)
            j += 1  # advance pointer `j` for `b`

        # If result is empty or last interval in result does not overlap with `curr`, append it
        if not result or result[-1][1] < curr[0]:
            # no overlap: either result empty or last interval ends strictly before curr starts
            result.append([curr[0], curr[1]])  # append a copy of curr to result to avoid aliasing
        else:
            # overlap case: extend the end of the last interval in result to cover curr
            # use max to keep the farthest end among the overlapping intervals
            last = result[-1]  # reference to last interval object in result
            if curr[1] > last[1]:  # only update if curr extends beyond last
                last[1] = curr[1]  # extend last interval's end to include curr's end

    # At this point at least one of the lists is exhausted; process any remaining intervals from `a`
    while i < len(a):  # while there are remaining intervals in `a`
        curr = a[i]  # take next interval from `a`
        i += 1  # advance pointer
        if not result or result[-1][1] < curr[0]:  # no overlap with last result interval
            result.append([curr[0], curr[1]])  # append a copy of curr
        else:
            # merge with last interval by extending end if needed
            last = result[-1]  # last interval in result
            if curr[1] > last[1]:  # if curr extends last interval's end
                last[1] = curr[1]  # update end

    # Process any remaining intervals from `b` in the same way
    while j < len(b):  # while there are remaining intervals in `b`
        curr = b[j]  # take next interval from `b`
        j += 1  # advance pointer `j`
        if not result or result[-1][1] < curr[0]:  # if there's no overlap with result's last interval
            result.append([curr[0], curr[1]])  # append curr
        else:
            last = result[-1]  # reference to last interval
            if curr[1] > last[1]:  # if curr extends the last interval's end
                last[1] = curr[1]  # extend it

    return result  # return the merged union list


# A simple "naive" implementation used only for verifying correctness in tests.
# It concatenates both lists, sorts them, and then merges sequentially.
def naive_union_for_test(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    # Combine both lists into one list
    combined = []  # empty combined list
    # extend combined with shallow copies to avoid accidental aliasing
    combined.extend([ [iv[0], iv[1]] for iv in a ])  # add intervals from `a`
    combined.extend([ [iv[0], iv[1]] for iv in b ])  # add intervals from `b`
    # sort combined list by start time
    combined.sort(key=lambda x: x[0])  # sort by interval start
    # now merge overlaps in one pass
    merged: List[List[int]] = []  # result for naive approach
    for iv in combined:  # iterate through sorted intervals
        if not merged or merged[-1][1] < iv[0]:  # if no overlap with last merged interval
            merged.append([iv[0], iv[1]])  # append a copy
        else:
            # overlap: extend last's end if this interval reaches further
            if iv[1] > merged[-1][1]:
                merged[-1][1] = iv[1]
    return merged  # return merged result


# The main test harness (requested: no unit testing frameworks; simple main function)
def main():
    # Define a list of test cases as tuples: (list_a, list_b, expected)
    test_cases: List[Tuple[List[List[int]], List[List[int]], List[List[int]]]] = [
        # Example from the screenshot
        ([[1,2],[5,9]], [[4,6],[8,10],[11,12]], [[1,2],[4,10],[11,12]]),
        # both empty
        ([], [], []),
        # one empty
        ([[1,3],[5,7]], [], [[1,3],[5,7]]),
        ([], [[2,4]], [[2,4]]),
        # touching intervals (should merge)
        ([[1,2]], [[2,3]], [[1,3]]),
        # nested intervals from the other list
        ([[1,10]], [[2,3],[4,5],[6,7]], [[1,10]]),
        # non-overlapping separated intervals
        ([[1,2],[10,12]], [[3,4],[13,14]], [[1,2],[3,4],[10,12],[13,14]]),
        # overlapping across lists with many merges
        ([[1,5],[10,14]], [[2,6],[7,11],[12,15]], [[1,6],[7,15]]),
    ]

    # Run each small test and print PASS/FAIL with details
    print("Running small test cases:")
    all_ok = True  # flag to record if all small tests pass
    for idx, (a, b, expected) in enumerate(test_cases, start=1):
        got = merge_two_sorted_interval_lists([iv[:] for iv in a], [iv[:] for iv in b])  # call function with copies
        ok = got == expected  # check equality with expected
        if not ok:
            all_ok = False  # record failure
        # print detailed result for this test
        print(f"Test {idx}: ", "PASS" if ok else "FAIL")
        if not ok:  # if failed, show details
            print("  A      =", a)
            print("  B      =", b)
            print("  Expected =", expected)
            print("  Got      =", got)

    # Use naive_union_for_test as an oracle to validate our algorithm against many random or large inputs
    # Large-data test: build two large lists (non-overlapping internally) but possibly overlapping with each other
    import random  # random numbers for large test
    random.seed(0)  # fixed seed for reproducibility

    def make_nonoverlapping_intervals(count, start_base=0, max_span=5, gap_min=1, gap_max=3):
        # Helper to create `count` non-overlapping intervals that are sorted.
        # start_base: value to start from
        # max_span: max length of an interval
        # gap_min/gap_max: min/max gap between successive intervals' starts
        res = []  # result list
        cur = start_base  # current start cursor
        for _ in range(count):  # generate count intervals
            span = random.randint(1, max_span)  # length of this interval
            res.append([cur, cur + span])  # append interval [cur, cur+span]
            # move cur forward by span plus a random gap to avoid internal overlaps
            cur = cur + span + random.randint(gap_min, gap_max)
        return res  # return generated list

    # Create large lists; choose size moderate to be safe in interactive environment
    large_n = 2000  # number of intervals for list a (adjustable; 2000 gives reasonable time here)
    large_m = 2500  # number of intervals for list b
    A_large = make_nonoverlapping_intervals(large_n, start_base=0, max_span=10, gap_min=0, gap_max=5)
    B_large = make_nonoverlapping_intervals(large_m, start_base=3, max_span=10, gap_min=0, gap_max=5)

    # Validate our linear algorithm against the naive (sort+merge) oracle
    print("\nRunning large-data verification (comparing to naive oracle)...")
    merge_fast = merge_two_sorted_interval_lists([iv[:] for iv in A_large], [iv[:] for iv in B_large])  # fast result
    merge_naive = naive_union_for_test(A_large, B_large)  # oracle result
    large_ok = merge_fast == merge_naive  # compare results
    print("Large test:", "PASS" if large_ok else "FAIL")
    if not large_ok:  # if mismatch, print sizes and small sample
        print("  len(A_large) =", len(A_large))
        print("  len(B_large) =", len(B_large))
        print("  len(fast)    =", len(merge_fast))
        print("  len(naive)   =", len(merge_naive))
        # show first few to inspect
        print("  fast[:10]   =", merge_fast[:10])
        print("  naive[:10]  =", merge_naive[:10])

    # Summary of overall success
    if all_ok and large_ok:
        print("\nAll tests PASS.")
    else:
        print("\nSome tests FAILED; inspect outputs above.")


# Run main when executed as a script
if __name__ == "__main__":
    main()
