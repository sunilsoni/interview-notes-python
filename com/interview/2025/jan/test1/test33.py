class Pizza:
    BASE_PRICES = {
        'thin': 8,
        'regular': 7
    }

    SIZE_MULTIPLIERS = {
        'small': 0.75,
        'medium': 1.0,
        'large': 2.0
    }

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

    def __str__(self):
        return f"{self.size.capitalize()} {self.base} crust pizza with {', '.join(self.toppings) or 'no toppings'}"


class Order:
    def __init__(self):
        self.pizzas = []

    def add_pizza(self, pizza):
        self.pizzas.append(pizza)

    def calculate_total(self):
        return sum(pizza.calculate_price() for pizza in self.pizzas)

    def get_order_summary(self):
        summary = "Order Summary:\n"
        for i, pizza in enumerate(self.pizzas, 1):
            price = pizza.calculate_price()
            summary += f"{i}. {pizza} - ${price:.2f}\n"
        summary += f"\nTotal: ${self.calculate_total():.2f}"
        return summary


def run_tests():
    print("Running tests...\n")

    # Test Case 1: Single pizza order
    print("Test Case 1: Single Pizza Order")
    order1 = Order()
    order1.add_pizza(Pizza('thin', 'small', ['cheese']))
    print(order1.get_order_summary())
    print("\n" + "=" * 50 + "\n")

    # Test Case 2: Multiple pizza order
    print("Test Case 2: Multiple Pizza Order")
    order2 = Order()
    order2.add_pizza(Pizza('thin', 'small', ['cheese']))
    order2.add_pizza(Pizza('regular', 'large', ['cheese', 'pepperoni']))
    order2.add_pizza(Pizza('thin', 'medium', ['olives']))
    print(order2.get_order_summary())
    print("\n" + "=" * 50 + "\n")

    # Test Case 3: Empty order
    print("Test Case 3: Empty Order")
    order3 = Order()
    print(order3.get_order_summary())
    print("\n" + "=" * 50 + "\n")

    # Test Case 4: Large order (stress test)
    print("Test Case 4: Large Order (20 pizzas)")
    order4 = Order()
    for _ in range(20):
        order4.add_pizza(Pizza('thin', 'large', ['cheese', 'pepperoni']))
    print(order4.get_order_summary())


if __name__ == "__main__":
    # Interactive demo
    print("Welcome to Pizza Shop!")
    order = Order()

    while True:
        print("\nMenu Options:")
        print("1. Add pizza to order")
        print("2. View current order")
        print("3. Finish and checkout")
        print("4. Cancel order")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            base = input("Enter base type (thin/regular): ")
            size = input("Enter size (small/medium/large): ")
            toppings = input("Enter toppings (comma-separated, or press enter for none): ")

            toppings = [t.strip() for t in toppings.split(',')] if toppings else []

            try:
                pizza = Pizza(base, size, toppings)
                order.add_pizza(pizza)
                print("\nPizza added to order!")
            except ValueError as e:
                print(f"\nError: {e}")

        elif choice == '2':
            if order.pizzas:
                print("\n" + order.get_order_summary())
            else:
                print("\nOrder is empty!")

        elif choice == '3':
            if order.pizzas:
                print("\nFinal " + order.get_order_summary())
                print("\nThank you for your order!")
            else:
                print("\nCannot checkout empty order!")
            break

        elif choice == '4':
            print("\nOrder cancelled!")
            break

        else:
            print("\nInvalid choice! Please try again.")

    # Run automated tests
    print("\nRunning automated tests...")
    run_tests()
