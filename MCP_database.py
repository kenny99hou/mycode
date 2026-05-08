#!/usr/bin/env python3
"""
MCP-style Server for Student Grades Database with AI-Ready Data

This server provides tools to query the student_grades SQLite database 
and format the results for AI consumption and analysis.
"""

import sqlite3
import json
import sys
from typing import Any, List, Dict, Optional, Union
from datetime import datetime

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

def format_for_ai(data: Union[Dict, List], context: str = "") -> str:
    """Format database results for AI consumption"""
    if isinstance(data, list):
        if not data:
            return f"No data found{context}."
        
        # Format list of records
        formatted = f"Found {len(data)} records{context}:\n\n"
        for i, item in enumerate(data, 1):
            formatted += f"{i}. "
            if isinstance(item, dict):
                formatted += format_record_for_ai(item)
            else:
                formatted += str(item)
            formatted += "\n"
        return formatted
    elif isinstance(data, dict):
        return f"Record{context}:\n{format_record_for_ai(data)}"
    else:
        return f"Data{context}: {data}"

def format_record_for_ai(record: Dict) -> str:
    """Format a single record for AI consumption"""
    if 'student_name' in record:
        # Student record
        formatted = f"Student: {record.get('student_name', 'Unknown')}"
        if 'grade' in record:
            formatted += f", Grade: {record['grade']}"
        if 'email' in record:
            formatted += f", Email: {record['email']}"
        if 'enrollment_date' in record:
            formatted += f", Enrolled: {record['enrollment_date']}"
        if 'id' in record:
            formatted += f", ID: {record['id']}"
        return formatted
    else:
        # Generic record
        return ", ".join([f"{k}: {v}" for k, v in record.items()])

# MCP-style tools (functions that can be called by AI)

def get_student_summary() -> str:
    """Get comprehensive summary of all students for AI analysis"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get basic statistics
        cursor.execute("SELECT COUNT(*) as count FROM student_grades")
        total_students = cursor.fetchone()["count"]
        
        cursor.execute("SELECT AVG(grade) as avg, MAX(grade) as max, MIN(grade) as min FROM student_grades")
        stats = cursor.fetchone()
        
        # Get grade distribution
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
        distribution = cursor.fetchall()
        
        # Get top and bottom performers
        cursor.execute("SELECT student_name, grade FROM student_grades ORDER BY grade DESC LIMIT 5")
        top_students = cursor.fetchall()
        
        cursor.execute("SELECT student_name, grade FROM student_grades ORDER BY grade ASC LIMIT 5")
        bottom_students = cursor.fetchall()
        
        conn.close()
        
        # Format for AI
        summary = f"STUDENT DATABASE SUMMARY\n"
        summary += f"=====================\n\n"
        summary += f"Total Students: {total_students}\n"
        summary += f"Average Grade: {stats['avg']:.2f}\n"
        summary += f"Highest Grade: {stats['max']}\n"
        summary += f"Lowest Grade: {stats['min']}\n\n"
        
        summary += "Grade Distribution:\n"
        for row in distribution:
            summary += f"  {row['grade_range']}: {row['count']} students\n"
        
        summary += f"\nTop 5 Performers:\n"
        for i, student in enumerate(top_students, 1):
            summary += f"  {i}. {student['student_name']}: {student['grade']}\n"
        
        summary += f"\nBottom 5 Performers:\n"
        for i, student in enumerate(bottom_students, 1):
            summary += f"  {i}. {student['student_name']}: {student['grade']}\n"
        
        return summary
        
    except Exception as e:
        return f"Error getting student summary: {e}"

def get_students_by_criteria(name_filter: str = "", min_grade: float = None, max_grade: float = None, limit: int = 50) -> str:
    """Get students matching specific criteria, formatted for AI analysis"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT id, student_name, grade, email, enrollment_date FROM student_grades WHERE 1=1"
        params = []
        
        if name_filter:
            query += " AND student_name LIKE ?"
            params.append(f"%{name_filter}%")
        
        if min_grade is not None:
            query += " AND grade >= ?"
            params.append(min_grade)
        
        if max_grade is not None:
            query += " AND grade <= ?"
            params.append(max_grade)
        
        query += " ORDER BY grade DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        students = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        context = ""
        if name_filter:
            context += f" with name containing '{name_filter}'"
        if min_grade is not None or max_grade is not None:
            grade_range = ""
            if min_grade is not None:
                grade_range += f" >= {min_grade}"
            if max_grade is not None:
                if grade_range:
                    grade_range += f" and <= {max_grade}"
                else:
                    grade_range += f" <= {max_grade}"
            context += f" with grade{grade_range}"
        
        return format_for_ai(students, context)
        
    except Exception as e:
        return f"Error searching students: {e}"

def get_student_details(student_id: int) -> str:
    """Get detailed information about a specific student for AI analysis"""
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
            student = dict(row)
            
            # Get student's rank
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) + 1 as rank FROM student_grades WHERE grade > ?", (student['grade'],))
            rank = cursor.fetchone()["rank"]
            conn.close()
            
            details = f"STUDENT DETAILS\n"
            details += f"==============\n\n"
            details += format_record_for_ai(student)
            details += f"\nClass Rank: #{rank} out of total students"
            details += f"\nCreated: {student['created_at']}"
            
            return details
        else:
            return f"No student found with ID {student_id}"
            
    except Exception as e:
        return f"Error getting student details: {e}"

def get_grade_analysis() -> str:
    """Get detailed grade analysis for AI consumption"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Grade statistics
        cursor.execute("SELECT AVG(grade) as avg, MAX(grade) as max, MIN(grade) as min FROM student_grades")
        stats = cursor.fetchone()
        
        # Get all grades for percentile calculation
        cursor.execute("SELECT grade FROM student_grades ORDER BY grade")
        grades = [row["grade"] for row in cursor.fetchall()]
        
        # Calculate percentiles
        n = len(grades)
        p25 = grades[n//4] if n > 0 else 0
        p50 = grades[n//2] if n > 0 else 0  # Median
        p75 = grades[3*n//4] if n > 0 else 0
        p90 = grades[9*n//10] if n > 0 else 0
        
        # Grade ranges analysis
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN grade >= 95 THEN 'Excellent (95-100)'
                    WHEN grade >= 90 THEN 'Outstanding (90-94)'
                    WHEN grade >= 85 THEN 'Very Good (85-89)'
                    WHEN grade >= 80 THEN 'Good (80-84)'
                    WHEN grade >= 75 THEN 'Above Average (75-79)'
                    WHEN grade >= 70 THEN 'Average (70-74)'
                    WHEN grade >= 65 THEN 'Below Average (65-69)'
                    WHEN grade >= 60 THEN 'Poor (60-64)'
                    ELSE 'Failing (0-59)'
                END as performance_level,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM student_grades), 1) as percentage
            FROM student_grades 
            GROUP BY performance_level
            ORDER BY 
                CASE 
                    WHEN grade >= 95 THEN 1
                    WHEN grade >= 90 THEN 2
                    WHEN grade >= 85 THEN 3
                    WHEN grade >= 80 THEN 4
                    WHEN grade >= 75 THEN 5
                    WHEN grade >= 70 THEN 6
                    WHEN grade >= 65 THEN 7
                    WHEN grade >= 60 THEN 8
                    ELSE 9
                END
        """)
        performance = cursor.fetchall()
        
        conn.close()
        
        analysis = f"GRADE ANALYSIS REPORT\n"
        analysis += f"===================\n\n"
        analysis += f"Statistical Overview:\n"
        analysis += f"  Mean (Average): {stats['avg']:.2f}\n"
        analysis += f"  Median (50th percentile): {p50:.2f}\n"
        analysis += f"  25th percentile: {p25:.2f}\n"
        analysis += f"  75th percentile: {p75:.2f}\n"
        analysis += f"  90th percentile: {p90:.2f}\n"
        analysis += f"  Range: {stats['min']:.2f} - {stats['max']:.2f}\n\n"
        
        analysis += f"Performance Levels:\n"
        for row in performance:
            analysis += f"  {row['performance_level']}: {row['count']} students ({row['percentage']}%)\n"
        
        return analysis
        
    except Exception as e:
        return f"Error performing grade analysis: {e}"

def find_similar_students(target_grade: float, tolerance: float = 2.0, limit: int = 10) -> str:
    """Find students with similar grades for AI comparison analysis"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        min_grade = target_grade - tolerance
        max_grade = target_grade + tolerance
        
        cursor.execute("""
            SELECT student_name, grade, email, enrollment_date
            FROM student_grades 
            WHERE grade BETWEEN ? AND ?
            ORDER BY ABS(grade - ?), grade DESC
            LIMIT ?
        """, (min_grade, max_grade, target_grade, limit))
        
        students = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        if not students:
            return f"No students found with grades within ±{tolerance} of {target_grade}"
        
        result = f"STUDENTS WITH SIMILAR GRADES (±{tolerance} of {target_grade})\n"
        result += f"================================================\n\n"
        
        for i, student in enumerate(students, 1):
            diff = abs(student['grade'] - target_grade)
            result += f"{i}. {student['student_name']}: {student['grade']} (diff: {diff:.2f})\n"
        
        return result
        
    except Exception as e:
        return f"Error finding similar students: {e}"

def get_enrollment_trends() -> str:
    """Analyze enrollment trends for AI insights"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Enrollment by year
        cursor.execute("""
            SELECT 
                substr(enrollment_date, 1, 4) as year,
                COUNT(*) as count,
                AVG(grade) as avg_grade
            FROM student_grades 
            WHERE enrollment_date IS NOT NULL
            GROUP BY year
            ORDER BY year
        """)
        yearly_data = cursor.fetchall()
        
        # Enrollment by month
        cursor.execute("""
            SELECT 
                substr(enrollment_date, 6, 2) as month,
                COUNT(*) as count,
                AVG(grade) as avg_grade
            FROM student_grades 
            WHERE enrollment_date IS NOT NULL
            GROUP BY month
            ORDER BY month
        """)
        monthly_data = cursor.fetchall()
        
        conn.close()
        
        trends = f"ENROLLMENT TRENDS ANALYSIS\n"
        trends += f"========================\n\n"
        
        if yearly_data:
            trends += "By Year:\n"
            for row in yearly_data:
                trends += f"  {row['year']}: {row['count']} students (avg grade: {row['avg_grade']:.2f})\n"
        
        if monthly_data:
            trends += "\nBy Month (across all years):\n"
            month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            for row in monthly_data:
                month_name = month_names[int(row['month'])] if row['month'].isdigit() else row['month']
                trends += f"  {month_name}: {row['count']} students (avg grade: {row['avg_grade']:.2f})\n"
        
        return trends
        
    except Exception as e:
        return f"Error analyzing enrollment trends: {e}"

def execute_ai_query(question: str) -> str:
    """Execute a natural language query about the student data"""
    try:
        # This is a simplified version - in a real implementation, 
        # you might use NLP to parse the question
        question_lower = question.lower()
        
        if "how many" in question_lower or "count" in question_lower or "total" in question_lower:
            return get_student_summary()
        elif "average" in question_lower or "mean" in question_lower:
            return get_grade_analysis()
        elif "top" in question_lower or "best" in question_lower or "highest" in question_lower:
            return get_students_by_criteria(limit=10)
        elif "bottom" in question_lower or "worst" in question_lower or "lowest" in question_lower:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT student_name, grade FROM student_grades ORDER BY grade ASC LIMIT 10")
            students = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return format_for_ai(students, " (lowest performers)")
        elif "enrollment" in question_lower or "trend" in question_lower:
            return get_enrollment_trends()
        else:
            return "I can help you analyze student data. Try asking about:\n- Total number of students\n- Average grades\n- Top/bottom performers\n- Grade distribution\n- Enrollment trends"
            
    except Exception as e:
        return f"Error processing query: {e}"

# MCP Server Interface
class MCPDatabaseServer:
    """MCP-style server for student grades database"""
    
    def __init__(self):
        self.tools = {
            "get_student_summary": get_student_summary,
            "get_students_by_criteria": get_students_by_criteria,
            "get_student_details": get_student_details,
            "get_grade_analysis": get_grade_analysis,
            "find_similar_students": find_similar_students,
            "get_enrollment_trends": get_enrollment_trends,
            "execute_ai_query": execute_ai_query
        }
    
    def list_tools(self):
        """List all available tools"""
        return list(self.tools.keys())
    
    def call_tool(self, tool_name: str, **kwargs):
        """Call a specific tool with arguments"""
        if tool_name not in self.tools:
            return f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
        
        try:
            return self.tools[tool_name](**kwargs)
        except Exception as e:
            return f"Error calling tool '{tool_name}': {e}"

def main():
    """Main function for interactive testing"""
    print("Student Grades MCP Server")
    print("========================")
    print("Available tools for AI analysis:")
    for tool in MCPDatabaseServer().list_tools():
        print(f"  - {tool}")
    print()
    
    # Interactive mode
    server = MCPDatabaseServer()
    
    while True:
        try:
            command = input("\nEnter command (tool_name [args]) or 'quit': ").strip()
            if command.lower() == 'quit':
                break
            
            if not command:
                continue
            
            # Parse command
            parts = command.split()
            tool_name = parts[0]
            
            # Simple argument parsing (for demonstration)
            kwargs = {}
            if len(parts) > 1:
                if tool_name == "get_student_details":
                    kwargs["student_id"] = int(parts[1])
                elif tool_name == "find_similar_students":
                    kwargs["target_grade"] = float(parts[1])
                elif tool_name == "execute_ai_query":
                    kwargs["question"] = " ".join(parts[1:])
            
            result = server.call_tool(tool_name, **kwargs)
            print(f"\nResult:\n{result}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()