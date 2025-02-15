# Pizza Pricing System

# 1. Problem Analysis:

# We need to build a system that calculates the price of a pizza based on its ingredients:
# - Base (e.g., thin, regular, cheesy crust) with associated prices.
# - Size (e.g., small, medium, large) with size multipliers.
# - 0 to N toppings with associated prices.

# The formula for calculating the price is:
# Price = (base price + sum of topping prices) * size multiplier

# Given examples:
# - Small thin crust cheese: ($8 + $2) * 0.75 = $7.50
# - Medium thin crust cheese: ($8 + $2) * 1.0 = $10.00

# Requirements:
# - Support different bases, sizes, and toppings.
# - Calculate the price using the provided formula.
# - Handle multiple test cases, including edge cases and large inputs.
# - Provide a simple main method for testing.

# 2. Solution Design:

# We will create classes to represent the components of a pizza:
# - Base: with types and corresponding prices.
# - Size: with types and corresponding multipliers.
# - Topping: with names and prices.

# A Pizza class will encapsulate these components and provide a method to calculate the price.

# This object-oriented approach allows for easy extension and maintenance.

# 3. Implementation:

class PizzaBase:
    base_prices = {
        'thin': 8.0,
        'regular': 7.0,
        # Additional bases can be added here
    }

    def __init__(self, base_type):
        if base_type not in self.base_prices:
            raise ValueError(f"Invalid base type: {base_type}")
        self.base_type = base_type
        self.price = self.base_prices[base_type]


class PizzaSize:
    size_multipliers = {
        'small': 0.75,
        'medium': 1.0,
        'large': 2.0,
        # Additional sizes can be added here
    }

    def __init__(self, size_type):
        if size_type not in self.size_multipliers:
            raise ValueError(f"Invalid size type: {size_type}")
        self.size_type = size_type
        self.multiplier = self.size_multipliers[size_type]


class Topping:
    topping_prices = {
        'cheese': 2.0,
        # Additional toppings can be added here
    }

    def __init__(self, topping_name):
        if topping_name not in self.topping_prices:
            raise ValueError(f"Invalid topping: {topping_name}")
        self.topping_name = topping_name
        self.price = self.topping_prices[topping_name]


class Pizza:
    def __init__(self, base, size, toppings=None):
        self.base = PizzaBase(base)
        self.size = PizzaSize(size)
        self.toppings = []
        if toppings:
            for topping_name in toppings:
                self.toppings.append(Topping(topping_name))

    def calculate_price(self):
        base_price = self.base.price
        toppings_price = sum(topping.price for topping in self.toppings)
        total_price = (base_price + toppings_price) * self.size.multiplier
        return round(total_price, 2)  # Rounded to 2 decimal places


# 4. Testing:

def main():
    # List to hold test cases
    test_cases = [
        {
            'description': 'Small thin crust cheese',
            'base': 'thin',
            'size': 'small',
            'toppings': ['cheese'],
            'expected_price': 7.50
        },
        {
            'description': 'Medium thin crust cheese',
            'base': 'thin',
            'size': 'medium',
            'toppings': ['cheese'],
            'expected_price': 10.00
        },
        {
            'description': 'Large regular crust with no toppings',
            'base': 'regular',
            'size': 'large',
            'toppings': [],
            'expected_price': 14.00  # ($7 + $0) * 2 = $14
        },
        {
            'description': 'Small regular crust with cheese',
            'base': 'regular',
            'size': 'small',
            'toppings': ['cheese'],
            'expected_price': 6.75  # ($7 + $2) * 0.75 = $6.75
        },
        {
            'description': 'Medium thin crust with multiple toppings',
            'base': 'thin',
            'size': 'medium',
            'toppings': ['cheese', 'cheese', 'cheese'],
            'expected_price': 14.00  # ($8 + $6) * 1.0 = $14.00
        },
        {
            'description': 'Edge case: Invalid base type',
            'base': 'stuffed',
            'size': 'medium',
            'toppings': ['cheese'],
            'expected_price': 'Error'
        },
        {
            'description': 'Edge case: No toppings',
            'base': 'thin',
            'size': 'small',
            'toppings': [],
            'expected_price': 6.00  # ($8 + $0) * 0.75 = $6.00
        },
        {
            'description': 'Edge case: Large number of toppings',
            'base': 'thin',
            'size': 'large',
            'toppings': ['cheese'] * 1000,
            'expected_price': (8 + 2 * 1000) * 2  # Heavy computation
        },
    ]

    passed_tests = 0
    for idx, test in enumerate(test_cases):
        try:
            pizza = Pizza(test['base'], test['size'], test['toppings'])
            price = pizza.calculate_price()
            expected_price = test['expected_price']
            if isinstance(expected_price, str) and expected_price == 'Error':
                print(f"Test {idx + 1} [{test['description']}]: FAIL (Expected an error, but got price {price})")
            elif abs(price - expected_price) < 0.01:  # Allowing minor floating point differences
                print(f"Test {idx + 1} [{test['description']}]: PASS")
                passed_tests += 1
            else:
                print(f"Test {idx + 1} [{test['description']}]: FAIL (Expected {expected_price}, got {price})")
        except ValueError as e:
            if test['expected_price'] == 'Error':
                print(f"Test {idx + 1} [{test['description']}]: PASS")
                passed_tests += 1
            else:
                print(f"Test {idx + 1} [{test['description']}]: FAIL (Unexpected error: {e})")
    print(f"{passed_tests} out of {len(test_cases)} tests passed.")


if __name__ == "__main__":
    main()
