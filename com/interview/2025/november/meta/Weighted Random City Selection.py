# Import statements - these provide additional functionality we need
import random  # For random number generation
from bisect import bisect_right  # For efficient binary search on sorted lists


# ============================================================================
# HIGH-LEVEL OVERVIEW OF THE SOLUTION
# ============================================================================
# 1. Calculate total population of all cities
# 2. Create cumulative probability distribution (0 to 1)
# 3. Generate random number between 0 and 1
# 4. Use binary search to find which city the random number falls into
# 5. Return that city
# ============================================================================

def weighted_random_city(city_population_map):
    """
    Selects a random city based on population weight.

    Args:
        city_population_map: Dictionary with city names as keys, populations as values

    Returns:
        A randomly selected city name (string)

    Example:
        Input: {'NY': 7000000, 'SF': 5000000, 'LA': 8000000}
        Output: 'NY' (or 'SF' or 'LA' based on weighted probability)
    """

    # Step 1: Validate input - Check if the dictionary is empty
    # Purpose: Prevent errors when processing an empty map
    # Logic: If map is empty, we cannot select any city
    if not city_population_map:
        raise ValueError("City population map cannot be empty")

    # Step 2: Extract city names and their populations into separate lists
    # Purpose: Keep data organized and accessible for calculation
    # Logic: Convert dictionary keys to list for indexing
    cities = list(city_population_map.keys())

    # Purpose: Extract all population values from the dictionary
    # Logic: Use values() method to get all populations in same order as cities
    populations = list(city_population_map.values())

    # Step 3: Calculate total population across all cities
    # Purpose: Needed to calculate individual probabilities
    # Logic: Sum all populations to get denominator for probability calculation
    # Example: 7,000,000 + 5,000,000 + 8,000,000 = 20,000,000
    total_population = sum(populations)

    # Step 4: Build cumulative probability distribution
    # Purpose: Create a sorted list of cumulative probabilities for binary search
    # Logic: Each element represents cumulative probability up to that city
    # Example with our data:
    #   NY: 7M/20M = 0.35, cumulative = 0.35
    #   SF: 5M/20M = 0.25, cumulative = 0.35 + 0.25 = 0.60
    #   LA: 8M/20M = 0.40, cumulative = 0.60 + 0.40 = 1.00
    cumulative_probabilities = []

    # Variable to keep track of running sum of probabilities
    # Purpose: Calculate each city's cumulative probability
    cumulative_sum = 0

    # Loop through each city and its population
    # Purpose: Calculate cumulative probability for each city
    for population in populations:
        # Add current city's probability to the running sum
        # Logic: individual_probability = population / total_population
        # This value is added to cumulative sum
        cumulative_sum += population / total_population

        # Append the cumulative probability to our list
        # Purpose: Store cumulative value for binary search lookup
        cumulative_probabilities.append(cumulative_sum)

    # Step 5: Generate random number between 0 and 1
    # Purpose: This random number will be used to select a city
    # Logic: random.random() returns float from 0.0 to 1.0
    # Example: might return 0.45
    random_value = random.random()

    # Step 6: Find which city corresponds to our random value
    # Purpose: Use binary search to efficiently find the city
    # Logic: bisect_right finds the position where random_value fits in cumulative list
    # How it works:
    #   If random_value = 0.45 and cumulative = [0.35, 0.60, 1.00]
    #   bisect_right returns index 1 (falls between 0.35 and 0.60, so SF's position)
    # Why binary search? Much faster than looping, especially with many cities
    # Time: O(log n) instead of O(n)
    city_index = bisect_right(cumulative_probabilities, random_value)

    # Step 7: Return the selected city
    # Purpose: Return the city name that corresponds to the selected index
    # Logic: Use index to get city from our cities list
    return cities[city_index]


# ============================================================================
# TESTING SUITE - USING MAIN METHOD (NOT UNITTEST)
# ============================================================================

def run_tests():
    """
    Main testing function that checks all test cases.
    Reports PASS/FAIL for each test case.
    """

    # Counter to track test results
    # Purpose: Keep count of passed and failed tests
    total_tests = 0
    passed_tests = 0

    # Test case counter for display
    test_case_number = 1

    print("=" * 80)
    print("WEIGHTED RANDOM CITY SELECTION - TEST SUITE")
    print("=" * 80)

    # ========================================================================
    # TEST 1: Basic Example from Problem Statement
    # ========================================================================
    print(f"\nTest {test_case_number}: Basic Example from Problem")
    print("-" * 80)

    # Increment test counter
    total_tests += 1
    test_case_number += 1

    try:
        # Create test data matching the problem example
        # Purpose: Test with the exact example provided in problem statement
        test_data_1 = {'NY': 7000000, 'SF': 5000000, 'LA': 8000000}

        # Run the function multiple times to verify probabilistic distribution
        # Purpose: Check that results follow expected probability distribution
        results_1 = [weighted_random_city(test_data_1) for _ in range(10000)]

        # Count occurrences of each city
        # Purpose: Verify probabilities are approximately correct
        ny_count = results_1.count('NY')
        sf_count = results_1.count('SF')
        la_count = results_1.count('LA')

        # Calculate observed probabilities
        # Purpose: Compare with expected probabilities
        # Expected: NY=0.35, SF=0.25, LA=0.40
        ny_prob = ny_count / len(results_1)
        sf_prob = sf_count / len(results_1)
        la_prob = la_count / len(results_1)

        # Define acceptable margin of error for probability
        # Purpose: Account for randomness while ensuring distribution is correct
        # 5% tolerance is reasonable for random sampling
        tolerance = 0.05

        # Verify each city's probability is close to expected
        # Purpose: Ensure weighted selection is working correctly
        ny_valid = abs(ny_prob - 0.35) < tolerance
        sf_valid = abs(sf_prob - 0.25) < tolerance
        la_valid = abs(la_prob - 0.40) < tolerance

        # All probabilities must be valid for test to pass
        # Purpose: Comprehensive check of the algorithm
        if ny_valid and sf_valid and la_valid:
            print(f"✓ PASS: Probabilistic Distribution Verified")
            print(f"  NY: {ny_prob:.2%} (expected ~35%)")
            print(f"  SF: {sf_prob:.2%} (expected ~25%)")
            print(f"  LA: {la_prob:.2%} (expected ~40%)")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Probabilities outside acceptable range")
            print(f"  NY: {ny_prob:.2%} (expected ~35%)")
            print(f"  SF: {sf_prob:.2%} (expected ~25%)")
            print(f"  LA: {la_prob:.2%} (expected ~40%)")

    except Exception as e:
        # Catch any errors that occur during test
        # Purpose: Report what went wrong
        print(f"✗ FAIL: Exception occurred - {str(e)}")

    # ========================================================================
    # TEST 2: Single City (Edge Case)
    # ========================================================================
    print(f"\nTest {test_case_number}: Single City (Edge Case)")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create test with only one city
        # Purpose: Test edge case where only one choice exists
        test_data_2 = {'Tokyo': 14000000}

        # Run multiple times
        # Purpose: Verify only 'Tokyo' is ever returned
        results_2 = [weighted_random_city(test_data_2) for _ in range(100)]

        # Check if all results are the single city
        # Purpose: With one city, 100% of results should be that city
        if all(city == 'Tokyo' for city in results_2):
            print(f"✓ PASS: Single city always returns correct city")
            print(f"  Result: {results_2[0]} (100% of the time)")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Single city test failed")

    except Exception as e:
        print(f"✗ FAIL: Exception occurred - {str(e)}")

    # ========================================================================
    # TEST 3: Two Cities with Equal Population
    # ========================================================================
    print(f"\nTest {test_case_number}: Equal Population Cities")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create test with equal populations
        # Purpose: Verify 50-50 probability distribution
        test_data_3 = {'CityA': 5000000, 'CityB': 5000000}

        # Run many times to check distribution
        # Purpose: With equal populations, each city should appear ~50% of time
        results_3 = [weighted_random_city(test_data_3) for _ in range(10000)]

        # Count occurrences
        cityA_count = results_3.count('CityA')
        cityB_count = results_3.count('CityB')

        # Calculate probabilities
        cityA_prob = cityA_count / len(results_3)
        cityB_prob = cityB_count / len(results_3)

        # Check if probabilities are close to 50%
        # Purpose: Equal populations should produce equal probabilities
        if abs(cityA_prob - 0.5) < 0.05 and abs(cityB_prob - 0.5) < 0.05:
            print(f"✓ PASS: Equal population distribution verified")
            print(f"  CityA: {cityA_prob:.2%} (expected ~50%)")
            print(f"  CityB: {cityB_prob:.2%} (expected ~50%)")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Distribution not equal")
            print(f"  CityA: {cityA_prob:.2%}")
            print(f"  CityB: {cityB_prob:.2%}")

    except Exception as e:
        print(f"✗ FAIL: Exception occurred - {str(e)}")

    # ========================================================================
    # TEST 4: Very Skewed Distribution
    # ========================================================================
    print(f"\nTest {test_case_number}: Highly Skewed Distribution")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create test with one dominant city
        # Purpose: Verify algorithm handles extreme probability ratios
        test_data_4 = {'BigCity': 9900000, 'SmallCity': 100000}

        # Run many times
        # Purpose: BigCity should appear ~99% of time
        results_4 = [weighted_random_city(test_data_4) for _ in range(10000)]

        # Count occurrences
        big_count = results_4.count('BigCity')
        small_count = results_4.count('SmallCity')

        # Calculate probabilities
        big_prob = big_count / len(results_4)
        small_prob = small_count / len(results_4)

        # Check if probabilities match expected skew
        # Purpose: With 99:1 ratio, results should show that ratio
        if abs(big_prob - 0.99) < 0.05 and abs(small_prob - 0.01) < 0.05:
            print(f"✓ PASS: Skewed distribution verified")
            print(f"  BigCity: {big_prob:.2%} (expected ~99%)")
            print(f"  SmallCity: {small_prob:.2%} (expected ~1%)")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Skewed distribution incorrect")
            print(f"  BigCity: {big_prob:.2%}")
            print(f"  SmallCity: {small_prob:.2%}")

    except Exception as e:
        print(f"✗ FAIL: Exception occurred - {str(e)}")

    # ========================================================================
    # TEST 5: Empty Dictionary (Error Handling)
    # ========================================================================
    print(f"\nTest {test_case_number}: Empty Dictionary Error Handling")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create empty dictionary
        # Purpose: Test error handling for invalid input
        test_data_5 = {}

        # Attempt to call function with empty dictionary
        # Purpose: Should raise ValueError
        result = weighted_random_city(test_data_5)

        # If we reach here, test failed (no exception raised)
        print(f"✗ FAIL: Should have raised ValueError for empty dictionary")

    except ValueError as e:
        # Expected behavior: ValueError should be raised
        print(f"✓ PASS: Correctly raised ValueError")
        print(f"  Error message: {str(e)}")
        passed_tests += 1

    except Exception as e:
        # Unexpected exception type
        print(f"✗ FAIL: Wrong exception type - {type(e).__name__}: {str(e)}")

    # ========================================================================
    # TEST 6: Many Cities (Scalability Test)
    # ========================================================================
    print(f"\nTest {test_case_number}: Many Cities (Scalability)")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create dictionary with 1000 cities
        # Purpose: Test performance and correctness with large dataset
        # Logic: Create cities with incrementally increasing populations
        test_data_6 = {f'City_{i}': (i + 1) * 100000 for i in range(1000)}

        # Run the function multiple times
        # Purpose: Ensure it handles 1000 cities without errors
        results_6 = [weighted_random_city(test_data_6) for _ in range(1000)]

        # Verify we get results from the dictionary
        # Purpose: Confirm all results are valid cities
        all_valid = all(city in test_data_6 for city in results_6)

        # Check that we get variety in results (not always same city)
        # Purpose: Confirm randomness is working with many cities
        unique_cities = len(set(results_6))

        if all_valid and unique_cities > 1:
            print(f"✓ PASS: Handled 1000 cities correctly")
            print(f"  All results valid: {all_valid}")
            print(f"  Unique cities selected: {unique_cities} out of 1000")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Issue with large dataset")
            print(f"  All results valid: {all_valid}")
            print(f"  Unique cities: {unique_cities}")

    except Exception as e:
        print(f"✗ FAIL: Exception with large dataset - {str(e)}")

    # ========================================================================
    # TEST 7: Large Population Numbers (Big Data)
    # ========================================================================
    print(f"\nTest {test_case_number}: Large Population Numbers")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create test with very large population numbers
        # Purpose: Ensure algorithm handles large integers without overflow
        # Note: Python handles arbitrary precision integers naturally
        test_data_7 = {
            'Country1': 1_000_000_000_000,  # 1 trillion
            'Country2': 2_000_000_000_000,  # 2 trillion
            'Country3': 7_000_000_000_000  # 7 trillion
        }

        # Run multiple times
        # Purpose: Verify probability calculation works with huge numbers
        results_7 = [weighted_random_city(test_data_7) for _ in range(10000)]

        # Count and calculate probabilities
        c1_count = results_7.count('Country1')
        c2_count = results_7.count('Country2')
        c3_count = results_7.count('Country3')

        c1_prob = c1_count / len(results_7)
        c2_prob = c2_count / len(results_7)
        c3_prob = c3_count / len(results_7)

        # Expected: 10%, 20%, 70% (1:2:7 ratio)
        # Purpose: Verify correct probability distribution with large numbers
        if (abs(c1_prob - 0.10) < 0.05 and
                abs(c2_prob - 0.20) < 0.05 and
                abs(c3_prob - 0.70) < 0.05):
            print(f"✓ PASS: Large numbers handled correctly")
            print(f"  Country1: {c1_prob:.2%} (expected ~10%)")
            print(f"  Country2: {c2_prob:.2%} (expected ~20%)")
            print(f"  Country3: {c3_prob:.2%} (expected ~70%)")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Incorrect distribution with large numbers")
            print(f"  Country1: {c1_prob:.2%}")
            print(f"  Country2: {c2_prob:.2%}")
            print(f"  Country3: {c3_prob:.2%}")

    except Exception as e:
        print(f"✗ FAIL: Exception occurred - {str(e)}")

    # ========================================================================
    # TEST 8: Fractional Populations (Edge Case)
    # ========================================================================
    print(f"\nTest {test_case_number}: Fractional Populations")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create test with float populations
        # Purpose: Verify algorithm works with decimal population values
        test_data_8 = {'CityX': 3.5, 'CityY': 6.5}

        # Run multiple times
        # Purpose: Check 35%-65% distribution
        results_8 = [weighted_random_city(test_data_8) for _ in range(10000)]

        # Count and calculate
        cityx_prob = results_8.count('CityX') / len(results_8)
        cityy_prob = results_8.count('CityY') / len(results_8)

        # Expected: 35% and 65%
        if abs(cityx_prob - 0.35) < 0.05 and abs(cityy_prob - 0.65) < 0.05:
            print(f"✓ PASS: Fractional populations handled correctly")
            print(f"  CityX: {cityx_prob:.2%} (expected ~35%)")
            print(f"  CityY: {cityy_prob:.2%} (expected ~65%)")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Fractional population test failed")
            print(f"  CityX: {cityx_prob:.2%}")
            print(f"  CityY: {cityy_prob:.2%}")

    except Exception as e:
        print(f"✗ FAIL: Exception occurred - {str(e)}")

    # ========================================================================
    # TEST 9: Cities with Zero Population (Edge Case)
    # ========================================================================
    print(f"\nTest {test_case_number}: City with Zero Population")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create test with one zero-population city
        # Purpose: Verify city with 0 population is never selected
        test_data_9 = {'ActiveCity': 10000000, 'GhostCity': 0}

        # Run multiple times
        # Purpose: Should never select GhostCity (0 probability)
        results_9 = [weighted_random_city(test_data_9) for _ in range(1000)]

        # Check if GhostCity was ever selected
        # Purpose: With 0 population, it should never appear
        ghost_count = results_9.count('GhostCity')

        if ghost_count == 0 and all(city == 'ActiveCity' for city in results_9):
            print(f"✓ PASS: Zero population city never selected")
            print(f"  ActiveCity selected: 100% of the time")
            print(f"  GhostCity selected: 0% of the time")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Zero population city was selected")
            print(f"  GhostCity count: {ghost_count}")

    except Exception as e:
        print(f"✗ FAIL: Exception occurred - {str(e)}")

    # ========================================================================
    # TEST 10: Multiple Large Scale Test
    # ========================================================================
    print(f"\nTest {test_case_number}: Multiple Runs with Consistent Probabilities")
    print("-" * 80)

    total_tests += 1
    test_case_number += 1

    try:
        # Create test data
        # Purpose: Test consistency across multiple runs
        test_data_10 = {
            'MetroA': 4000000,
            'MetroB': 3000000,
            'MetroC': 2000000,
            'MetroD': 1000000
        }

        # Run 5 separate batches of 10000 samples each
        # Purpose: Verify consistency and stability of the algorithm
        batch_results = []
        expected_probs = {
            'MetroA': 0.40,
            'MetroB': 0.30,
            'MetroC': 0.20,
            'MetroD': 0.10
        }

        # Run multiple independent batches
        for batch in range(5):
            # Generate samples for this batch
            batch_samples = [weighted_random_city(test_data_10) for _ in range(10000)]

            # Calculate probabilities for this batch
            batch_probs = {
                city: batch_samples.count(city) / len(batch_samples)
                for city in test_data_10.keys()
            }
            batch_results.append(batch_probs)

        # Verify all batches are consistent
        # Purpose: Ensure algorithm is stable and reliable
        all_consistent = True
        for city in test_data_10.keys():
            # Get all probabilities for this city across batches
            city_probs = [batch[city] for batch in batch_results]

            # Check if all are close to expected
            # Purpose: Should be within tolerance in all batches
            if not all(abs(prob - expected_probs[city]) < 0.05 for prob in city_probs):
                all_consistent = False
                break

        if all_consistent:
            print(f"✓ PASS: Consistent probabilities across 5 batches")
            print(f"  Each batch: 10,000 samples")
            print(f"  Expected probabilities maintained across all runs")
            for city in test_data_10.keys():
                avg_prob = sum(batch[city] for batch in batch_results) / 5
                print(f"    {city}: {avg_prob:.2%} (expected {expected_probs[city]:.0%})")
            passed_tests += 1
        else:
            print(f"✗ FAIL: Inconsistent results across batches")

    except Exception as e:
        print(f"✗ FAIL: Exception occurred - {str(e)}")

    # ========================================================================
    # SUMMARY REPORT
    # ========================================================================
    print("\n" + "=" * 80)
    print("TEST SUMMARY REPORT")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✓")
    print(f"Failed: {total_tests - passed_tests} ✗")
    print(f"Success Rate: {(passed_tests / total_tests) * 100:.1f}%")
    print("=" * 80)

    # Return whether all tests passed
    # Purpose: Useful for automated testing
    return passed_tests == total_tests


# ============================================================================
# COMPLEXITY ANALYSIS - DETAILED EXPLANATION
# ============================================================================

"""
TIME COMPLEXITY ANALYSIS:
==========================

1. PREPROCESSING PHASE - Building Cumulative Probabilities:
   - Converting dictionary keys to list: O(n) where n = number of cities
   - Converting dictionary values to list: O(n)
   - Calculating sum of populations: O(n)
   - Building cumulative probabilities array: O(n)
     - Loop runs n times
     - Each iteration does constant time operation (addition, append)

   Total Preprocessing: O(n) + O(n) + O(n) + O(n) = O(n)

2. SELECTION PHASE - Finding Random City:
   - Generating random number: O(1) constant time
   - Binary search using bisect_right: O(log n)
     - Cumulative array has n elements
     - Binary search eliminates half each iteration
     - Maximum iterations = log₂(n)
   - Index lookup and return: O(1)

   Total Selection: O(log n)

OVERALL TIME COMPLEXITY:
- Single call: O(n) preprocessing + O(log n) selection = O(n)
  Note: Preprocessing happens once per call
- If selecting m times with same map: O(n + m*log n)
  Note: For large m, this becomes O(m*log n) after initial O(n)
- Typical scenario (single selection): O(n)

WHY NOT SLOWER?
- Simple sum loop: O(n) is unavoidable (must check all cities)
- Binary search: O(log n) is faster than linear O(n) lookup
- With 1000 cities: O(log 1000) = 10 comparisons vs 500 average linear searches

---

SPACE COMPLEXITY ANALYSIS:
============================

1. DATA STRUCTURES CREATED:
   - cities list: O(n) space
     - Stores n city name strings
     - Each string takes variable space, but total is O(n)

   - populations list: O(n) space
     - Stores n numerical values

   - cumulative_probabilities list: O(n) space
     - Stores n cumulative probability values (floats)

2. VARIABLES (CONSTANT SPACE):
   - total_population: O(1) single number
   - cumulative_sum: O(1) single number
   - random_value: O(1) single number
   - city_index: O(1) single number

TOTAL SPACE COMPLEXITY: O(n) + O(n) + O(n) + O(1) = O(n)

BREAKDOWN:
- We need to store cities: unavoidable, requires O(n)
- We need to store populations: unavoidable, requires O(n)
- We create cumulative array: necessary for efficient selection, requires O(n)
- Total: 3 arrays of size n = O(3n) = O(n)

WHY THIS SPACE USAGE?
- We must store all cities for the output: O(n) is necessary
- We could avoid storing separate populations/cumulative lists
  but keeping them makes the code clear and only adds constant factor

SPACE OPTIMIZATION:
- Could save space by not storing populations separately
- Could merge cities and cumulative probabilities
- Would reduce from O(3n) to O(2n) but O(n) overall stays same
- Not worth the code complexity trade-off

---

ALGORITHM COMPARISON:
=====================

Method 1: BINARY SEARCH ON CUMULATIVE (Our Solution)
- Time: O(n) preprocessing + O(log n) per selection
- Space: O(n)
- Best for: Multiple selections, large datasets
- Example: 1000 cities, 100 selections = 1000 + 100*10 = 2000 operations

Method 2: LINEAR SEARCH (Simple Alternative)
- Time: O(n) preprocessing + O(n) per selection
- Space: O(n)
- Best for: Small number of cities (< 100)
- Example: 1000 cities, 100 selections = 1000 + 100*500 = 51,000 operations

Method 3: REJECTION SAMPLING (No Preprocessing)
- Time: O(1) to O(n) per selection (average O(n/max_ratio))
- Space: O(n)
- Best for: When distribution is very skewed
- Note: Can be slow if most rejections occur

Performance Comparison (1000 cities, 1000 selections):
- Binary Search: 1000 + 10,000 = 11,000 operations
- Linear Search: 1000 + 500,000 = 501,000 operations
- Binary Search is 45x FASTER!

---

WHY BINARY SEARCH IS OPTIMAL:
===============================

The cumulative probability array is sorted (monotonically increasing).
Example: [0.35, 0.60, 1.00] - always increasing

Binary search works because:
1. Array is sorted: ✓ (probabilities are cumulative)
2. We search for value: ✓ (random number between 0 and 1)
3. Find position: ✓ (bisect_right gives insertion point)

Binary search is optimal because:
- No sorting needed: already sorted by construction
- Each comparison eliminates half of remaining elements
- Maximum iterations: log₂(n)
- No data structure can do better than O(log n) for searching sorted data

---

SCALABILITY ANALYSIS:

Cities | Preprocessing | Per Selection | 1000 Selections
-------|---------------|---------------|-----------------
10     | 10 ops        | ~3 ops        | 3,010 ops
100    | 100 ops       | ~7 ops        | 7,100 ops
1,000  | 1,000 ops     | ~10 ops       | 11,000 ops
10,000 | 10,000 ops    | ~14 ops       | 24,000 ops
100,000| 100,000 ops   | ~17 ops       | 117,000 ops
1,000,000| 1M ops      | ~20 ops       | 1,020,000 ops

Note: Logarithmic growth means adding 0 cities increases per-selection time minimally
- 10 to 1,000 cities: 3 to 10 ops (3.3x increase for 100x more cities)
- 1,000 to 1M cities: 10 to 20 ops (2x increase for 1000x more cities)

This is EXCELLENT SCALABILITY!
"""

# ============================================================================
# ENTRY POINT - RUN ALL TESTS
# ============================================================================

if __name__ == "__main__":
    # Call the testing function
    # Purpose: Execute all test cases when script runs
    # Logic: Calls run_tests() which returns True if all pass, False otherwise
    success = run_tests()

    # Print final status
    # Purpose: Give clear indication of overall test result
    print("\n" + "=" * 80)
    if success:
        # All tests passed
        print("✓ ALL TESTS PASSED - SOLUTION IS CORRECT")
    else:
        # Some tests failed
        print("✗ SOME TESTS FAILED - REVIEW ERRORS ABOVE")
    print("=" * 80)