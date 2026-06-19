import json
from pathlib import Path

from grade_calculator import Course, GradeItem


DATA_FILE = Path("data/courses.json")


def course_to_dict(course: Course) -> dict:
    return {
        "name": course.name,
        "target_score": course.target_score,
        "academic_year": course.academic_year,
        "semester": course.semester,
        "credits": course.credits,
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


def dict_to_course(course_data: dict) -> Course:
    items = []

    for item_data in course_data["items"]:
        items.append(GradeItem(**item_data))

    return Course(
        name=course_data["name"],
        target_score=course_data["target_score"],
        items=items,
        academic_year=course_data.get("academic_year", "未設定"),
        semester=course_data.get("semester", "未設定"),
        credits=course_data.get("credits", 0.0)
    )


def load_courses() -> list[Course]:
    if not DATA_FILE.exists():
        return []

    if DATA_FILE.stat().st_size == 0:
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        courses_data = json.load(file)

    courses = []

    for course_data in courses_data:
        courses.append(dict_to_course(course_data))

    return courses


def save_courses(courses: list[Course]) -> None:
    DATA_FILE.parent.mkdir(exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            [course_to_dict(course) for course in courses],
            file,
            ensure_ascii=False,
            indent=4
        )


def save_course(course: Course) -> None:
    courses = load_courses()
    courses.append(course)
    save_courses(courses)