from abc import ABC, abstractmethod
from typing import List, Dict


class Store:
    def __init__(self, store_id: str, name: str, price_catalog: Dict):
        self.store_id = store_id
        self.name = name
        self.price_catalog = price_catalog

    def get_pizza_base_price(self, base_type: str) -> float:
        return self.price_catalog['pizza_bases'][base_type]

    def get_pizza_size_multiplier(self, size: str) -> float:
        return self.price_catalog['pizza_size_multipliers'][size]

    def get_topping_price(self, topping: str) -> float:
        return self.price_catalog['pizza_toppings'][topping]

    def get_drink_price(self, type_: str, size: str) -> float:
        return self.price_catalog['drinks'][type_][size]

    def get_cookie_price(self, type_: str) -> float:
        return self.price_catalog['cookies'][type_]


class OrderItem(ABC):
    @abstractmethod
    def calculate_price(self, store: Store) -> float:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Pizza(OrderItem):
    def __init__(self, base: str, size: str, toppings: List[str] = None):
        self.base = base.lower()
        self.size = size.lower()
        self.toppings = [t.lower() for t in (toppings or [])]

    def calculate_price(self, store: Store) -> float:
        base_price = store.get_pizza_base_price(self.base)
        toppings_price = sum(store.get_topping_price(t) for t in self.toppings)
        size_multiplier = store.get_pizza_size_multiplier(self.size)

        return (base_price + toppings_price) * size_multiplier

    def __str__(self) -> str:
        return f"{self.size.capitalize()} {self.base} crust pizza with {', '.join(self.toppings) or 'no toppings'}"


class Drink(OrderItem):
    def __init__(self, type_: str, size: str):
        self.type = type_.lower()
        self.size = size.lower()

    def calculate_price(self, store: Store) -> float:
        return store.get_drink_price(self.type, self.size)

    def __str__(self) -> str:
        return f"{self.size.capitalize()} {self.type}"


class Cookie(OrderItem):
    def __init__(self, type_: str, quantity: int = 1):
        self.type = type_.lower()
        self.quantity = quantity
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")

    def calculate_price(self, store: Store) -> float:
        return store.get_cookie_price(self.type) * self.quantity

    def __str__(self) -> str:
        return f"{self.type.replace('_', ' ').title()} Cookie (x{self.quantity})"


class Order:
    def __init__(self, store: Store):
        self.store = store
        self.items = []

    def add_item(self, item: OrderItem):
        self.items.append(item)

    def calculate_total(self) -> float:
        return sum(item.calculate_price(self.store) for item in self.items)

    def get_order_summary(self) -> str:
        if not self.items:
            return f"Order is empty! (Store: {self.store.name})"

        summary = f"Order Summary (Store: {self.store.name}):\n"
        for i, item in enumerate(self.items, 1):
            price = item.calculate_price(self.store)
            summary += f"{i}. {item} - ${price:.2f}\n"
        summary += f"\nTotal: ${self.calculate_total():.2f}"
        return summary


# Example store configurations
DOWNTOWN_PRICES = {
    'pizza_bases': {
        'thin': 8,
        'regular': 7
    },
    'pizza_size_multipliers': {
        'small': 0.75,
        'medium': 1.0,
        'large': 2.0
    },
    'pizza_toppings': {
        'cheese': 2,
        'olives': 1,
        'pepperoni': 3
    },
    'drinks': {
        'soda': {'small': 2, 'medium': 3, 'large': 4},
        'juice': {'small': 3, 'medium': 4, 'large': 5},
        'water': {'small': 1, 'medium': 2, 'large': 3}
    },
    'cookies': {
        'chocolate_chip': 2,
        'oatmeal': 2,
        'sugar': 1.5
    }
}

SUBURB_PRICES = {
    'pizza_bases': {
        'thin': 6,
        'regular': 5
    },
    'pizza_size_multipliers': {
        'small': 0.75,
        'medium': 1.0,
        'large': 1.75
    },
    'pizza_toppings': {
        'cheese': 1.5,
        'olives': 0.75,
        'pepperoni': 2.5
    },
    'drinks': {
        'soda': {'small': 1.5, 'medium': 2.5, 'large': 3.5},
        'juice': {'small': 2.5, 'medium': 3.5, 'large': 4.5},
        'water': {'small': 0.75, 'medium': 1.5, 'large': 2.5}
    },
    'cookies': {
        'chocolate_chip': 1.5,
        'oatmeal': 1.5,
        'sugar': 1.0
    }
}


def main():
    # Create store instances
    downtown_store = Store("DT001", "Downtown Store", DOWNTOWN_PRICES)
    suburb_store = Store("SB001", "Suburb Store", SUBURB_PRICES)

    # Example orders from different stores
    print("Testing orders from different stores:")

    # Downtown order
    downtown_order = Order(downtown_store)
    downtown_order.add_item(Pizza('thin', 'medium', ['cheese', 'pepperoni']))
    downtown_order.add_item(Drink('soda', 'large'))
    print("\nDowntown Order:")
    print(downtown_order.get_order_summary())

    # Suburb order (same items)
    suburb_order = Order(suburb_store)
    suburb_order.add_item(Pizza('thin', 'medium', ['cheese', 'pepperoni']))
    suburb_order.add_item(Drink('soda', 'large'))
    print("\nSuburb Order:")
    print(suburb_order.get_order_summary())


if __name__ == "__main__":
    main()
