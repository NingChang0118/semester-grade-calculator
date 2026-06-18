from grade_calculator import Course, GradeItem

course = Course(
    name="資料結構",
    target_score=60,
    items=[
        GradeItem("作業", 30, 85, True),
        GradeItem("期中考", 30, 70, True),
        GradeItem("期末考", 40)
    ]
)

print(f"課程名稱：{course.name}")
print(f"目前加權分數：{course.current_score():.2f}")
print(f"剩餘占比：{course.remaining_weight():.2f}%")
print(f"剩餘項目平均需要：{course.required_average_score():.2f} 分")
print(f"目前狀態：{course.grade_status()}")