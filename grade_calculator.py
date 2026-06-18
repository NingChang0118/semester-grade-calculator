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

    def current_score(self) -> float:
        total = 0.0

        for item in self.items:
            if item.completed and item.score is not None:
                total += item.score * (item.weight / 100)

        return total

    def remaining_weight(self) -> float:
        remaining = 0.0

        for item in self.items:
            if not item.completed:
                remaining += item.weight

        return remaining