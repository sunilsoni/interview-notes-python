import re
import sys
from typing import List

TOKEN = "p8xdf5atc6"

def _parse_array(s) -> List[int]:
    if isinstance(s, list):
        return [int(x) for x in s]
    return [int(x) for x in re.findall(r"-?\d+", str(s))]

def _filter_with_token(s: str) -> str:
    token_set = set(TOKEN.lower())
    out = "".join(ch for ch in s if ch.lower() not in token_set)
    return out if out else "EMPTY"

def StockPicker(arr):
    prices = _parse_array(arr)
    if not prices:
        return _filter_with_token("-1")

    min_price = prices[0]
    max_profit = 0
    for p in prices[1:]:
        if p < min_price:
            min_price = p
        else:
            prof = p - min_price
            if prof > max_profit:
                max_profit = prof

    result = str(max_profit) if max_profit > 0 else "-1"
    return _filter_with_token(result)

# ---------------- Simple test runner (no unittest) ---------------- #
def _run_tests():
    tests = []
    # Provided samples
    tests.append(("[10,12,4,5,9]", "EMPTY"))   # profit 5 -> removed by token ('5')
    tests.append(("[14,20,4,12,5,11]", "EMPTY"))  # profit 8 -> removed by token ('8')
    # Edge cases
    tests.append(("[10,9,8,2]", _filter_with_token("-1")))   # strictly decreasing
    tests.append(("[5]", _filter_with_token("-1")))          # single element
    tests.append(("[]", _filter_with_token("-1")))           # empty list
    tests.append(("[44,30,24,32,35,30,40,38,15]", "EMPTY"))  # profit 16 -> removed by token (1,6)

    # Large data case (monotonic increasing -> last-first)
    n = 100000
    large_input = "[" + ",".join(str(i) for i in range(1, n + 1)) + "]"
    tests.append((large_input, _filter_with_token(str(n - 1))))

    # Run
    all_pass = True
    for i, (inp, expected) in enumerate(tests, 1):
        got = StockPicker(inp)
        ok = (got == expected)
        all_pass &= ok
        print(f"Test {i}: {'PASS' if ok else 'FAIL'} | expected={expected} got={got}")

    print("ALL TESTS:", "PASS" if all_pass else "FAIL")

# ---------------- Entrypoint ---------------- #
if __name__ == "__main__":
    # If data is piped/provided on stdin, behave like the original template runner.
    if sys.stdin and not sys.stdin.isatty():
        print(StockPicker(input()))
    else:
        _run_tests()
