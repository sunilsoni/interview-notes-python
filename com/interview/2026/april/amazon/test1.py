# The given data store containing all apps, their arguments, and their instances.
data = [
    {
        "name": "app1",
        "argument": "-Darg1=arg1 -Xmx4G -Xms1024M",
        "instances": [
            {
                "host": "host1.example.com",
                "port": 5000,
                "argument": "-Xmx2G -Xms1G -Darg1=arg1override"
            },
            {
                "host": "host2.example.com",
                "port": 5000,
                "argument": ""
            }
        ]
    },
    {
        "name": "app2",
        "argument": "-Darg1=arg2 -Xmx1G -Xms512M",
        "instances": [
            {
                "host": "host1.example.com",
                "port": 5001,
                "argument": "-Xmx10G"
            }
        ]
    },
    {
        "name": "app3",
        "argument": "-Darg1=arg2 -Xmx2G -Xms2G",
        "instances": [
            {
                "host": "host2.example.com",
                "port": 5001,
                "argument": ""
            }
        ]
    }
]

# We create two global dictionaries to act as instant lookup tables for large data.
app_lookup = {}
instance_lookup = {}


# This function runs once at the start to populate our lookup tables.
def build_lookup_tables():
    # Loop through every single app dictionary inside our main data list.
    for app in data:
        # Save the app dictionary into our lookup table using the app's name as the key.
        app_lookup[app['name']] = app

        # We use .get() here safely in case an app somehow has no 'instances' key.
        for instance in app.get('instances', []):
            # We create a unique key using a tuple of (host, port) since that combination is unique.
            key = (instance['host'], instance['port'])

            # We save BOTH the instance data AND a reference to the parent app.
            # We need the parent app later so we know where to get fallback arguments from.
            instance_lookup[key] = {
                'instance_data': instance,
                'parent_app': app
            }


# Helper function to extract the Xmx and Xms values from a string of arguments.
def parse_memory_flags(arg_string):
    # We create a fresh dictionary to store the extracted memory values.
    memory_values = {}

    # If the argument string is empty or None, we just return the empty dictionary.
    if not arg_string:
        return memory_values

    # We split the string by spaces. Example: "-Xmx1G -Xms512M" becomes ["-Xmx1G", "-Xms512M"]
    parts = arg_string.split()

    # We loop through every part of the split string.
    for part in parts:
        # Check if this specific part starts with the maximum memory flag.
        if part.startswith('-Xmx'):
            # If it does, we slice the string from index 4 to the end to skip "-Xmx" and grab the value (e.g., "1G").
            memory_values['xmx'] = part[4:]

        # Check if this specific part starts with the minimum memory flag.
        elif part.startswith('-Xms'):
            # Slicing from index 4 skips "-Xms" and gives us just the value (e.g., "512M").
            memory_values['xms'] = part[4:]

    # Return the dictionary containing whatever flags we managed to find.
    return memory_values


# Function 1: Get the app dictionary by its name.
def get_app(app_name: str) -> dict:
    # We ask our lookup table for the app. If it doesn't exist, we return an empty dictionary '{}'.
    return app_lookup.get(app_name, {})


# Function 2: Get the instance dictionary by its host and port.
def get_instance(host: str, port: int) -> dict:
    # We build the lookup key tuple using the provided host and port.
    key = (host, port)

    # We look up our saved data (which includes both the instance and the parent app).
    mapping = instance_lookup.get(key)

    # If we found the mapping, we return just the 'instance_data' portion.
    if mapping:
        return mapping['instance_data']

    # If the mapping was not found in our table, we return an empty dictionary.
    return {}


# Function 3: Get the final resolved memory usage for an instance.
def get_memory_usage(host: str, port: int) -> dict:
    # We set up our default return format with zeros as fallbacks.
    result = {'xmx': 0, 'xms': 0}

    # We build the unique key tuple to search for the instance.
    key = (host, port)

    # We search the lookup table for the instance and its parent app info.
    mapping = instance_lookup.get(key)

    # If the instance doesn't exist at all, we just return the default 0 values.
    if not mapping:
        return result

    # We extract the specific instance dictionary from our mapping.
    instance = mapping['instance_data']

    # We extract the parent app dictionary from our mapping so we can use its defaults.
    parent_app = mapping['parent_app']

    # We parse the parent app's argument string to find its base memory flags.
    # We use .get('argument', '') so if 'argument' is missing, it safely passes an empty string.
    app_memory = parse_memory_flags(parent_app.get('argument', ''))

    # We parse the instance's argument string to find its specific override memory flags.
    instance_memory = parse_memory_flags(instance.get('argument', ''))

    # Now we resolve the XMX (max memory) value.
    # Logic: Try to get 'xmx' from the instance. If it's not there, try to get it from the app.
    # If neither has it, fall back to our default 0.
    result['xmx'] = instance_memory.get('xmx', app_memory.get('xmx', 0))

    # We do the exact same resolution logic for the XMS (min memory) value.
    result['xms'] = instance_memory.get('xms', app_memory.get('xms', 0))

    # Finally, we return the fully resolved memory settings.
    return result


# A simple helper function to run tests and clearly print PASS or FAIL.
def run_test(test_name, actual_result, expected_result):
    # If the actual output exactly matches what we expect, the test passes.
    if actual_result == expected_result:
        print(f"[PASS] {test_name}")
    # If they don't match, the test fails, and we print out the difference for debugging.
    else:
        print(f"[FAIL] {test_name}")
        print(f"       Expected: {expected_result}")
        print(f"       Got:      {actual_result}")


# Our main function to execute the setup and run all tests.
def main():
    # First, we MUST call this to populate our dictionaries, or nothing will work!
    build_lookup_tables()

    print("--- Running Tests ---")

    # Test 1: Testing get_app with an existing app.
    # We expect to get the exact dictionary for "app2" from the global data.
    run_test(
        "get_app('app2')",
        get_app('app2'),
        data[1]
    )

    # Test 2: Testing get_instance with an existing instance.
    # We expect to get the first instance from "app1".
    run_test(
        "get_instance('host1.example.com', 5000)",
        get_instance('host1.example.com', 5000),
        data[0]['instances'][0]
    )

    # Test 3: Testing get_memory_usage - Partial Override Scenario (From Interview Transcript)
    # The app has -Xmx1G and -Xms512M. The instance ONLY overrides -Xmx to 10G.
    # We expect XMX to be 10G (override) and XMS to be 512M (fallback).
    run_test(
        "get_memory_usage('host1.example.com', 5001) - Partial Override",
        get_memory_usage('host1.example.com', 5001),
        {'xmx': '10G', 'xms': '512M'}
    )

    # Test 4: Testing get_memory_usage - Full Override Scenario
    # App has 4G/1024M. Instance has 2G/1G.
    # We expect the instance to completely override the app.
    run_test(
        "get_memory_usage('host1.example.com', 5000) - Full Override",
        get_memory_usage('host1.example.com', 5000),
        {'xmx': '2G', 'xms': '1G'}
    )

    # Test 5: Testing get_memory_usage - No Override Scenario
    # App has 2G/2G. Instance has an empty argument string "".
    # We expect it to rely entirely on the app's arguments.
    run_test(
        "get_memory_usage('host2.example.com', 5001) - No Override",
        get_memory_usage('host2.example.com', 5001),
        {'xmx': '2G', 'xms': '2G'}
    )

    # Test 6: Testing edge cases (Missing data)
    # Looking for a host/port that does not exist in our data at all.
    # We expect our default empty states.
    run_test("Edge Case - Fake App", get_app('fake_app'), {})
    run_test("Edge Case - Fake Instance", get_instance('fake.com', 9999), {})
    run_test("Edge Case - Fake Memory", get_memory_usage('fake.com', 9999), {'xmx': 0, 'xms': 0})


# Standard Python boilerplate to ensure main() only runs if this script is executed directly.
if __name__ == '__main__':
    main()