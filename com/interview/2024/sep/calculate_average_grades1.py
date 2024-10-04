from typing import List, Dict


def calculate_average(grades: List[float]) -> float:
    valid_grades = [grade for grade in grades if grade is not None]
    if not valid_grades:
        return 0
    return round(sum(valid_grades) / len(valid_grades), 2)


def calculate_average_grades(students: List[Dict], threshold: float) -> Dict:
    result = {}

    # Group students by class
    classes = {}
    for student in students:
        class_name = student['class']
        if class_name not in classes:
            classes[class_name] = []
        avg_grade = calculate_average(student['grades'])
        if avg_grade >= threshold:
            classes[class_name].append((student['name'], avg_grade))

    # Calculate per class averages and build the output dictionary
    for class_name, student_grades in classes.items():
        if student_grades:
            student_dict = {name: grade for name, grade in student_grades}
            class_average = round(sum(grade for _, grade in student_grades) / len(student_grades), 2)
            result[class_name] = {
                "students": student_dict,
                "class_average": class_average
            }

    return result


# Input data
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

# Output
print(calculate_average_grades(students, threshold))
