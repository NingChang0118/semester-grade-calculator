import json
from pathlib import Path

from grade_calculator import Course, GradeItem


DATA_FILE = Path("data/courses.json")


def course_to_dict(course: Course) -> dict:
    return {
        "name": course.name,
        "target_score": course.target_score,
        "items": [
            {
                "name": item.name,
                "weight": item.weight,
                "score": item.score,
                "completed": item.completed,
                "is_bonus": item.is_bonus
            }
            for item in course.items
        ]
    }


def save_course(course: Course) -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)

    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as file:
            courses = json.load(file)
    else:
        courses = []

    courses.append(course_to_dict(course))

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(courses, file, ensure_ascii=False, indent=4)