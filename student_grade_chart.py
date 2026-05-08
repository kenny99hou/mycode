#!/usr/bin/env python3
"""
Student Grade Bell Chart Generator

This script creates a bell curve (normal distribution) visualization
for all student grades in the database.
"""

import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import matplotlib.patches as patches

def get_all_grades():
    """Get all grades from the database"""
    try:
        conn = sqlite3.connect('student_grades.db')
        cursor = conn.cursor()
        cursor.execute("SELECT grade FROM student_grades ORDER BY grade")
        grades = [row[0] for row in cursor.fetchall()]
        conn.close()
        return grades
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def create_bell_chart(grades):
    """Create a bell chart visualization of student grades"""
    
    if not grades:
        print("No grades found in database")
        return
    
    # Calculate statistics
    mean_grade = np.mean(grades)
    std_grade = np.std(grades)
    median_grade = np.median(grades)
    
    print(f"Grade Statistics:")
    print(f"  Mean: {mean_grade:.2f}")
    print(f"  Median: {median_grade:.2f}")
    print(f"  Std Dev: {std_grade:.2f}")
    print(f"  Min: {min(grades):.2f}")
    print(f"  Max: {max(grades):.2f}")
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Histogram with normal distribution overlay
    ax1.hist(grades, bins=20, density=True, alpha=0.7, color='skyblue', 
             edgecolor='black', label='Actual Grades')
    
    # Generate normal distribution curve
    x = np.linspace(min(grades) - 5, max(grades) + 5, 100)
    normal_curve = stats.norm.pdf(x, mean_grade, std_grade)
    ax1.plot(x, normal_curve, 'r-', linewidth=2, label='Normal Distribution')
    
    # Add vertical lines for mean and median
    ax1.axvline(mean_grade, color='red', linestyle='--', alpha=0.8, label=f'Mean: {mean_grade:.2f}')
    ax1.axvline(median_grade, color='green', linestyle='--', alpha=0.8, label=f'Median: {median_grade:.2f}')
    
    # Add standard deviation lines
    ax1.axvline(mean_grade - std_grade, color='orange', linestyle=':', alpha=0.6, label=f'-1σ: {mean_grade - std_grade:.2f}')
    ax1.axvline(mean_grade + std_grade, color='orange', linestyle=':', alpha=0.6, label=f'+1σ: {mean_grade + std_grade:.2f}')
    
    ax1.set_xlabel('Grade')
    ax1.set_ylabel('Density')
    ax1.set_title('Grade Distribution with Normal Curve Overlay')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Q-Q plot to check normality
    stats.probplot(grades, dist="norm", plot=ax2)
    ax2.set_title('Q-Q Plot (Normality Check)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def create_grade_distribution_analysis(grades):
    """Create detailed grade distribution analysis"""
    
    # Grade categories
    grade_ranges = [
        (90, 100, 'A (90-100)'),
        (80, 89, 'B (80-89)'),
        (70, 79, 'C (70-79)'),
        (60, 69, 'D (60-69)'),
        (0, 59, 'F (0-59)')
    ]
    
    # Count students in each range
    distribution = []
    for min_grade, max_grade, label in grade_ranges:
        count = len([g for g in grades if min_grade <= g <= max_grade])
        percentage = (count / len(grades)) * 100
        distribution.append((label, count, percentage))
    
    # Create pie chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Pie chart
    labels = [d[0] for d in distribution]
    sizes = [d[1] for d in distribution]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                       startangle=90, textprops={'fontsize': 10})
    ax1.set_title('Grade Distribution Pie Chart')
    
    # Bar chart
    bars = ax2.bar(labels, sizes, color=colors, alpha=0.8, edgecolor='black')
    ax2.set_xlabel('Grade Range')
    ax2.set_ylabel('Number of Students')
    ax2.set_title('Grade Distribution Bar Chart')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, size in zip(bars, sizes):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{size}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Print distribution table
    print("\nGrade Distribution Table:")
    print("=" * 40)
    print(f"{'Grade Range':<15} {'Count':<8} {'Percentage':<12}")
    print("-" * 40)
    for label, count, percentage in distribution:
        print(f"{label:<15} {count:<8} {percentage:<12.1f}%")
    print("=" * 40)

def create_statistical_summary(grades):
    """Create statistical summary visualization"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Box plot
    ax1.boxplot(grades, vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue', alpha=0.8))
    ax1.set_ylabel('Grade')
    ax1.set_title('Grade Box Plot')
    ax1.grid(True, alpha=0.3)
    
    # Add statistics text
    stats_text = f"""
    Statistics:
    Mean: {np.mean(grades):.2f}
    Median: {np.median(grades):.2f}
    Std Dev: {np.std(grades):.2f}
    Min: {min(grades):.2f}
    Max: {max(grades):.2f}
    Q1: {np.percentile(grades, 25):.2f}
    Q3: {np.percentile(grades, 75):.2f}
    """
    ax1.text(1.1, 0.5, stats_text, transform=ax1.transAxes, 
             fontsize=10, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Cumulative distribution
    sorted_grades = np.sort(grades)
    cumulative = np.arange(1, len(sorted_grades) + 1) / len(sorted_grades)
    ax2.plot(sorted_grades, cumulative, linewidth=2, color='blue')
    ax2.set_xlabel('Grade')
    ax2.set_ylabel('Cumulative Probability')
    ax2.set_title('Cumulative Distribution Function')
    ax2.grid(True, alpha=0.3)
    
    # Violin plot
    ax3.violinplot(grades, vert=True, positions=[1], showmeans=True, showmedians=True)
    ax3.set_ylabel('Grade')
    ax3.set_title('Grade Violin Plot')
    ax3.set_xticks([1])
    ax3.set_xticklabels(['All Grades'])
    ax3.grid(True, alpha=0.3)
    
    # Histogram with KDE
    ax4.hist(grades, bins=15, density=True, alpha=0.7, color='lightgreen', 
             edgecolor='black', label='Histogram')
    
    # Add KDE curve
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(grades)
    x_range = np.linspace(min(grades) - 5, max(grades) + 5, 100)
    ax4.plot(x_range, kde(x_range), 'r-', linewidth=2, label='KDE Curve')
    
    ax4.set_xlabel('Grade')
    ax4.set_ylabel('Density')
    ax4.set_title('Histogram with Kernel Density Estimation')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def main():
    """Main function to generate all visualizations"""
    print("Student Grade Bell Chart Generator")
    print("=" * 40)
    
    # Get grades from database
    grades = get_all_grades()
    
    if not grades:
        print("No grades found. Please run 'python3 test.py' first to create the database.")
        return
    
    print(f"Found {len(grades)} grades in database")
    
    # Create visualizations
    print("\n1. Creating Bell Chart with Normal Distribution...")
    create_bell_chart(grades)
    
    print("\n2. Creating Grade Distribution Analysis...")
    create_grade_distribution_analysis(grades)
    
    print("\n3. Creating Statistical Summary...")
    create_statistical_summary(grades)
    
    print("\nAll visualizations complete!")

if __name__ == "__main__":
    main()