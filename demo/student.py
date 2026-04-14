from dataclasses import dataclass
from typing import Optional
import random


def generate_id() -> str:
    """Generate a unique student ID."""
    return f"S{str(random.randint(1000, 9999))}"


@dataclass
class Student:
    name: str
    age: int
    gender: str
    score: float
    student_id: Optional[str] = None

    def __post_init__(self):
        if self.student_id is None:
            self.student_id = generate_id()