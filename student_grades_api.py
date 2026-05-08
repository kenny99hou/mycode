#!/usr/bin/env python3
"""
Student Grades Database API Server

This server provides REST API endpoints to interact with the student_grades 
SQLite database created by the test.py script.
"""

import sqlite3
import json
from typing import Any, List, Dict, Optional
from flask import Flask, request, jsonify

# Create Flask app
app = Flask("student_grades_api")

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

@app.route('/api/students/count', methods=['GET'])
def get_student_count():
    """Get the total number of students in the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM student_grades")
        result = cursor.fetchone()
        conn.close()
        return jsonify({"total_students": result["count"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/statistics', methods=['GET'])
def get_grade_statistics():
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
        
        return jsonify({
            "average_grade": round(stats["avg"], 2),
            "highest_grade": stats["max"],
            "lowest_grade": stats["min"],
            "median_grade": median,
            "grade_distribution": distribution
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/top', methods=['GET'])
def get_top_students():
    """Get top students by grade"""
    limit = request.args.get('limit', 10, type=int)
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
        return jsonify({"top_students": students})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/search', methods=['GET'])
def search_students():
    """Search students by name and/or grade range"""
    name = request.args.get('name', '')
    min_grade = request.args.get('min_grade', type=float)
    max_grade = request.args.get('max_grade', type=float)
    
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
        return jsonify({"search_results": students, "count": len(students)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student_by_id(student_id):
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
            return jsonify({"student": student})
        else:
            return jsonify({"error": f"Student with ID {student_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students', methods=['POST'])
def add_student():
    """Add a new student to the database"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'grade' not in data:
        return jsonify({"error": "Name and grade are required"}), 400
    
    name = data['name']
    grade = data['grade']
    email = data.get('email', '')
    enrollment_date = data.get('enrollment_date', '')
    
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
        
        return jsonify({
            "success": True,
            "student_id": student_id,
            "message": f"Student '{name}' added successfully with ID {student_id}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student_grade(student_id):
    """Update a student's grade"""
    data = request.get_json()
    
    if not data or 'grade' not in data:
        return jsonify({"error": "Grade is required"}), 400
    
    new_grade = data['grade']
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if student exists
        cursor.execute("SELECT student_name FROM student_grades WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            conn.close()
            return jsonify({"error": f"Student with ID {student_id} not found"}), 404
        
        # Update grade
        cursor.execute("UPDATE student_grades SET grade = ? WHERE id = ?", (new_grade, student_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": f"Grade updated for {student['student_name']} (ID: {student_id}) to {new_grade}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student from the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if student exists
        cursor.execute("SELECT student_name FROM student_grades WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if not student:
            conn.close()
            return jsonify({"error": f"Student with ID {student_id} not found"}), 404
        
        # Delete student
        cursor.execute("DELETE FROM student_grades WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": f"Student '{student['student_name']}' (ID: {student_id}) deleted successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/database/schema', methods=['GET'])
def get_database_schema():
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
        
        return jsonify({
            "table_name": "student_grades",
            "total_records": total_count,
            "columns": columns,
            "database_file": DB_FILE
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/database/query', methods=['POST'])
def execute_custom_query():
    """Execute a custom SQL query (SELECT statements only for safety)"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({"error": "SQL query is required"}), 400
    
    sql_query = data['query']
    
    try:
        # Safety check - only allow SELECT statements
        if not sql_query.strip().upper().startswith("SELECT"):
            return jsonify({"error": "Only SELECT queries are allowed for safety"}), 400
        
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
        
        return jsonify({
            "query": sql_query,
            "columns": columns,
            "results": results,
            "row_count": len(results)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/', methods=['GET'])
def api_info():
    """API information and available endpoints"""
    return jsonify({
        "name": "Student Grades API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/students/count": "Get total number of students",
            "GET /api/students/statistics": "Get grade statistics",
            "GET /api/students/top?limit=N": "Get top N students by grade",
            "GET /api/students/search?name=X&min_grade=Y&max_grade=Z": "Search students",
            "GET /api/students/{id}": "Get student by ID",
            "POST /api/students": "Add new student",
            "PUT /api/students/{id}": "Update student grade",
            "DELETE /api/students/{id}": "Delete student",
            "GET /api/database/schema": "Get database schema",
            "POST /api/database/query": "Execute custom SELECT query",
            "GET /api/health": "Health check"
        }
    })

if __name__ == "__main__":
    print("Starting Student Grades API Server...")
    print(f"Database file: {DB_FILE}")
    print("Available endpoints:")
    print("- GET /api/students/count")
    print("- GET /api/students/statistics")
    print("- GET /api/students/top?limit=N")
    print("- GET /api/students/search?name=X&min_grade=Y&max_grade=Z")
    print("- GET /api/students/{id}")
    print("- POST /api/students")
    print("- PUT /api/students/{id}")
    print("- DELETE /api/students/{id}")
    print("- GET /api/database/schema")
    print("- POST /api/database/query")
    print("- GET /api/health")
    print("- GET / (API info)")
    print("\nServer starting on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
