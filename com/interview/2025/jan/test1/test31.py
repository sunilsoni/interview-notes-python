#!/usr/bin/env python3

class PizzaPriceCalculator:

    def __init__(self):
        # Price data can be extended or modified
        self.base_prices = {
            "thin": 8,
            "regular": 7
        }
        self.topping_prices = {
            "cheese": 2
        }
        self.size_multipliers = {
            "small": 0.75,
            "medium": 1.0,
            "large": 2.0
        }

    def calculate_price(self, base_type, size, toppings):
        """
        Calculates the price of a pizza.

        :param base_type: (str) e.g., "thin", "regular"
        :param size: (str) e.g., "small", "medium", "large"
        :param toppings: (list of str) e.g., ["cheese"]
        :return: (float) final pizza price
        """
        base_price = self.base_prices.get(base_type, 0)
        total_toppings_price = sum(self.topping_prices.get(t, 0) for t in toppings)
        multiplier = self.size_multipliers.get(size, 1.0)

        return (base_price + total_toppings_price) * multiplier


def main():
    # Create an instance of the calculator
    calculator = PizzaPriceCalculator()

    # Define test cases (input -> expected_output)
    # Format: (base_type, size, toppings_list, expected_price)
    test_cases = [
        ("thin", "small", ["cheese"], 7.50),  # as per example: (8 + 2) * 0.75 = 7.5
        ("thin", "medium", ["cheese"], 10.00),  # as per example: (8 + 2) * 1.0 = 10.0
        ("regular", "small", [], 5.25),  # (7 + 0) * 0.75 = 5.25
        ("regular", "large", ["cheese"], 18.0),  # (7 + 2) * 2 = 18.0
        # Add more variations
    ]

    # Test runner
    print("Running Tests...")
    for i, (base_type, size, toppings, expected) in enumerate(test_cases, start=1):
        price = calculator.calculate_price(base_type, size, toppings)
        # Check tolerance for floating point comparison
        if abs(price - expected) < 1e-9:
            result = "PASS"
        else:
            result = f"FAIL (expected {expected}, got {price:.2f})"
        print(f"Test Case {i}: {result}")

    # Additional test for large data inputs
    # E.g., a pizza with 10,000 "cheese" toppings (stress test)
    large_toppings = ["cheese"] * 10000
    large_price = calculator.calculate_price("thin", "large", large_toppings)
    print("Large Data Test Price:", large_price)


if __name__ == "__main__":
    main()
