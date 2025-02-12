class Pizza:
    # Base prices
    BASE_PRICES = {
        'thin': 8,
        'regular': 7
    }

    # Size multipliers
    SIZE_MULTIPLIERS = {
        'small': 0.75,
        'medium': 1.0,
        'large': 2.0
    }

    # Topping prices
    TOPPING_PRICES = {
        'cheese': 2,
        'olives': 1,
        'pepperoni': 3
    }

    def __init__(self, base, size, toppings=None):
        self.base = base.lower()
        self.size = size.lower()
        self.toppings = [t.lower() for t in (toppings or [])]

    def calculate_price(self):
        if self.base not in self.BASE_PRICES:
            raise ValueError(f"Invalid base type: {self.base}")
        if self.size not in self.SIZE_MULTIPLIERS:
            raise ValueError(f"Invalid size: {self.size}")

        base_price = self.BASE_PRICES[self.base]
        toppings_price = sum(self.TOPPING_PRICES.get(t, 0) for t in self.toppings)
        size_multiplier = self.SIZE_MULTIPLIERS[self.size]

        return (base_price + toppings_price) * size_multiplier


def run_tests():
    test_cases = [
        {
            'name': "Small thin crust cheese pizza",
            'input': Pizza('thin', 'small', ['cheese']),
            'expected': 7.50
        },
        {
            'name': "Medium thin crust cheese pizza",
            'input': Pizza('thin', 'small', ['cheese']),
            'expected': 10.00
        }
    ]

    for test in test_cases:
        actual = test['input'].calculate_price()
        passed = abs(actual - test['expected']) < 0.01  # Handle floating point comparison
        result = "PASS" if passed else "FAIL"
        print(f"{test['name']}: {result}")
        print(f"Expected: ${test['expected']:.2f}, Got: ${actual:.2f}\n")


if __name__ == "__main__":
    # Run the tests
    run_tests()

    # Example of handling large data
    large_order = Pizza('thin', 'large', ['cheese'] * 100)
    try:
        price = large_order.calculate_price()
        print(f"Large order price: ${price:.2f}")
    except Exception as e:
        print(f"Error processing large order: {e}")
