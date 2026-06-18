from dataclasses import dataclass


@dataclass
class GradeItem:
    name: str
    weight: float
    score: float | None = None
    completed: bool = False
    is_bonus: bool = False


@dataclass
class Course:
    name: str
    target_score: float
    items: list[GradeItem]

    def total_weight(self) -> float:
        total = 0.0

        for item in self.items:
            if not item.is_bonus:
                total += item.weight

        return total

    def current_score(self) -> float:
        total = 0.0

        for item in self.items:
            if item.completed and item.score is not None:
                total += item.score * (item.weight / 100)

        return total

    def remaining_weight(self) -> float:
        remaining = 0.0

        for item in self.items:
            if not item.completed and not item.is_bonus:
                remaining += item.weight

        return remaining
    
    def required_average_score(self) -> float:
        current = self.current_score()
        remaining = self.remaining_weight()

        if remaining <= 0:
            return 0.0

        required = (self.target_score - current) / (remaining / 100)

        return required