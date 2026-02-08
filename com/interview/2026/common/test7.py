import sys


def ArithmeticEquation(N):
    MOD = 1000007
    if N == 1: return 1

    # The problem reduces to finding the number of divisors of (N!)^2
    # Formula: If (N!)^2 = p1^a1 * p2^a2..., then divisors = (a1+1)(a2+1)...
    # For N!, the exponent of prime p is sum(floor(N/p^k))

    limit = N
    primes = []
    is_prime = [True] * (limit + 1)
    for p in range(2, limit + 1):
        if is_prime[p]:
            primes.append(p)
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False

    total_divisors = 1
    for p in primes:
        exponent_in_n_fact = 0
        temp_n = N
        while temp_n >= p:
            exponent_in_n_fact += temp_n // p
            temp_n //= p

        # Exponent in (N!)^2 is 2 * exponent_in_N!
        total_divisors = (total_divisors * (2 * exponent_in_n_fact + 1)) % MOD

    return total_divisors


def test():
    test_cases = [
        (1, 1),
        (2, 3),
        (32327, 656502)
    ]

    for n_val, expected in test_cases:
        result = ArithmeticEquation(n_val)
        status = "PASS" if result == expected else f"FAIL (Got {result})"
        print(f"N={n_val}: {status}")


if __name__ == "__main__":
    test()