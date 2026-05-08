#!/usr/bin/env python3
"""
Test script for the Student Grades API Server

This script tests the REST API endpoints to ensure they work correctly
with the SQLite database.
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:5001/api"

def test_api_endpoints():
    """Test all API endpoints"""
    print("=== Testing Student Grades API Server ===\n")
    
    # Wait a moment for server to start
    time.sleep(1)
    
    # Test 1: Health check
    print("1. Testing GET /api/health:")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Result: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test 2: Get student count
    print("2. Testing GET /api/students/count:")
    try:
        response = requests.get(f"{API_BASE_URL}/students/count")
        print(f"   Status: {response.status_code}")
        print(f"   Result: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test 3: Get grade statistics
    print("3. Testing GET /api/students/statistics:")
    try:
        response = requests.get(f"{API_BASE_URL}/students/statistics")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Average Grade: {result.get('average_grade', 'N/A')}")
        print(f"   Grade Distribution: {result.get('grade_distribution', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test 4: Get top 5 students
    print("4. Testing GET /api/students/top?limit=5:")
    try:
        response = requests.get(f"{API_BASE_URL}/students/top?limit=5")
        print(f"   Status: {response.status_code}")
        result = response.json()
        if 'top_students' in result:
            print("   Top 5 Students:")
            for i, student in enumerate(result['top_students'], 1):
                print(f"     {i}. {student['name']}: {student['grade']}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test 5: Search for students with 'John' in name
    print("5. Testing GET /api/students/search?name=John:")
    try:
        response = requests.get(f"{API_BASE_URL}/students/search?name=John")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Found {result.get('count', 0)} students with 'John' in name")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test 6: Search for students with grades above 90
    print("6. Testing GET /api/students/search?min_grade=90:")
    try:
        response = requests.get(f"{API_BASE_URL}/students/search?min_grade=90")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Found {result.get('count', 0)} students with grades above 90")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test 7: Get student by ID (assuming ID 1 exists)
    print("7. Testing GET /api/students/1:")
    try:
        response = requests.get(f"{API_BASE_URL}/students/1")
        print(f"   Status: {response.status_code}")
        result = response.json()
        if 'student' in result:
            student = result['student']
            print(f"   Student: {student['name']}, Grade: {student['grade']}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test 8: Add a new student
    print("8. Testing POST /api/students:")
    try:
        new_student = {
            "name": "API Test Student",
            "grade": 87.5,
            "email": "api.test@university.edu"
        }
        response = requests.post(f"{API_BASE_URL}/students", json=new_student)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Result: {result}")
        
        # Store the new student ID for later tests
        if result.get('success') and 'student_id' in result:
            new_student_id = result['student_id']
        else:
            new_student_id = None
    except Exception as e:
        print(f"   Error: {e}")
        new_student_id = None
    print()
    
    # Test 9: Update student grade (if we have a student ID)
    if new_student_id:
        print(f"9. Testing PUT /api/students/{new_student_id}:")
        try:
            update_data = {"grade": 92.0}
            response = requests.put(f"{API_BASE_URL}/students/{new_student_id}", json=update_data)
            print(f"   Status: {response.status_code}")
            result = response.json()
            print(f"   Result: {result}")
        except Exception as e:
            print(f"   Error: {e}")
        print()
        
        # Test 10: Delete the test student
        print(f"10. Testing DELETE /api/students/{new_student_id}:")
        try:
            response = requests.delete(f"{API_BASE_URL}/students/{new_student_id}")
            print(f"   Status: {response.status_code}")
            result = response.json()
            print(f"   Result: {result}")
        except Exception as e:
            print(f"   Error: {e}")
        print()
    
    # Test 11: Get database schema
    print("11. Testing GET /api/database/schema:")
    try:
        response = requests.get(f"{API_BASE_URL}/database/schema")
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Table: {result.get('table_name', 'N/A')}")
        print(f"   Total Records: {result.get('total_records', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    # Test 12: Execute custom query
    print("12. Testing POST /api/database/query:")
    try:
        query_data = {
            "query": "SELECT student_name, grade FROM student_grades WHERE grade > 95 ORDER BY grade DESC LIMIT 3"
        }
        response = requests.post(f"{API_BASE_URL}/database/query", json=query_data)
        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Found {result.get('row_count', 0)} students with grades above 95")
        if result.get('results'):
            print("   Results:")
            for student in result['results']:
                print(f"     {student['student_name']}: {student['grade']}")
    except Exception as e:
        print(f"   Error: {e}")
    print()
    
    print("=== API Testing Complete ===")

def check_database_exists():
    """Check if the database file exists and has data"""
    import sqlite3
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
        print("Starting API server test...")
        print("Make sure the API server is running on http://localhost:5001")
        print("Run: python3 student_grades_api.py")
        print()
        test_api_endpoints()
    else:
        print("Database not found. Please run 'python3 test.py' first to create it.")
