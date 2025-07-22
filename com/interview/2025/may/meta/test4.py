from collections import deque

def process_stream(stream, buffer_size):
    """
    Processes a stream of events with a sliding buffer of `buffer_size`.
    Each time the buffer fills, computes and prints:
      - # of engagements
      - total watch time (in seconds)
      - list of post_ids
    Ignores events marked is_test_content==True when computing metrics.
    """
    buf = deque()  # will hold the last `buffer_size` events

    for event in stream:
        # 1) add new event to the right
        buf.append(event)

        # 2) if we have a full window, compute & print metrics
        if len(buf) == buffer_size:
            # a) filter out test content
            valid = [
                e for e in buf
                if not e.get('is_test_content', False)
            ]

            # b) count total engagements
            total_eng = sum(e['engaged_with_post'] for e in valid)

            # c) sum viewed_time_ms, convert to seconds, round to 3 decimals
            total_ms = sum(e['viewed_time_ms'] for e in valid)
            total_sec = round(total_ms / 1000.0, 3)

            # d) collect post IDs of valid events, in buffer order
            post_ids = [str(e['post_id']) for e in valid]

            # e) formatted output
            print(
                f"You've got {total_eng} engagement(s) "
                f"and spent {total_sec}s viewing content. "
                f"Post ids: {', '.join(post_ids)}"
            )

            # 3) slide window: remove oldest event
            buf.popleft()

def run_tests():
    """
    Defines several test cases (including the provided example and edge cases),
    runs them, and prints PASS/FAIL.
    """
    tests = []

    # -- Example from prompt
    tests.append({
        'name': 'prompt_example',
        'stream': [
            {'post_id': 101, 'viewed_time_ms': 6500, 'engaged_with_post': 1},
            {'post_id': 104, 'viewed_time_ms': 200,  'engaged_with_post': 1},
            {'post_id': 105, 'viewed_time_ms': 4200, 'engaged_with_post': 0, 'is_test_content': True},
            {'post_id': 108, 'viewed_time_ms': 4499, 'engaged_with_post': 1},
            {'post_id': 106, 'viewed_time_ms': 500,  'engaged_with_post': 1},
        ],
        'buffer_size': 3,
        'expected': [
            "You've got 2 engagement(s) and spent 6.7s viewing content. Post ids: 101, 104",
            "You've got 2 engagement(s) and spent 4.699s viewing content. Post ids: 104, 108",
            "You've got 2 engagement(s) and spent 4.999s viewing content. Post ids: 108, 106",
        ]
    })

    # -- Edge case: no events
    tests.append({
        'name': 'empty_stream',
        'stream': [],
        'buffer_size': 3,
        'expected': []
    })

    # -- Edge case: buffer never fills
    tests.append({
        'name': 'never_fills',
        'stream': [
            {'post_id': 1, 'viewed_time_ms': 1000, 'engaged_with_post': 0}
        ],
        'buffer_size': 3,
        'expected': []
    })

    # -- Large data test: generate 10_000 events with no test content
    large_stream = [
        {'post_id': i, 'viewed_time_ms': 1000 + (i % 5)*100, 'engaged_with_post': i % 2}
        for i in range(10_000)
    ]
    # Expect roughly 10_000 - buffer_size + 1 outputs
    expected_count = len(large_stream) - 5 + 1
    tests.append({
        'name': 'large_stream',
        'stream': large_stream,
        'buffer_size': 5,
        'expected_count': expected_count
    })

    # run each test
    for t in tests:
        print(f"\nRunning test `{t['name']}`...")
        # capture printed lines
        from io import StringIO
        import sys

        buf_out = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf_out

        process_stream(t['stream'], t['buffer_size'])

        sys.stdout = old_stdout
        lines = [line.strip() for line in buf_out.getvalue().splitlines() if line.strip()]

        # verify
        if 'expected' in t:
            ok = lines == t['expected']
        else:
            ok = len(lines) == t['expected_count']

        status = "PASS" if ok else "FAIL"
        print(f"  {status}: got {len(lines)} lines; expected "
              f"{len(t.get('expected', ['']*t['expected_count']))}.")
        if not ok:
            print("  -> Got:")
            for l in lines:
                print("    ", l)
            if 'expected' in t:
                print("  -> Expected:")
                for l in t['expected']:
                    print("    ", l)

if __name__ == "__main__":
    run_tests()