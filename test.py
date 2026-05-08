import sqlite3
import random
from datetime import datetime, timedelta

def create_database_and_table():
    """Create SQLite database and student grades table with 200 random students"""
    
    try:
        # Connect to SQLite database (creates file if it doesn't exist)
        connection = sqlite3.connect('student_grades.db')
        cursor = connection.cursor()
        
        print("Connected to SQLite database 'student_grades.db'")
        
        # Drop table if it exists to start fresh
        cursor.execute("DROP TABLE IF EXISTS student_grades")
        
        # Create student_grades table
        create_table_query = """
        CREATE TABLE student_grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            grade REAL NOT NULL,
            email TEXT,
            enrollment_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        print("Table 'student_grades' created successfully")
        
        # Generate 200 random students
        first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", 
            "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", 
            "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra", "Donald", "Donna", 
            "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle", 
            "Kevin", "Laura", "Brian", "George", "Kimberly", "Edward", "Deborah", "Ronald", 
            "Dorothy", "Timothy", "Jason", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", 
            "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon", "Benjamin", 
            "Samuel", "Gregory", "Frank", "Alexander", "Raymond", "Patrick", "Jack", "Dennis", 
            "Jerry", "Tyler", "Henry", "Peter", "Christian", "Chris", "Aaron", "Billy", "Ethan", 
            "Russell", "Vincent", "Adam", "Johnny"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", 
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", 
            "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", 
            "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", 
            "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", 
            "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", 
            "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", 
            "Collins", "Edwards", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", 
            "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox", 
            "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson", 
            "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross", 
            "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", 
            "Hughes", "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales", 
            "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes", "Myers", "Ford", 
            "Hamilton", "Graham", "Sullivan", "Wallace", "Woods", "Cole", "West", "Jordan", 
            "Owens", "Reynolds", "Fisher", "Ellis", "Harrison", "Gibson"
        ]
        
        # Insert 200 random students
        insert_query = """
        INSERT INTO student_grades (student_name, grade, email, enrollment_date)
        VALUES (?, ?, ?, ?)
        """
        
        students_data = []
        for i in range(1, 201):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            student_name = f"{first_name} {last_name}"
            grade = round(random.uniform(60, 100), 2)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@university.edu"
            
            # Random enrollment date within the last 2 years
            start_date = datetime(2022, 1, 1)
            random_days = random.randint(0, 730)  # 2 years = 730 days
            enrollment_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
            
            students_data.append((student_name, grade, email, enrollment_date))
        
        # Execute batch insert
        cursor.executemany(insert_query, students_data)
        connection.commit()
        
        print(f"Successfully inserted {cursor.rowcount} students into the database")
        
        # Display some statistics
        cursor.execute("SELECT COUNT(*) FROM student_grades")
        total_students = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(grade), MAX(grade), MIN(grade) FROM student_grades")
        avg_grade, max_grade, min_grade = cursor.fetchone()
        
        cursor.execute("SELECT student_name, grade FROM student_grades ORDER BY grade DESC LIMIT 5")
        top_students = cursor.fetchall()
        
        print(f"\n=== Database Statistics ===")
        print(f"Total Students: {total_students}")
        print(f"Average Grade: {avg_grade:.2f}")
        print(f"Highest Grade: {max_grade}")
        print(f"Lowest Grade: {min_grade}")
        print(f"\n=== Top 5 Students ===")
        for i, (name, grade) in enumerate(top_students, 1):
            print(f"{i}. {name}: {grade}")
            
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        
    finally:
        if 'connection' in locals():
            connection.close()
            print("\nSQLite connection closed")

def query_sample_data():
    """Query and display sample data from the database"""
    try:
        connection = sqlite3.connect('student_grades.db')
        cursor = connection.cursor()
        
        # Show sample records
        cursor.execute("SELECT * FROM student_grades LIMIT 10")
        records = cursor.fetchall()
        
        print("\n=== Sample Records ===")
        print("ID | Name                | Grade | Email                          | Enrollment Date")
        print("-" * 80)
        for record in records:
            print(f"{record[0]:3d} | {record[1]:18s} | {record[2]:5.2f} | {record[3]:30s} | {record[4]}")
        
        # Show table schema
        cursor.execute("PRAGMA table_info(student_grades)")
        columns = cursor.fetchall()
        print(f"\n=== Table Schema ===")
        for col in columns:
            print(f"{col[1]:15s} {col[2]:10s} {'NOT NULL' if col[3] else ''} {'PRIMARY KEY' if col[5] else ''}")
            
    except sqlite3.Error as e:
        print(f"Query Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def run_sql_queries():
    """Run some example SQL queries"""
    try:
        connection = sqlite3.connect('student_grades.db')
        cursor = connection.cursor()
        
        print("\n=== Example SQL Queries ===")
        
        # Query 1: Students with grades above 90
        cursor.execute("SELECT student_name, grade FROM student_grades WHERE grade > 90 ORDER BY grade DESC")
        honor_students = cursor.fetchall()
        print(f"\nStudents with grades above 90: {len(honor_students)}")
        for name, grade in honor_students[:5]:  # Show top 5
            print(f"  {name}: {grade}")
        
        # Query 2: Grade distribution
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN grade >= 90 THEN 'A (90-100)'
                    WHEN grade >= 80 THEN 'B (80-89)'
                    WHEN grade >= 70 THEN 'C (70-79)'
                    WHEN grade >= 60 THEN 'D (60-69)'
                    ELSE 'F (0-59)'
                END as grade_range,
                COUNT(*) as count
            FROM student_grades 
            GROUP BY grade_range
            ORDER BY grade_range DESC
        """)
        grade_distribution = cursor.fetchall()
        print(f"\nGrade Distribution:")
        for grade_range, count in grade_distribution:
            print(f"  {grade_range}: {count} students")
        
        # Query 3: Average grade by first name (for names with multiple students)
        cursor.execute("""
            SELECT 
                substr(student_name, 1, instr(student_name, ' ') - 1) as first_name,
                AVG(grade) as avg_grade,
                COUNT(*) as count
            FROM student_grades 
            GROUP BY first_name 
            HAVING count > 1
            ORDER BY avg_grade DESC
            LIMIT 5
        """)
        name_stats = cursor.fetchall()
        print(f"\nTop 5 First Names by Average Grade:")
        for first_name, avg_grade, count in name_stats:
            print(f"  {first_name}: {avg_grade:.2f} (avg) - {count} students")
            
    except sqlite3.Error as e:
        print(f"Query Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    print("=== SQLite Student Grades Database Setup ===")
    print("Creating database and inserting 200 random students...")
    create_database_and_table()
    
    print("\n=== Querying Sample Data ===")
    query_sample_data()
    
    run_sql_queries()