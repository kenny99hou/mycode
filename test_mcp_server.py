#!/usr/bin/env python3
"""
Test script for the Student Grades MCP Server

This script tests the MCP server tools to ensure they work correctly
with the SQLite database.
"""

import json
import sqlite3
from mcp_student_server import *

def test_mcp_server():
    """Test all MCP server tools"""
    print("=== Testing Student Grades MCP Server ===\n")
    
    # Test 1: Get student count
    print("1. Testing get_student_count():")
    result = json.loads(get_student_count())
    print(f"   Result: {result}")
    print()
    
    # Test 2: Get grade statistics
    print("2. Testing get_grade_statistics():")
    result = json.loads(get_grade_statistics())
    print(f"   Result: {result}")
    print()
    
    # Test 3: Get top 5 students
    print("3. Testing get_top_students(5):")
    result = json.loads(get_top_students(5))
    print(f"   Result: {result}")
    print()
    
    # Test 4: Search for students with 'John' in name
    print("4. Testing search_students(name='John'):")
    result = json.loads(search_students(name="John"))
    print(f"   Result: {result}")
    print()
    
    # Test 5: Search for students with grades above 90
    print("5. Testing search_students(min_grade=90):")
    result = json.loads(search_students(min_grade=90))
    print(f"   Found {result.get('count', 0)} students with grades above 90")
    if result.get('search_results'):
        print("   Top 3:")
        for i, student in enumerate(result['search_results'][:3], 1):
            print(f"     {i}. {student['name']}: {student['grade']}")
    print()
    
    # Test 6: Get student by ID (assuming ID 1 exists)
    print("6. Testing get_student_by_id(1):")
    result = json.loads(get_student_by_id(1))
    print(f"   Result: {result}")
    print()
    
    # Test 7: Get database schema
    print("7. Testing get_database_schema():")
    result = json.loads(get_database_schema())
    print(f"   Result: {result}")
    print()
    
    # Test 8: Add a new student
    print("8. Testing add_student():")
    result = json.loads(add_student("Test Student", 85.5, "test.student@university.edu"))
    print(f"   Result: {result}")
    print()
    
    # Test 9: Execute custom query
    print("9. Testing execute_custom_query():")
    query = "SELECT student_name, grade FROM student_grades WHERE grade > 95 ORDER BY grade DESC LIMIT 3"
    result = json.loads(execute_custom_query(query))
    print(f"   Query: {query}")
    print(f"   Result: {result}")
    print()
    
    print("=== MCP Server Testing Complete ===")

def check_database_exists():
    """Check if the database file exists and has data"""
    try:
        conn = sqlite3.connect("student_grades.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM student_grades")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Database 'student_grades.db' exists with {count} records")
        return True
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        print("Please run 'python3 test.py' first to create the database")
        return False

if __name__ == "__main__":
    if check_database_exists():
        test_mcp_server()
    else:
        print("Database not found. Please run 'python3 test.py' first to create it.")
