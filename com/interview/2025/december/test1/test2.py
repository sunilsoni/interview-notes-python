def solve_vada_pav_tikki():
    """
    Solve: VADA + PAV = TIKKI
    Letters: V, A, D, P, T, I, K (7 unique letters)
    """

    # Try all possible digits for each letter
    # V, P, T cannot be 0 (first letters of words)

    for V in range(1, 10):  # V: 1-9 (not 0)
        for A in range(0, 10):  # A: 0-9
            if A == V:  # must be different
                continue

            for D in range(0, 10):  # D: 0-9
                if D in [V, A]:  # must be different
                    continue

                for P in range(1, 10):  # P: 1-9 (not 0)
                    if P in [V, A, D]:  # must be different
                        continue

                    for T in range(1, 10):  # T: 1-9 (not 0)
                        if T in [V, A, D, P]:  # must be different
                            continue

                        for I in range(0, 10):  # I: 0-9
                            if I in [V, A, D, P, T]:  # must be different
                                continue

                            for K in range(0, 10):  # K: 0-9
                                if K in [V, A, D, P, T, I]:  # must be different
                                    continue

                                # Convert words to numbers
                                VADA = V * 1000 + A * 100 + D * 10 + A
                                PAV = P * 100 + A * 10 + V
                                TIKKI = T * 10000 + I * 1000 + K * 100 + K * 10 + I

                                # Check if equation holds
                                if VADA + PAV == TIKKI:
                                    print("SOLUTION FOUND!")
                                    print(f"V={V}, A={A}, D={D}, P={P}, T={T}, I={I}, K={K}")
                                    print(f"VADA  = {VADA}")
                                    print(f"PAV   = {PAV}")
                                    print(f"TIKKI = {TIKKI}")
                                    print(f"Check: {VADA} + {PAV} = {VADA + PAV}")
                                    print("-" * 40)


# Run the solver
print("Solving: VADA + PAV = TIKKI")
print("=" * 40)
solve_vada_pav_tikki()
print("Done!")