from typing import List, Dict

import requests


class CountryInfoApp:
    BASE_URL = "https://restcountries.com/v3.1/all"

    @staticmethod
    def get_country_info() -> List[Dict]:
        try:
            response = requests.get(CountryInfoApp.BASE_URL)
            response.raise_for_status()
            countries = response.json()

            filtered_countries = []
            for country in countries:
                filtered_country = {
                    "name": country["name"]["common"],
                    "flag": country["flags"]["png"] if "flags" in country and "png" in country["flags"] else "",
                    "capital": country["capital"][0] if "capital" in country and country["capital"] else "N/A",
                    "currency": next(iter(country["currencies"].values()))["name"] if "currencies" in country else "N/A"
                }
                filtered_countries.append(filtered_country)

            return filtered_countries
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return []


def main():
    app = CountryInfoApp()
    result = app.get_country_info()

    # Print the first 5 countries as a sample
    for country in result[:5]:
        print(country)


if __name__ == "__main__":
    main()
