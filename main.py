from grade_calculator import Course, GradeItem
from storage import save_course
import grade_calculator
print(grade_calculator.__file__)

def create_course() -> Course:
    course_name = input("請輸入課程名稱：")
    target_score = float(input("請輸入目標分數："))

    item_count = int(input("請輸入成績項目數量："))

    items = []

    for i in range(item_count):
        print(f"\n--- 成績項目 {i + 1} ---")

        name = input("項目名稱：")
        weight = float(input("占比（%）："))

        completed = input("是否已完成（y/n）：").lower() == "y"
        is_bonus = input("是否為加分項目（y/n）：").lower() == "y"

        score = None

        if completed:
            score = float(input("成績："))

        items.append(
            GradeItem(
                name=name,
                weight=weight,
                score=score,
                completed=completed,
                is_bonus=is_bonus
            )
        )

    return Course(
        name=course_name,
        target_score=target_score,
        items=items
    )


course = create_course()

if not course.is_weight_valid():
    print(f"錯誤：成績占比總和應為 100%，目前為 {course.total_weight():.2f}%")
else:
    print(f"\n課程名稱：{course.name}")
    print(f"目前加權分數：{course.current_score():.2f}")
    print(f"剩餘占比：{course.remaining_weight():.2f}%")
    print(f"剩餘項目平均需要：{course.required_average_score():.2f} 分")
    print(f"提醒：{course.status_message()}")

save_course(course)
print("課程資料已儲存。")