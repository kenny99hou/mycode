def calculate_area(length, width):
    """Calculates the area of a rectangle."""
    return length * width

area = calculate_area(5, 3)
print(f"Area of rectangle: {area}")

class Car:
  def __init__(self, make, model, year, color):  # Constructor with arguments
    """Initializes a Car object with the given attributes."""
    self.make = make
    self.model = model
    self.year = year
    self.color = color

  def describe(self):
    """Returns a descriptive string about the car."""
    #print(f"This is a {self.year} {self.make} {self.model} {self.color}.")
    return f"This is a {self.year} {self.make} {self.model} {self.color}."

# Create Car objects with different attributes
my_car = Car("Ford", "Mustang", 2023, '')
his_car = Car("Toyota", "Camry", 2020, '')
bad_car = Car("bad", "bad-make", 1900, "blue")

# Access and print attributes
print(my_car.describe())  # Output: This is a 2023 Ford Mustang.
print(his_car.describe())  # Output: This is a 2020 Toyota Camry.
print(bad_car.describe())



name = "Alice"
age = 30

# Traditional string formatting
greeting = "Hello, " + name + "! You are " + str(age) + " years old."
print(greeting)

# Using f-strings for formatted output
f_greeting = f"Hello, {name}! You are {age} years old."
print(f_greeting)

class Person:
  def __init__(self, name, age):
    self.name = name  # Assign the value of the argument to the object's attribute
    self.age = age

  def greet(self):
    """Greets the person by name."""
    print(f"Hello, my name is {self.name} and I am {self.age} years old.")

# Create a Person object
person1 = Person("Alice", 30)

# Call the greet() method on the object
person1.greet()