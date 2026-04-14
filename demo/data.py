from student import Student
from manager import StudentManager


def init_test_data(manager: StudentManager):
    """Initialize test data."""
    test_students = [
        Student(name="张三", age=18, gender="男", score=85.5),
        Student(name="李四", age=19, gender="女", score=92.0),
        Student(name="王五", age=20, gender="男", score=78.5),
        Student(name="赵六", age=18, gender="女", score=88.0),
        Student(name="钱七", age=21, gender="男", score=95.5),
    ]

    for student in test_students:
        manager.add_student(student)

    return len(test_students)