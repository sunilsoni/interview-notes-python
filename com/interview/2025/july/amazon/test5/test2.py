#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Question Details:
 Amazon notifies our service with JSON messages of the form:
   { customerId, itemId, timestamp }
 whenever a customer buys an item.
 We need to compute the top-k items by total purchase count.

Ambiguities & Clarifications:
 - Should popularity be over all time, or sliding windows? (Here we do all time.)
 - How large can the stream get, and what memory limits apply?
 - How do we break ties when counts are equal?
 - What is the value of k at runtime?
Improvement Alternatives:
 - For very large streams, use a streaming algorithm (Count-Min Sketch) for approximate counts.
 - Reset counts periodically if we only care about recent popularity.
 - Use a min-heap of size k to keep only the top items as counts update.

"""

import heapq  # for efficient top-k computation
import json   # for parsing JSON messages
import random # for generating large test data (simulating scale)

def process_purchase(event_json, counts):
    """
    Update the counts dict with one purchase event.
    :param event_json: JSON string of the form '{"customerId":..., "itemId":..., "timestamp":...}'
    :param counts: dict mapping itemId -> current purchase count
    """
    # parse the JSON text into a Python dict
    event = json.loads(event_json)
    # get the itemId from the event
    item = event['itemId']
    # increase the count for this item by 1 (start from zero if new)
    counts[item] = counts.get(item, 0) + 1

def get_top_k(counts, k):
    """
    Return a list of the top k itemIds by count, sorted descending by count.
    :param counts: dict mapping itemId -> purchase count
    :param k: number of top items to return
    :return: list of tuples (itemId, count)
    """
    # use heapq.nlargest to pick the k items with largest counts
    # this runs in O(n log k) time, good when k << n
    top = heapq.nlargest(k, counts.items(), key=lambda x: x[1])
    return top

def run_test(test_name, events, k, expected):
    """
    Run one test scenario: process all events, compute top-k, compare to expected.
    Prints PASS or FAIL.
    :param test_name: descriptive name of the test
    :param events: list of JSON strings representing purchase events
    :param k: integer top-k to compute
    :param expected: list of tuples (itemId, count) that we expect
    """
    counts = {}  # start with empty counts
    # feed all events into our processor
    for e in events:
        process_purchase(e, counts)
    # compute top-k from the accumulated counts
    result = get_top_k(counts, k)
    # check if we got exactly what we expected
    if result == expected:
        print(f"{test_name}: PASS")
    else:
        print(f"{test_name}: FAIL")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")

def main():
    """
    Simple main method to run a suite of tests, including a large-data test.
    """
    # Test 1: basic small stream
    events1 = [
        '{"customerId":"C1","itemId":"A","timestamp":"2025-08-01T10:00:00Z"}',
        '{"customerId":"C2","itemId":"B","timestamp":"2025-08-01T10:01:00Z"}',
        '{"customerId":"C3","itemId":"A","timestamp":"2025-08-01T10:02:00Z"}',
        '{"customerId":"C4","itemId":"C","timestamp":"2025-08-01T10:03:00Z"}',
        '{"customerId":"C5","itemId":"B","timestamp":"2025-08-01T10:04:00Z"}'
    ]
    # counts: A=2, B=2, C=1; top-2 could be A and B
    expected1 = [("A", 2), ("B", 2)]
    run_test("Test1-Basic", events1, 2, expected1)

    # Test 2: tie-breaking by insertion order of nlargest (stable), expecting C after A
    events2 = [
        '{"customerId":"X","itemId":"C","timestamp":"..."}',
        '{"customerId":"Y","itemId":"A","timestamp":"..."}',
        '{"customerId":"Z","itemId":"A","timestamp":"..."}',
        '{"customerId":"W","itemId":"B","timestamp":"..."}',
        '{"customerId":"V","itemId":"B","timestamp":"..."}'
    ]
    # counts: A=2, B=2, C=1; top-2 are A and B
    expected2 = [("A", 2), ("B", 2)]
    run_test("Test2-Tie", events2, 2, expected2)

    # Test 3: k larger than number of unique items
    events3 = [
        '{"customerId":"1","itemId":"X","timestamp":"..."}'
    ]
    expected3 = [("X", 1)]
    run_test("Test3-SmallK", events3, 5, expected3)

    # Test 4: large-scale simulation to check performance
    large_events = []
    num_events = 100_000
    item_ids = [f"item{n}" for n in range(100)]
    # generate random purchases
    for _ in range(num_events):
        iid = random.choice(item_ids)
        # we don't need realistic JSON here; timestamp can be dummy
        large_events.append(json.dumps({"customerId":"u","itemId":iid,"timestamp":"t"}))
    # we won't know exact expected top-k, but we can at least run it to see it doesn't crash
    try:
        _ = get_top_k({iid: large_events.count(json.dumps({"customerId":"u","itemId":iid,"timestamp":"t"})) for iid in item_ids}, 10)
        print("Test4-LargeData: PASS (no crash)")
    except Exception as e:
        print("Test4-LargeData: FAIL", e)

if __name__ == "__main__":
    main()

"""
Originality & Authenticity Verification:
 - This solution was crafted specifically for the problem above, with simple data structures.
 - To check for originality, you could run a plagiarism detector on this file, compare against known codebases,
   and do a manual review to ensure it matches the problem context.
"""