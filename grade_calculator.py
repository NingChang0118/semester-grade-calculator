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
    
    def grade_status(self) -> str:
        required = self.required_average_score()

        if self.current_score() >= self.target_score:
            return "achieved"

        if self.remaining_weight() <= 0:
            return "failed"

        if required > 100:
            return "impossible"

        if required >= 80:
            return "danger"

        return "possible"
    
    def status_message(self) -> str:
        status = self.grade_status()

        if status == "achieved":
            return "恭喜！你已經達成目標分數。"

        if status == "failed":
            return "所有成績項目已完成，但尚未達成目標分數。"

        if status == "impossible":
            return "剩餘項目所需分數超過 100 分，目前無法達成目標。"

        if status == "danger":
            return "仍有機會達成目標，但剩餘項目需要較高分數。"

        return "目前進度正常，持續努力即可達成目標。"

