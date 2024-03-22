import requests


# Function to get the complete phone number with country code using the REST API
def get_phone_numbers(country, phone_number):
    # Replace spaces with '%20' for URL encoding
    country = country.replace(' ', '%20')

    # API endpoint with the country query
    api_url = f"https://jsonmock.hackerrank.com/api/countries?name={country}"

    # Make the GET request to the API
    response = requests.get(api_url)
    # Check if the request was successful
    if response.status_code != 200:
        return "-1"

    # Parse the JSON response
    data = response.json()

    # If there is no data or the data array is empty, return '-1'
    if not data or not data['data']:
        return "-1"

    # If there are multiple calling codes, use the one at the highest index
    calling_code = data['data'][0]['callingCodes'][-1]

    # Format and return the complete phone number
    return f"+{calling_code} {phone_number}"


# Example usage
# Since this is a coding challenge and the actual endpoint may not exist,
# this code won't run here as it is for demonstration purposes.
# Replace 'Afghanistan' and the phone number with actual values for testing.
print(get_phone_numbers('Afghanistan', '765355443'))
# Sample calls (uncomment the one you want to test)
print(get_phone_numbers("Afghanistan", "765355443"))
print(get_phone_numbers("Puerto Rico", "564593986"))
print(get_phone_numbers("Oceania", "987574876"))
