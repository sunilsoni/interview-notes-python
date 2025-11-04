import random  # Used to generate random numbers

def choose_city_weighted(cities):
    """
    Function to return a random city name based on population-weighted probability.
    :param cities: dict {city_name: population}
    :return: city name (string)
    """

    # Step 1: Calculate the total population across all cities.
    # This helps determine the overall range for random selection.
    total_population = sum(cities.values())

    # Step 2: Create cumulative population thresholds.
    # Example: For {"NY":7M, "SF":5M, "LA":8M}
    # cumulative = [("NY",7M),("SF",12M),("LA",20M)]
    cumulative = []
    cumulative_sum = 0
    for city, pop in cities.items():
        cumulative_sum += pop
        cumulative.append((city, cumulative_sum))  # store each city's upper limit

    # Step 3: Generate a random number between 0 and total_population
    r = random.randint(1, total_population)  # inclusive of both ends

    # Step 4: Find which city range this random number falls into
    for city, cum_pop in cumulative:
        if r <= cum_pop:
            return city  # Return the matching city name

    # Step 5: Fallback (should never reach here)
    return None
def main():
    # Test Case 1: Basic example from problem statement
    cities = {"NY": 7000000, "SF": 5000000, "LA": 8000000}

    print("Testing random weighted selection (small dataset):")
    results = {"NY": 0, "SF": 0, "LA": 0}

    # Run simulation many times to observe approximate probabilities
    trials = 100000
    for _ in range(trials):
        chosen = choose_city_weighted(cities)
        results[chosen] += 1

    # Display approximate probability distribution
    for city, count in results.items():
        print(f"{city}: {count/trials:.2%} probability (Expected: {cities[city]/sum(cities.values()):.2%})")

    # Large Data Test Case
    print("\nTesting large dataset (1 million cities with random populations)...")
    large_cities = {f"City_{i}": random.randint(1, 1000) for i in range(1, 1000001)}
    city_selected = choose_city_weighted(large_cities)
    print(f"Sample selection from large dataset: {city_selected}")

if __name__ == "__main__":
    main()
