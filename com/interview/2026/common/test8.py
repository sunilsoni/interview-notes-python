def ArithmeticEquation(N):
    MOD = 1000007
    # (x-N!)(y-N!) = (N!)^2, count divisors of (N!)^2
    # For each prime p <= N, find exponent in N! via Legendre
    # divisors of (N!)^2 = product of (2*exp+1)
    sieve = [True] * (N + 1)
    primes = []
    for i in range(2, N + 1):
        if sieve[i]:
            primes.append(i)
            for j in range(i * i, N + 1, i):
                sieve[j] = False
    result = 1
    for p in primes:
        exp = 0
        pk = p
        while pk <= N:
            exp += N // pk
            pk *= p
        result = result * (2 * exp + 1) % MOD
    return result

if __name__ == '__main__':
    import time
    tests = [
        (1, 1),
        (2, 3),
        (32327, 656502),
        (3, 9),
        (4, 27),
        (5, 135),
    ]
    # Verify N=3: 3!=6, (6)^2=36, divisors of 36: 1,2,3,4,6,9,12,18,36 = 9
    # Verify N=4: 4!=24, (24)^2=576=2^6*3^2, divs=(6+1)*(2+1)=21... wait
    # 4! = 24 = 2^3 * 3^1, (4!)^2 = 2^6 * 3^2, divs = 7*3 = 21
    # Let me fix test
    tests[3] = (3, 9)  # 3!=6=2*3, (6)^2=2^2*3^2, divs=3*3=9 ✓
    tests[4] = (4, 21) # 4!=24=2^3*3, (24)^2=2^6*3^2, divs=7*3=21
    tests[5] = (5, 105) # 5!=120=2^3*3*5, (120)^2=2^6*3^2*5^2, divs=7*3*3... wait
    # 5! = 120 = 2^3 * 3 * 5, so (5!)^2 = 2^6*3^2*5^2, divs = 7*3*3 = 63
    tests[5] = (5, 63)

    all_pass = True
    for i, (n, exp) in enumerate(tests):
        res = ArithmeticEquation(n)
        status = "PASS" if res == exp else "FAIL"
        if status == "FAIL":
            all_pass = False
        print(f"Test {i}: N={n}, expected={exp}, got={res} -> {status}")

    # Large data test
    t0 = time.time()
    r = ArithmeticEquation(1000000)
    t1 = time.time()
    print(f"Large test: N=10^6, result={r}, time={t1-t0:.3f}s -> {'PASS' if t1-t0<5 else 'FAIL (TLE)'}")

    print(f"\nAll provided tests: {'PASS' if all_pass else 'FAIL'}")