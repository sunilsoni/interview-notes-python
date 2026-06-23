import math
import os
import random
import re
import sys
import requests
import json


def mostSuccessfulDomesticClub(league, weight):
    # Set the base API endpoint URL provided in the instructions
    base_url = "https://jsonmock.hackerrank.com/api/football_teams"

    # Start the maximum score at negative infinity so any real score will beat it
    max_score = -float('inf')

    # Create an empty string to hold the name of the winning club
    best_club = ""

    # Set our starting page number to 1
    current_page = 1

    # We will set this to the real total pages after our first API call
    total_pages = 1

    # Loop continuously as long as the current page is less than or equal to total pages
    while current_page <= total_pages:

        # Setup the parameters for the API request (handles spaces in league names safely)
        params = {
            'league': league,
            'page': current_page
        }

        # Make the HTTP GET request to the API and parse the response into a JSON dictionary
        response = requests.get(base_url, params=params).json()

        # On the very first loop, update our total_pages variable from the API's metadata
        if current_page == 1:
            total_pages = response['total_pages']

        # Extract the list of football clubs from the 'data' array in the JSON
        teams_data = response['data']

        # Iterate through every single club found on the current page
        for club in teams_data:

            # Extract the club's name
            name = club['name']

            # Extract the count of total silverware won
            silverware = club['total_silverware_count']

            # Extract the number of Champions League titles won
            champions_league = club['number_of_champions_league_won']

            # Extract the count of top-three finishes
            top_three = club['league_top_three_finishes']

            # Calculate the success points using the exact formula provided
            current_score = silverware - champions_league + (weight * top_three)

            # Check if this club's score is strictly greater than our running maximum
            if current_score > max_score:
                # If it is, update the maximum score to this new high score
                max_score = current_score

                # And record this club's name as the current leader
                best_club = name

        # After checking all clubs on this page, increment the page counter to fetch the next page
        current_page += 1

    # Once all pages are processed and the loop finishes, return the overall winner
    return best_club


def run_tests():
    print("--- Starting Tests ---")

    # Define our test cases based on the problem description
    test_cases = [
        {
            "name": "Sample Case 0",
            "league": "English Premier League (EPL)",
            "weight": 0.37,
            "expected": "Manchester United FC"
        },
        {
            "name": "Sample Case 1",
            "league": "EFL League One",
            "weight": 0.87,
            "expected": "Bolton Wanderers"
        },
        {
            "name": "Edge Case: Zero Weight",
            "league": "English Premier League (EPL)",
            "weight": 0.0,
            "expected": "Manchester United FC"  # Usually still holds due to sheer silverware volume
        }
    ]

    # Loop through each test case
    for idx, tc in enumerate(test_cases):
        try:
            # Call our function with the test case inputs
            result = mostSuccessfulDomesticClub(tc["league"], tc["weight"])

            # Compare the actual result with what we expect to see
            if result == tc["expected"]:
                print(f"[PASS] Test {idx}: {tc['name']}")
            else:
                print(f"[FAIL] Test {idx}: {tc['name']} | Expected '{tc['expected']}', but got '{result}'")

        except Exception as e:
            # Catch any network or code errors safely
            print(f"[ERROR] Test {idx}: {tc['name']} crashed with error: {str(e)}")

    print("--- Testing Complete ---")


# Standard Python idiom to run the tests when the script is executed directly
if __name__ == '__main__':
    run_tests()