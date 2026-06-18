from dataclasses import dataclass


@dataclass
class GradeItem:
    name: str
    weight: float
    score: float | None = None
    completed: bool = False


@dataclass
class Course:
    name: str
    target_score: float
    items: list[GradeItem]