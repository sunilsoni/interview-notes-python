# Python 3 solution with two improved samplers and a simple PASS/FAIL test harness.

import random          # random number generation for sampling and test reproducibility
from bisect import bisect_left   # binary search over prefix sums for O(log n) sampling
from collections import Counter  # compact counting of draws during tests
import time            # quick timing of large-data trials


def _sanitize_weights(weights):
    """
    Make a clean list of (name, w) with only positive weights.
    Raise ValueError if nothing valid remains.
    """
    # Convert any mapping to list of pairs and drop non-positive weights
    cleaned = [(k, int(v)) for k, v in weights.items() if int(v) > 0]
    # If all weights were zero or negative, we cannot sample
    if not cleaned:
        raise ValueError("No positive weights to sample from.")
    return cleaned


def weighted_choice_once(weights):
    """
    Single-shot weighted choice using prefix sums + binary search.
    Build cost: O(n). One draw: O(log n).
    Good when you'll sample a few times or n is small/medium.
    """
    # Ensure we have positive integer weights
    cleaned = _sanitize_weights(weights)

    # Separate names and prefix sums for binary search
    names = []         # holds city names in prefix order
    prefix = []        # holds cumulative sums
    running = 0       # running total while building prefix

    # Build prefix sums: prefix[i] = sum of weights up to index i (inclusive)
    for name, w in cleaned:
        names.append(name)       # store the city name at this position
        running += w             # extend the cumulative total
        prefix.append(running)   # record the new boundary

    # Total weight is the last prefix entry
    total = prefix[-1]

    # Draw a target in [0, total-1]; use integers to avoid float rounding issues
    r = random.randrange(total)

    # Find the first index where prefix[idx] > r
    idx = bisect_left(prefix, r + 1)

    # Return the corresponding city name
    return names[idx]


class WeightedAliasSampler:
    """
    Vose's Alias Method.
    Preprocessing: O(n)
    Draw: O(1)
    Best when you need many samples from the same static distribution.
    """

    def __init__(self, weights):
        # Clean the input first (positive weights only)
        cleaned = _sanitize_weights(weights)

        # Extract names and numeric weights into parallel arrays
        self.names = [name for name, _ in cleaned]   # keep index->name mapping
        w = [float(weight) for _, weight in cleaned] # local float copy of weights
        n = len(w)                                   # number of categories

        # Sum of weights (for normalization)
        total = sum(w)

        # Scale each weight by n / total so average becomes 1.0
        scaled = [wi * n / total for wi in w]

        # Prepare working stacks for small/large groups based on scaled weight
        small = []  # indices with scaled[i] < 1
        large = []  # indices with scaled[i] >= 1

        for i, s in enumerate(scaled):
            (small if s < 1.0 else large).append(i)

        # Allocate arrays:
        # prob[i] stores the "kept" probability within bucket i
        # alias[i] stores fallback index if the coin flip fails
        self.prob = [0.0] * n
        self.alias = [0] * n

        # Core alias table construction
        while small and large:
            i = small.pop()     # take a bucket with deficit (<1)
            j = large.pop()     # take a bucket with surplus (>=1)

            self.prob[i] = scaled[i]  # probability of choosing i within bucket i
            self.alias[i] = j         # otherwise, choose alias j

            # Reduce j's surplus by the amount we gave to i
            scaled[j] = (scaled[j] + scaled[i]) - 1.0

            # Re-classify j depending on its new size
            (small if scaled[j] < 1.0 else large).append(j)

        # Any leftovers are exactly 1.0 (no alias needed)
        for j in large:
            self.prob[j] = 1.0
            self.alias[j] = j
        for i in small:
            self.prob[i] = 1.0
            self.alias[i] = i

    def sample(self):
        """
        Draw one sample in O(1).
        1) Pick a random column k uniformly in [0, n-1].
        2) Flip a biased coin: with prob[k] return names[k]; else names[alias[k]].
        """
        n = len(self.names)                 # number of buckets
        k = random.randrange(n)             # pick a column uniformly
        coin = random.random()              # uniform [0,1)
        # If coin less than prob[k], keep k; else use alias
        return self.names[k] if coin < self.prob[k] else self.names[self.alias[k]]


# ----------------------------
# Simple Monte-Carlo Test Rig
# ----------------------------

def expected_ratios(weights):
    """Return {name: expected_probability} after sanitization."""
    cleaned = _sanitize_weights(weights)
    total = sum(w for _, w in cleaned)
    return {name: w / total for name, w in cleaned}


def run_trials(draw_fn, weights, trials):
    """
    Run `trials` draws using draw_fn() -> name, and return observed ratios.
    draw_fn is a zero-arg callable that returns a sampled name each time.
    """
    counts = Counter()                 # count how many times each name is sampled
    for _ in range(trials):            # repeat sampling
        counts[draw_fn()] += 1         # tally the returned name
    # Convert counts to probabilities by dividing by trials
    return {k: v / float(trials) for k, v in counts.items()}


def pass_fail(observed, expected, tolerance=0.02):
    """
    Compare observed vs expected probabilities with an absolute tolerance.
    Return (passed_bool, details_string).
    """
    msgs = []
    ok = True
    for k in expected:
        obs = observed.get(k, 0.0)                # 0 if never observed
        exp = expected[k]
        diff = abs(obs - exp)
        # Flag if outside tolerance (e.g., 2% = 0.02)
        if diff > tolerance:
            ok = False
            msgs.append(f"{k}: obs={obs:.4f}, exp={exp:.4f}, diff={diff:.4f} > tol")
        else:
            msgs.append(f"{k}: obs={obs:.4f}, exp={exp:.4f}, diff={diff:.4f}")
    return ok, " | ".join(msgs)


def main():
    # Fix seed for reproducibility of test results printed to console
    random.seed(42)

    print("\n=== Test 1: Problem example (NY=7, SF=5, LA=8) ===")
    weights1 = {"NY": 7_000_000, "SF": 5_000_000, "LA": 8_000_000}
    exp1 = expected_ratios(weights1)
    trials = 100_000  # 100k Monte-Carlo draws for stable estimates

    # Binary-search sampler (prefix + bisect)
    obs1_bin = run_trials(lambda: weighted_choice_once(weights1), weights1, trials)
    ok1_bin, msg1_bin = pass_fail(obs1_bin, exp1, tolerance=0.02)
    print(f"[Binary]  PASS={ok1_bin} :: {msg1_bin}")

    # Alias sampler (Vose)
    alias1 = WeightedAliasSampler(weights1)     # build once
    obs1_alias = run_trials(alias1.sample, weights1, trials)
    ok1_alias, msg1_alias = pass_fail(obs1_alias, exp1, tolerance=0.02)
    print(f"[Alias ]  PASS={ok1_alias} :: {msg1_alias}")

    print("\n=== Test 2: Equal weights (A=B=C=D=10) ===")
    weights2 = {"A": 10, "B": 10, "C": 10, "D": 10}
    exp2 = expected_ratios(weights2)
    obs2_alias = run_trials(WeightedAliasSampler(weights2).sample, weights2, trials)
    ok2, msg2 = pass_fail(obs2_alias, exp2, tolerance=0.02)
    print(f"[Alias ]  PASS={ok2} :: {msg2}")

    print("\n=== Test 3: Single city ===")
    weights3 = {"OnlyOne": 999}
    exp3 = expected_ratios(weights3)
    obs3_bin = run_trials(lambda: weighted_choice_once(weights3), weights3, 10_000)
    ok3, msg3 = pass_fail(obs3_bin, exp3, tolerance=0.0)  # must be exact
    print(f"[Binary]  PASS={ok3} :: {msg3}")

    print("\n=== Test 4: Input sanitization (drop zero/negatives) ===")
    weights4 = {"X": 5, "Y": 0, "Z": -3, "W": 5}
    exp4 = expected_ratios(weights4)
    obs4_alias = run_trials(WeightedAliasSampler(weights4).sample, weights4, trials)
    ok4, msg4 = pass_fail(obs4_alias, exp4, tolerance=0.02)
    print(f"[Alias ]  PASS={ok4} :: {msg4}")

    print("\n=== Test 5: Large data sampling ===")
    # Build a large dictionary (e.g., 200k items) with small random weights
    n = 200_000
    large = {f"City_{i}": random.randint(1, 100) for i in range(n)}
    t0 = time.time()
    alias_large = WeightedAliasSampler(large)   # O(n) preprocessing
    t1 = time.time()
    # Draw many samples quickly
    draws = 200_000
    for _ in range(draws):
        _ = alias_large.sample()
    t2 = time.time()
    print(f"Built alias for {n:,} items in {(t1 - t0):.3f}s; "
          f"{draws:,} draws in {(t2 - t1):.3f}s (O(1) draw each).")

    print("\nAll tests executed.\n")


if __name__ == "__main__":
    main()
