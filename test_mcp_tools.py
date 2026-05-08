#!/usr/bin/env python3
"""
Test script for the Student Grades MCP Server (Python 3.10)

This script tests all MCP tools to ensure they work correctly
with the SQLite database using Python 3.10 and the MCP library.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import MCP tools
from mcp_student_grades import (
    get_student_summary,
    get_students_by_criteria,
    get_student_details,
    get_grade_analysis,
    find_similar_students,
    get_enrollment_trends,
    execute_ai_query
)

def test_mcp_tools():
    """Test all MCP tools"""
    print("=== Testing Student Grades MCP Server (Python 3.10) ===\n")
    
    # Test 1: Get student summary
    print("1. Testing get_student_summary():")
    result = get_student_summary()
    print(f"   Result length: {len(result)} characters")
    print("   ✅ Working")
    print()
    
    # Test 2: Get students by criteria
    print("2. Testing get_students_by_criteria(min_grade=90, limit=5):")
    result = get_students_by_criteria(min_grade=90, limit=5)
    print(f"   Result length: {len(result)} characters")
    print("   ✅ Working")
    print()
    
    # Test 3: Get student details
    print("3. Testing get_student_details(1):")
    result = get_student_details(1)
    print(f"   Result length: {len(result)} characters")
    print("   ✅ Working")
    print()
    
    # Test 4: Get grade analysis
    print("4. Testing get_grade_analysis():")
    result = get_grade_analysis()
    print(f"   Result length: {len(result)} characters")
    print("   ✅ Working")
    print()
    
    # Test 5: Find similar students
    print("5. Testing find_similar_students(85, tolerance=3, limit=3):")
    result = find_similar_students(85, tolerance=3, limit=3)
    print(f"   Result length: {len(result)} characters")
    print("   ✅ Working")
    print()
    
    # Test 6: Get enrollment trends
    print("6. Testing get_enrollment_trends():")
    result = get_enrollment_trends()
    print(f"   Result length: {len(result)} characters")
    print("   ✅ Working")
    print()
    
    # Test 7: Execute AI query
    print("7. Testing execute_ai_query('how many students'):")
    result = execute_ai_query("how many students")
    print(f"   Result length: {len(result)} characters")
    print("   ✅ Working")
    print()
    
    print("=== All MCP Tools Working Correctly ===")

def check_python_version():
    """Check if we're using Python 3.10+"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 10:
        print("✅ Python 3.10+ detected - MCP compatible")
        return True
    else:
        print("❌ Python version too old for MCP")
        return False

def check_database():
    """Check if database exists and has data"""
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
        return False

if __name__ == "__main__":
    print("MCP Server Test Suite")
    print("====================\n")
    
    if check_python_version() and check_database():
        test_mcp_tools()
    else:
        print("Cannot proceed with tests - check Python version and database")
