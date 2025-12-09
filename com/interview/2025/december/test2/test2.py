# Parent class
class Parent:
    def __init__(self, name):
        self.name = name

    def show_info(self):
        print(f"Parent name: {self.name}")


# Child class inherits from Parent
class Child(Parent):
    def __init__(self, name, age):
        # Call Parent's constructor using super()
        super().__init__(name)
        self.age = age

    # Override method
    def show_info(self):
        # Call Parent's method first
        super().show_info()
        print(f"Child age: {self.age}")


# Usage
p = Parent("Uday")
p.show_info()

c = Child("Uday Pavuluri", 20)
c.show_info()
