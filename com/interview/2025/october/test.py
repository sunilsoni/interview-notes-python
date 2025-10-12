# ===============================================
# Simple Example: Singleton + Superclass + Static
# ===============================================

# Superclass (Parent)
class Animal:
    def speak(self):
        print("Animal speaks!")  # Common behavior for all animals


# Singleton subclass (Child)
class Dog(Animal):
    _instance = None  # class variable to store only one instance

    def __new__(cls):
        # Create only one object of Dog
        if cls._instance is None:
            cls._instance = super(Dog, cls).__new__(cls)
            print("Creating new Dog instance...")
        else:
            print("Reusing existing Dog instance...")
        return cls._instance

    def speak(self):
        # Overriding superclass method
        print("Dog barks! Woof woof!")


# Static class
class MathUtil:
    @staticmethod
    def add(a, b):
        return a + b


# MAIN execution
if __name__ == "__main__":
    print("=== Singleton Demo ===")
    d1 = Dog()
    d2 = Dog()

    # Check if both are same instance
    print("Is same instance:", d1 is d2)  # should be True

    # Demonstrate inheritance
    d1.speak()  # From Dog (overrides Animal.speak)

    print("\n=== Static Class Demo ===")
    result = MathUtil.add(10, 5)
    print("Sum =", result)
