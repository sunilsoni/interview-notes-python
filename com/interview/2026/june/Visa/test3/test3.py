# This helper checks the clubs from one API page.
def update_best_club(clubs, weight, best_name, best_points):

    # Visit every club present on the current API page.
    for club in clubs:

        # Read the total number of trophies won by the club.
        # "or 0" safely handles a missing or null value.
        total_silverware = int(
            club.get("total_silverware_count") or 0
        )

        # Read the number of Champions League trophies.
        champions_league_won = int(
            club.get("number_of_champions_league_won") or 0
        )

        # Read how many times the club finished in the top three.
        top_three_finishes = int(
            club.get("league_top_three_finishes") or 0
        )

        # Apply the success-points formula given in the question.
        success_points = (
            total_silverware
            - champions_league_won
            + weight * top_three_finishes
        )

        # Check whether this club has a better score.
        if success_points > best_points:

            # Save the new highest score.
            best_points = success_points

            # Save the name belonging to the new highest score.
            best_name = club.get("name", "")

    # Return the best club found so far.
    return best_name, best_points


def mostSuccessfulDomesticClub(league, weight):

    # Store the API endpoint without manually building query parameters.
    url = "https://jsonmock.hackerrank.com/api/football_teams"

    # Start reading from the first page.
    page = 1

    # Initially assume that at least page 1 must be requested.
    total_pages = 1

    # No club has been selected yet.
    best_name = ""

    # Start below every possible score.
    # Therefore, the first club will automatically become the current best.
    best_points = float("-inf")

    # Continue until every API page has been processed.
    while page <= total_pages:

        # Send the league and page as query parameters.
        # requests safely handles spaces and brackets in the league name.
        response = requests.get(
            url,
            params={
                "league": league,
                "page": page
            }
        )

        # Raise an error when the API returns an unsuccessful HTTP status.
        response.raise_for_status()

        # Convert the JSON response into a Python dictionary.
        result = response.json()

        # Read how many pages exist for this league.
        total_pages = int(result.get("total_pages", 0))

        # Read the list of clubs from the current page.
        clubs = result.get("data", [])

        # Compare the clubs from this page with the current winner.
        best_name, best_points = update_best_club(
            clubs,
            weight,
            best_name,
            best_points
        )

        # Move to the next API page.
        page += 1

    # Return only the winning club's name.
    return best_name

# This helper prints PASS or FAIL for one test case.
def run_test(test_name, clubs, weight, expected_name):

    # Run the same comparison logic used by the API solution.
    actual_name, actual_points = update_best_club(
        clubs,
        weight,
        "",
        float("-inf")
    )

    # Compare the actual club name with the expected name.
    passed = actual_name == expected_name

    # Select the text to print.
    status = "PASS" if passed else "FAIL"

    # Print all useful test information.
    print(
        f"{status}: {test_name} | "
        f"Expected = {expected_name} | "
        f"Actual = {actual_name} | "
        f"Points = {actual_points}"
    )

    # Return True or False for the final result.
    return passed


def main():

    # Assume all tests pass until one test fails.
    all_passed = True

    # Data shown in Sample Case 0.
    epl_clubs = [
        {
            "name": "Manchester United FC",
            "total_silverware_count": 66,
            "number_of_champions_league_won": 3,
            "league_top_three_finishes": 27
        },
        {
            "name": "Liverpool",
            "total_silverware_count": 48,
            "number_of_champions_league_won": 6,
            "league_top_three_finishes": 27
        }
    ]

    # Verify Sample Case 0.
    all_passed &= run_test(
        "Sample Case 0",
        epl_clubs,
        0.37,
        "Manchester United FC"
    )

    # Data shown in Sample Case 1.
    efl_clubs = [
        {
            "name": "Bolton Wanderers",
            "total_silverware_count": 7,
            "number_of_champions_league_won": 0,
            "league_top_three_finishes": 2
        },
        {
            "name": "Charlton Athletic",
            "total_silverware_count": 5,
            "number_of_champions_league_won": 0,
            "league_top_three_finishes": 2
        }
    ]

    # Verify Sample Case 1.
    all_passed &= run_test(
        "Sample Case 1",
        efl_clubs,
        0.87,
        "Bolton Wanderers"
    )

    # Test the Arsenal example from the question.
    arsenal_data = [
        {
            "name": "Arsenal FC",
            "total_silverware_count": 30,
            "number_of_champions_league_won": 0,
            "league_top_three_finishes": 18
        }
    ]

    # Arsenal's score should be 39.
    all_passed &= run_test(
        "Single club",
        arsenal_data,
        0.50,
        "Arsenal FC"
    )

    # Test null fields to confirm they are safely treated as zero.
    missing_values = [
        {
            "name": "Club A",
            "total_silverware_count": None,
            "number_of_champions_league_won": None,
            "league_top_three_finishes": None
        },
        {
            "name": "Club B",
            "total_silverware_count": 1,
            "number_of_champions_league_won": 0,
            "league_top_three_finishes": 0
        }
    ]

    # Club B has one point, while Club A has zero.
    all_passed &= run_test(
        "Null values",
        missing_values,
        0.50,
        "Club B"
    )

    # Generate 100,000 clubs without storing all of them in a list.
    large_data = (
        {
            "name": f"Club {number}",
            "total_silverware_count": number,
            "number_of_champions_league_won": 0,
            "league_top_three_finishes": 0
        }
        for number in range(100_000)
    )

    # Club 99999 has the highest score.
    all_passed &= run_test(
        "Large input",
        large_data,
        0.50,
        "Club 99999"
    )

    # Print the combined result.
    if all_passed:

        # Every test produced the expected result.
        print("\nAll calculation tests passed.")

    else:

        # At least one test produced an incorrect result.
        print("\nOne or more tests failed.")


# Run the tests only when this file is executed directly.
if __name__ == "__main__":

    # Start the local test program.
    main()