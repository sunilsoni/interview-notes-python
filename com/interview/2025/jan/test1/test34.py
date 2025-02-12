from abc import ABC, abstractmethod
from typing import List


# Base class for all orderable items
class OrderItem(ABC):
    @abstractmethod
    def calculate_price(self) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Pizza(OrderItem):
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

    def __init__(self, base: str, size: str, toppings: List[str] = None):
        self.base = base.lower()
        self.size = size.lower()
        self.toppings = [t.lower() for t in (toppings or [])]

    def calculate_price(self) -> float:
        if self.base not in self.BASE_PRICES:
            raise ValueError(f"Invalid base type: {self.base}")
        if self.size not in self.SIZE_MULTIPLIERS:
            raise ValueError(f"Invalid size: {self.size}")

        base_price = self.BASE_PRICES[self.base]
        toppings_price = sum(self.TOPPING_PRICES.get(t, 0) for t in self.toppings)
        size_multiplier = self.SIZE_MULTIPLIERS[self.size]

        return (base_price + toppings_price) * size_multiplier

    def __str__(self) -> str:
        return f"{self.size.capitalize()} {self.base} crust pizza with {', '.join(self.toppings) or 'no toppings'}"


class Drink(OrderItem):
    PRICES = {
        'soda': {'small': 2, 'medium': 3, 'large': 4},
        'juice': {'small': 3, 'medium': 4, 'large': 5},
        'water': {'small': 1, 'medium': 2, 'large': 3}
    }

    def __init__(self, type_: str, size: str):
        self.type = type_.lower()
        self.size = size.lower()
        if self.type not in self.PRICES:
            raise ValueError(f"Invalid drink type: {self.type}")
        if self.size not in self.PRICES[self.type]:
            raise ValueError(f"Invalid size: {self.size}")

    def calculate_price(self) -> float:
        return self.PRICES[self.type][self.size]

    def __str__(self) -> str:
        return f"{self.size.capitalize()} {self.type}"


class Cookie(OrderItem):
    PRICES = {
        'chocolate_chip': 2,
        'oatmeal': 2,
        'sugar': 1.5
    }

    def __init__(self, type_: str, quantity: int = 1):
        self.type = type_.lower()
        self.quantity = quantity
        if self.type not in self.PRICES:
            raise ValueError(f"Invalid cookie type: {self.type}")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

    def calculate_price(self) -> float:
        return self.PRICES[self.type] * self.quantity

    def __str__(self) -> str:
        return f"{self.type.replace('_', ' ').title()} Cookie (x{self.quantity})"


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item: OrderItem):
        self.items.append(item)

    def calculate_total(self) -> float:
        return sum(item.calculate_price() for item in self.items)

    def get_order_summary(self) -> str:
        if not self.items:
            return "Order is empty!"

        summary = "Order Summary:\n"
        for i, item in enumerate(self.items, 1):
            price = item.calculate_price()
            summary += f"{i}. {item} - ${price:.2f}\n"
        summary += f"\nTotal: ${self.calculate_total():.2f}"
        return summary


def show_menu():
    print("\nMenu Options:")
    print("1. Add pizza")
    print("2. Add drink")
    print("3. Add cookies")
    print("4. View current order")
    print("5. Finish and checkout")
    print("6. Cancel order")


def main():
    print("Welcome to Pizza & More!")
    order = Order()

    while True:
        show_menu()
        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            try:
                base = input("Enter base type (thin/regular): ")
                size = input("Enter size (small/medium/large): ")
                toppings = input("Enter toppings (comma-separated, or press enter for none): ")
                toppings = [t.strip() for t in toppings.split(',')] if toppings else []

                pizza = Pizza(base, size, toppings)
                order.add_item(pizza)
                print("\nPizza added to order!")
            except ValueError as e:
                print(f"\nError: {e}")

        elif choice == '2':
            try:
                type_ = input("Enter drink type (soda/juice/water): ")
                size = input("Enter size (small/medium/large): ")

                drink = Drink(type_, size)
                order.add_item(drink)
                print("\nDrink added to order!")
            except ValueError as e:
                print(f"\nError: {e}")

        elif choice == '3':
            try:
                type_ = input("Enter cookie type (chocolate_chip/oatmeal/sugar): ")
                quantity = int(input("Enter quantity: "))

                cookie = Cookie(type_, quantity)
                order.add_item(cookie)
                print("\nCookies added to order!")
            except ValueError as e:
                print(f"\nError: {e}")

        elif choice == '4':
            print("\n" + order.get_order_summary())

        elif choice == '5':
            if order.items:
                print("\nFinal " + order.get_order_summary())
                print("\nThank you for your order!")
            else:
                print("\nCannot checkout empty order!")
            break

        elif choice == '6':
            print("\nOrder cancelled!")
            break

        else:
            print("\nInvalid choice! Please try again.")


def run_tests():
    print("\nRunning tests...")

    # Test case 1: Mixed order
    order = Order()
    order.add_item(Pizza('thin', 'medium', ['cheese', 'pepperoni']))
    order.add_item(Drink('soda', 'large'))
    order.add_item(Cookie('chocolate_chip', 2))
    print("\nTest Case 1: Mixed Order")
    print(order.get_order_summary())

    # Add more test cases as needed


if __name__ == "__main__":
    main()
    run_tests()
