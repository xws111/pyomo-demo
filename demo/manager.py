from typing import Optional
from student import Student


class StudentManager:
    def __init__(self):
        self.students: list[Student] = []

    def add_student(self, student: Student) -> bool:
        """Add a new student. Returns True if successful."""
        self.students.append(student)
        return True

    def remove_student(self, student_id: str) -> bool:
        """Remove a student by ID. Returns True if found and removed."""
        for i, s in enumerate(self.students):
            if s.student_id == student_id:
                self.students.pop(i)
                return True
        return False

    def update_student(self, student_id: str, **kwargs) -> bool:
        """Update student fields. Returns True if found and updated."""
        student = self.find_student(student_id)
        if student is None:
            return False

        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
        return True

    def find_student(self, student_id: str) -> Optional[Student]:
        """Find a student by ID. Returns None if not found."""
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def find_by_name(self, name: str) -> list[Student]:
        """Find students by name (partial match)."""
        return [s for s in self.students if name.lower() in s.name.lower()]

    def list_students(self, sort_by: str = "name") -> list[Student]:
        """List all students, optionally sorted by a field."""
        if sort_by == "name":
            return sorted(self.students, key=lambda s: s.name)
        elif sort_by == "age":
            return sorted(self.students, key=lambda s: s.age)
        elif sort_by == "score":
            return sorted(self.students, key=lambda s: s.score)
        elif sort_by == "student_id":
            return sorted(self.students, key=lambda s: s.student_id)
        return self.students

    def get_statistics(self) -> dict:
        """Get statistics about students."""
        if not self.students:
            return {
                "total": 0,
                "average_score": 0,
                "max_score": 0,
                "min_score": 0
            }

        scores = [s.score for s in self.students]
        return {
            "total": len(self.students),
            "average_score": sum(scores) / len(scores),
            "max_score": max(scores),
            "min_score": min(scores)
        }