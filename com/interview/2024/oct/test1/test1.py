import json


# Function to sum up numbers from a specific field in a JSON string
def sum_numbers(json_str, field_name):
    # Parse the JSON string into a Python list of dictionaries
    data = json.loads(json_str)
    total_sum = 0

    # Iterate over each item in the list
    for item in data:
        # Check if the field exists in the item and if its value is a number (int or float)
        if field_name in item and isinstance(item[field_name], (int, float)):
            # Add the value to the total sum
            total_sum += item[field_name]

    # Return the total sum of the field values
    return total_sum


# Example usage
json_str = '[{"name": "item1", "value": 10}, {"name": "item2", "value": 20}, {"name": "item3", "value": 30}]'
field_name = "value"

# Call the function and print the result
result = sum_numbers(json_str, field_name)
print(f"The sum of '{field_name}' fields is: {result}")
