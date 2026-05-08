#!/usr/bin/env python3
"""
MCP Server for SQLite Student Grades Database

This server provides tools to interact with the student_grades SQLite database
created by the test.py script.
"""

import sqlite3
import json
from typing import Any, List, Dict, Optional
from mcp.server.fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("student_grades_db")

# Database configuration
DB_FILE = "student_grades.db"

def get_db_connection():
    """Establish connection to SQLite database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # Enable dictionary-like access
        return conn
    except sqlite3.Error as e:
        raise Exception(f"Database connection error: {e}")

@mcp.tool()
def get_student_count() -> str:
    """Get the total number of students in the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM student_grades")
        result = cursor.fetchone()
        conn.close()
        return json.dumps({"total_students": result["count"]})
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_grade_statistics() -> str:
    """Get grade statistics (average, min, max, median)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Basic statistics
        cursor.execute("SELECT AVG(grade) as avg, MAX(grade) as max, MIN(grade) as min FROM student_grades")
        stats = cursor.fetchone()
        
        # Median calculation
        cursor.execute("SELECT grade FROM student_grades ORDER BY grade")
        grades = [row["grade"] for row in cursor.fetchall()]
        median = grades[len(grades)//2] if grades else 0
        
        # Grade distribution
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
        distribution = {row["grade_range"]: row["count"] for row in cursor.fetchall()}
        
        conn.close()
        
        return json.dumps({
            "average_grade": round(stats["avg"], 2),
            "highest_grade": stats["max"],
            "lowest_grade": stats["min"],
            "median_grade": median,
            "grade_distribution": distribution
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_top_students(limit: int = 10) -> str:
    """Get top students by grade (default: 10 students)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT id, student_name, grade, email, enrollment_date
            FROM student_grades 
            ORDER BY grade DESC 
            LIMIT {limit}
        """)
        
        students = []
        for row in cursor.fetchall():
            students.append({
                "id": row["id"],
                "name": row["student_name"],
                "grade": row["grade"],
                "email": row["email"],
                "enrollment_date": row["enrollment_date"]
            })
        
        conn.close()
        return json.dumps({"top_students": students})
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def search_students(name: str = "", min_grade: float = None, max_grade: float = None) -> str:
    """Search students by name and/or grade range"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, student_name, grade, email, enrollment_date FROM student_grades WHERE 1=1"
        params = []
        
        if name:
            query += " AND student_name LIKE ?"
            params.append(f"%{name}%")
        
        if min_grade is not None:
            query += " AND grade >= ?"
            params.append(min_grade)
        
        if max_grade is not None:
            query += " AND grade <= ?"
            params.append(max_grade)
        
        query += " ORDER BY grade DESC"
        
        cursor.execute(query, params)
        
        students = []
        for row in cursor.fetchall():
            students.append({
                "id": row["id"],
                "name": row["student_name"],
                "grade": row["grade"],
                "email": row["email"],
                "enrollment_date": row["enrollment_date"]
            })
        
        conn.close()
        return json.dumps({"search_results": students, "count": len(students)})
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_student_by_id(student_id: int) -> str:
    """Get detailed information for a specific student by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, student_name, grade, email, enrollment_date, created_at
            FROM student_grades 
            WHERE id = ?
        """, (student_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            student = {
                "id": row["id"],
                "name": row["student_name"],
                "grade": row["grade"],
                "email": row["email"],
                "enrollment_date": row["enrollment_date"],
                "created_at": row["created_at"]
            }
            return json.dumps({"student": student})
        else:
            return json.dumps({"error": f"Student with ID {student_id} not found"})
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def add_student(name: str, grade: float, email: str = "", enrollment_date: str = "") -> str:
    """Add a new student to the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Generate email if not provided
        if not email:
            name_parts = name.lower().replace(" ", ".")
            cursor.execute("SELECT COUNT(*) as count FROM student_grades")
            count = cursor.fetchone()["count"] + 1
            email = f"{name_parts}{count}@university.edu"
        
        # Use current date if enrollment_date not provided
        if not enrollment_date:
            from datetime import datetime
            enrollment_date = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute("""
            INSERT INTO student_grades (student_name, grade, email, enrollment_date)
            VALUES (?, ?, ?, ?)
        """, (name, grade, email, enrollment_date))
        
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return json.dumps({
            "success": True,
            "student_id": student_id,
            "message": f"Student '{name}' added successfully with ID {student_id}"
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def update_student_grade(student_id: int, new_grade: float) -> str:
    """Update a student's grade"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if student exists
        cursor.execute("SELECT student_name FROM student_grades WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            conn.close()
            return json.dumps({"error": f"Student with ID {student_id} not found"})
        
        # Update grade
        cursor.execute("UPDATE student_grades SET grade = ? WHERE id = ?", (new_grade, student_id))
        conn.commit()
        conn.close()
        
        return json.dumps({
            "success": True,
            "message": f"Grade updated for {student['student_name']} (ID: {student_id}) to {new_grade}"
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_student(student_id: int) -> str:
    """Delete a student from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if student exists
        cursor.execute("SELECT student_name FROM student_grades WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            conn.close()
            return json.dumps({"error": f"Student with ID {student_id} not found"})
        
        # Delete student
        cursor.execute("DELETE FROM student_grades WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        
        return json.dumps({
            "success": True,
            "message": f"Student '{student['student_name']}' (ID: {student_id}) deleted successfully"
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_database_schema() -> str:
    """Get the database schema and table information"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get table schema
        cursor.execute("PRAGMA table_info(student_grades)")
        columns = []
        for row in cursor.fetchall():
            columns.append({
                "name": row["name"],
                "type": row["type"],
                "not_null": bool(row["notnull"]),
                "default": row["dflt_value"],
                "primary_key": bool(row["pk"])
            })
        
        # Get table stats
        cursor.execute("SELECT COUNT(*) as count FROM student_grades")
        total_count = cursor.fetchone()["count"]
        
        conn.close()
        
        return json.dumps({
            "table_name": "student_grades",
            "total_records": total_count,
            "columns": columns,
            "database_file": DB_FILE
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
def execute_custom_query(sql_query: str) -> str:
    """Execute a custom SQL query (SELECT statements only for safety)"""
    try:
        # Safety check - only allow SELECT statements
        if not sql_query.strip().upper().startswith("SELECT"):
            return json.dumps({"error": "Only SELECT queries are allowed for safety"})
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Fetch results
        results = []
        for row in cursor.fetchall():
            result = {}
            for i, col in enumerate(columns):
                result[col] = row[i]
            results.append(result)
        
        conn.close()
        
        return json.dumps({
            "query": sql_query,
            "columns": columns,
            "results": results,
            "row_count": len(results)
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    print("Starting Student Grades MCP Server...")
    print(f"Database file: {DB_FILE}")
    print("Available tools:")
    print("- get_student_count")
    print("- get_grade_statistics")
    print("- get_top_students")
    print("- search_students")
    print("- get_student_by_id")
    print("- add_student")
    print("- update_student_grade")
    print("- delete_student")
    print("- get_database_schema")
    print("- execute_custom_query")
    mcp.run()
