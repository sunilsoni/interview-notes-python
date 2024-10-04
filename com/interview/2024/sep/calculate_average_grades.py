from typing import Dict, List


def calculate_average_grades(students: List[Dict], threshold: float) -> Dict:
    # Dictionary to store class-wise student grades
    class_grades = {}

    for student in students:
        name = student['name']
        grades = [grade for grade in student['grades'] if grade is not None]
        class_name = student['class']

        # Calculate average grade for the student
        avg_grade = sum(grades) / len(grades) if grades else 0

        # Only include students with average grade above threshold
        if avg_grade >= threshold:
            if class_name not in class_grades:
                class_grades[class_name] = {}
            class_grades[class_name][name] = avg_grade

    # Calculate class averages
    for class_name, students in class_grades.items():
        class_avg = sum(students.values()) / len(students) if students else 0
        class_grades[class_name]['class_average'] = class_avg

    return class_grades


# Test the function
students = [
    {"name": "Alice", "grades": [85, 90, None, 78], "class": "Math"},
    {"name": "Bob", "grades": [80, 82, 84], "class": "Math"},
    {"name": "Charlie", "grades": [95, None, 92, 88], "class": "Science"},
    {"name": "David", "grades": [70, 75, None, 72], "class": "Science"},
    {"name": "Eve", "grades": [88, 90, 85], "class": "History"},
    {"name": "Frank", "grades": [92, 94, None, 89], "class": "History"},
    {"name": "Grace", "grades": [78, 85, 80], "class": "Art"},
    {"name": "Hannah", "grades": [85, 87, 90], "class": "Art"}
]

threshold = 80

result = calculate_average_grades(students, threshold)
print(result)
