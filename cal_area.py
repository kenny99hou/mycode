def calculate_area(length, width):
    """Calculates the area of a rectangle."""
    return length * width

area = calculate_area(5, 3)
print(f"Area of rectangle: {area}")

class Car:
  def __init__(self, make, model, year):  # Constructor with arguments
    """Initializes a Car object with the given attributes."""
    self.make = make
    self.model = model
    self.year = year

  def describe(self):
    """Returns a descriptive string about the car."""
    return f"This is a {self.year} {self.make} {self.model}."

# Create Car objects with different attributes
my_car = Car("Ford", "Mustang", 2023)
his_car = Car("Toyota", "Camry", 2020)

# Access and print attributes
print(my_car.describe())  # Output: This is a 2023 Ford Mustang.
print(his_car.describe())  # Output: This is a 2020 Toyota Camry.