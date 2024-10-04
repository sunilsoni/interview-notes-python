from typing import List

import requests


class CountryInfoApp:
    BASE_URL = "https://restcountries.com/v3.1/all"

    @staticmethod
    def get_country_info(fields: List[str]) -> List[dict]:
        try:
            response = requests.get(CountryInfoApp.BASE_URL)
            response.raise_for_status()
            countries = response.json()

            filtered_countries = []
            for country in countries:
                filtered_country = {}
                for field in fields:
                    if field in country:
                        filtered_country[field] = country[field]
                filtered_countries.append(filtered_country)

            return filtered_countries
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []


def main():
    app = CountryInfoApp()

    # Test case 1: Basic fields
    fields1 = ["name", "capital", "population"]
    result1 = app.get_country_info(fields1)
    print("Test case 1 result:", result1[:2])  # Print first two countries

    # Test case 2: More complex fields
    fields2 = ["name", "languages", "currencies"]
    result2 = app.get_country_info(fields2)
    print("Test case 2 result:", result2[:2])  # Print first two countries

    # Test case 3: Invalid field
    fields3 = ["name", "invalid_field"]
    result3 = app.get_country_info(fields3)
    print("Test case 3 result:", result3[:2])  # Print first two countries


if __name__ == "__main__":
    main()
