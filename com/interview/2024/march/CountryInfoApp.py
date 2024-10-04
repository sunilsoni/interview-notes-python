from typing import List, Dict, Any

import requests

BASE_URL = "https://restcountries.com/v3.1/all"


def get_country_info(fields: List[str]) -> List[Dict[str, Any]]:
    # Join the fields list into a comma-separated string
    fields_str = ",".join(fields)
    url = f"{BASE_URL}?fields={fields_str}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        countries = response.json()

        return [
            {
                field: extract_field_data(country, field)
                for field in fields
            }
            for country in countries
        ]

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def extract_field_data(country: Dict[str, Any], field: str) -> Any:
    if field == "name":
        return country["name"]["common"]
    elif field == "flags":
        return {
            "png": country["flags"]["png"],
            "alt": country["flags"].get("alt", "")
        }
    else:
        return country.get(field, "N/A")


# Example usage
if __name__ == "__main__":
    # Example 1: Get name and flags
    print("Example 1: Name and Flags")
    info = get_country_info(["name", "flags"])
    for country in info[:3]:  # Print first 3 countries
        print(country)
    print()

    # Example 2: Get name, capital, and population
    print("Example 2: Name, Capital, and Population")
    info = get_country_info(["name", "capital", "population"])
    for country in info[:3]:  # Print first 3 countries
        print(country)
    print()

    # Example 3: Get name, region, and languages
    print("Example 3: Name, Region, and Languages")
    info = get_country_info(["name", "region", "languages"])
    for country in info[:3]:  # Print first 3 countries
        print(country)
