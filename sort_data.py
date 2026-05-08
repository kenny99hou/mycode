import random
import matplotlib.pyplot as plt

class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

# Original students
students = [
    Student("Alice", 88),
    Student("Bob", 95),
    Student("Charlie", 78),
    Student("Ken", 99.1)
]

# Generate 200 random students
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna", "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle", "Kevin", "Laura", "Brian", "Sarah", "George", "Kimberly", "Edward", "Deborah", "Ronald", "Dorothy", "Timothy", "Lisa", "Jason", "Nancy", "Jeffrey", "Karen", "Ryan", "Betty", "Jacob", "Helen", "Gary", "Sandra", "Nicholas", "Donna", "Eric", "Carol", "Jonathan", "Ruth", "Stephen", "Sharon", "Larry", "Michelle", "Justin", "Laura", "Scott", "Sarah", "Brandon", "Kimberly", "Benjamin", "Deborah", "Samuel", "Dorothy", "Gregory", "Lisa", "Frank", "Nancy", "Alexander", "Karen", "Raymond", "Betty", "Patrick", "Helen", "Jack", "Sandra", "Dennis", "Donna", "Jerry", "Carol", "Tyler", "Ruth", "Henry", "Sharon", "Peter", "Michelle", "Walter", "Laura", "Christian", "Sarah", "Chris", "Kimberly", "Aaron", "Deborah", "Jose", "Dorothy", "Billy", "Lisa", "Ethan", "Nancy", "Russell", "Karen", "Vincent", "Betty", "Adam", "Helen", "Johnny", "Sandra", "Ryan", "Donna", "Nathan", "Carol", "Douglas", "Ruth", "Zachary", "Sharon", "Walter", "Michelle", "Kyle", "Laura", "Eddie", "Sarah", "Walter", "Kimberly", "Jerry", "Deborah", "Russell", "Dorothy", "Ethan", "Lisa", "Patrick", "Nancy", "Jose", "Karen", "Billy", "Betty", "Adam", "Helen", "Johnny", "Sandra", "Ryan", "Donna", "Nathan", "Carol", "Douglas", "Ruth", "Zachary", "Sharon", "Walter", "Michelle", "Kyle", "Laura", "Eddie", "Sarah", "Jerry", "Kimberly", "Russell", "Deborah", "Ethan", "Dorothy", "Patrick", "Lisa", "Jose", "Nancy", "Billy", "Karen", "Adam", "Betty", "Johnny", "Helen", "Ryan", "Sandra", "Nathan", "Donna", "Douglas", "Carol", "Zachary", "Ruth", "Walter", "Sharon", "Kyle", "Michelle", "Eddie", "Laura", "Jerry", "Sarah", "Russell", "Kimberly", "Ethan", "Deborah", "Patrick", "Dorothy", "Jose", "Lisa", "Billy", "Nancy", "Adam", "Karen", "Johnny", "Betty", "Ryan", "Helen", "Nathan", "Sandra", "Douglas", "Donna", "Zachary", "Carol", "Walter", "Ruth", "Kyle", "Sharon", "Eddie", "Michelle", "Jerry", "Laura", "Russell", "Sarah", "Ethan", "Kimberly", "Patrick", "Deborah", "Jose", "Dorothy", "Billy", "Lisa", "Adam", "Nancy", "Johnny", "Karen", "Ryan", "Betty", "Nathan", "Helen", "Douglas", "Sandra", "Zachary", "Donna", "Walter", "Carol", "Kyle", "Ruth", "Eddie", "Sharon", "Jerry", "Michelle", "Russell", "Laura", "Ethan", "Sarah", "Patrick", "Kimberly", "Jose", "Deborah", "Billy", "Dorothy", "Adam", "Lisa", "Johnny", "Nancy", "Ryan", "Karen", "Nathan", "Betty", "Douglas", "Helen", "Zachary", "Sandra", "Walter", "Donna", "Kyle", "Carol", "Eddie", "Ruth", "Jerry", "Sharon", "Russell", "Michelle", "Ethan", "Laura", "Patrick", "Sarah", "Jose", "Kimberly", "Billy", "Deborah", "Adam", "Dorothy", "Johnny", "Lisa", "Ryan", "Nancy", "Nathan", "Karen", "Douglas", "Betty", "Zachary", "Helen", "Walter", "Sandra", "Kyle", "Donna", "Eddie", "Carol", "Jerry", "Ruth", "Russell", "Sharon", "Ethan", "Michelle", "Patrick", "Laura", "Jose", "Sarah", "Billy", "Kimberly", "Adam", "Deborah", "Johnny", "Dorothy", "Ryan", "Lisa", "Nathan", "Nancy", "Douglas", "Karen", "Zachary", "Betty", "Walter", "Helen", "Kyle", "Sandra", "Eddie", "Donna", "Jerry", "Carol", "Russell", "Ruth", "Ethan", "Sharon", "Patrick", "Michelle", "Jose", "Laura", "Billy", "Sarah", "Adam", "Kimberly", "Johnny", "Deborah", "Ryan", "Dorothy", "Nathan", "Lisa", "Douglas", "Nancy", "Zachary", "Karen", "Walter", "Betty", "Kyle", "Helen", "Eddie", "Sandra", "Jerry", "Donna", "Russell", "Carol", "Ethan", "Ruth", "Patrick", "Sharon", "Jose", "Michelle", "Billy", "Laura", "Adam", "Sarah", "Johnny", "Kimberly", "Ryan", "Deborah", "Nathan", "Dorothy", "Douglas", "Lisa", "Zachary", "Nancy", "Walter", "Karen", "Kyle", "Betty", "Eddie", "Helen", "Jerry", "Sandra", "Russell", "Donna", "Ethan", "Carol", "Patrick", "Ruth", "Jose", "Sharon", "Billy", "Michelle", "Adam", "Laura", "Johnny", "Sarah", "Ryan", "Kimberly", "Nathan", "Deborah", "Douglas", "Dorothy", "Zachary", "Lisa", "Walter", "Nancy", "Kyle", "Karen", "Eddie", "Betty", "Jerry", "Helen", "Russell", "Sandra", "Ethan", "Donna", "Patrick", "Carol", "Jose", "Ruth", "Billy", "Sharon", "Adam", "Michelle", "Johnny", "Laura", "Ryan", "Sarah", "Nathan", "Kimberly", "Douglas", "Deborah", "Zachary", "Dorothy", "Walter", "Lisa", "Kyle", "Nancy", "Eddie", "Karen", "Jerry", "Betty", "Russell", "Helen", "Ethan", "Sandra", "Patrick", "Donna", "Jose", "Carol", "Billy", "Ruth", "Adam", "Sharon", "Johnny", "Michelle", "Ryan", "Laura", "Nathan", "Sarah", "Douglas", "Kimberly", "Zachary", "Deborah", "Walter", "Dorothy", "Kyle", "Lisa", "Eddie", "Nancy", "Jerry", "Karen", "Russell", "Betty", "Ethan", "Helen", "Patrick", "Sandra", "Jose", "Donna", "Billy", "Carol", "Adam", "Ruth", "Johnny", "Sharon", "Ryan", "Michelle", "Nathan", "Laura", "Douglas", "Sarah", "Zachary", "Kimberly", "Walter", "Deborah", "Kyle", "Dorothy", "Eddie", "Lisa", "Jerry", "Nancy", "Russell", "Karen", "Ethan", "Betty", "Patrick", "Helen", "Sandra", "Jose", "Donna", "Billy", "Carol", "Adam", "Ruth", "Johnny", "Sharon", "Ryan", "Michelle", "Nathan", "Laura"]

# Add 200 random students with random grades between 60-100
for i in range(200):
    name = random.choice(first_names) + f" {i+1}"
    grade = round(random.uniform(60, 100), 1)
    students.append(Student(name, grade))

print(f"Total students: {len(students)}")

# Sort students by grade
sorted_students = sorted(students, key=lambda s: s.grade, reverse=True)

# Create visualization
plt.figure(figsize=(15, 8))

# Histogram of grade distribution
plt.subplot(1, 2, 1)
grades = [s.grade for s in students]
plt.hist(grades, bins=20, edgecolor='black', alpha=0.7, color='skyblue')
plt.xlabel('Grade')
plt.ylabel('Number of Students')
plt.title('Grade Distribution')
plt.grid(True, alpha=0.3)

# Top 20 students bar chart
plt.subplot(1, 2, 2)
top_20 = sorted_students[:20]
names = [s.name[:15] + "..." if len(s.name) > 15 else s.name for s in top_20]
grades_top20 = [s.grade for s in top_20]

plt.barh(names, grades_top20, color='lightcoral')
plt.xlabel('Grade')
plt.title('Top 20 Students')
plt.gca().invert_yaxis()  # Highest grade at top

plt.tight_layout()
plt.show()

# Print top 10 students
print("\nTop 10 Students:")
print("="*40)
for i, student in enumerate(sorted_students[:10], 1):
    print(f"{i:2d}. {student.name}: {student.grade}")

# Print statistics
grades = [s.grade for s in students]
print(f"\nStatistics:")
print(f"Average grade: {sum(grades)/len(grades):.2f}")
print(f"Highest grade: {max(grades):.1f}")
print(f"Lowest grade: {min(grades):.1f}")
print(f"Median grade: {sorted(grades)[len(grades)//2]:.1f}")
# Output:
# Ken: 99.1
# Bob: 95
# Alice: 88
# Charlie: 78
