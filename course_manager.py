from grade_calculator import Course, GradeItem
from storage import save_course, save_courses, load_courses


def show_loaded_courses() -> None:
    courses = load_courses()

    print(f"已載入 {len(courses)} 門課程。")

    if courses:
        print("目前課程：")

        for index, course in enumerate(courses, start=1):
            print(f"{index}. {course.name}")
    else:
        print("目前沒有已儲存課程。")


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


def add_course() -> None:
    course = create_course()

    if not course.is_weight_valid():
        print(
            f"錯誤：成績占比總和應為 100%，目前為 {course.total_weight():.2f}%"
        )
        return

    print(f"\n課程名稱：{course.name}")
    print(f"目前加權分數：{course.current_score():.2f}")
    print(f"剩餘占比：{course.remaining_weight():.2f}%")
    print(f"剩餘項目平均需要：{course.required_average_score():.2f} 分")
    print(f"提醒：{course.status_message()}")

    save_course(course)
    print("課程資料已儲存。")


def list_courses() -> None:
    courses = load_courses()

    if not courses:
        print("目前沒有已儲存課程。")
        return

    print("\n=== 已儲存課程 ===")

    for index, course in enumerate(courses, start=1):
        print(f"\n{index}. {course.name}")
        print(f"目標分數：{course.target_score}")
        print(f"目前加權分數：{course.current_score():.2f}")
        print(f"提醒：{course.status_message()}")


def delete_course() -> None:
    courses = load_courses()

    if not courses:
        print("目前沒有可刪除的課程。")
        return

    print("\n=== 刪除課程 ===")

    for index, course in enumerate(courses, start=1):
        print(f"{index}. {course.name}")

    choice = input("請輸入要刪除的課程編號：")

    if not choice.isdigit():
        print("無效輸入，請輸入數字。")
        return

    course_index = int(choice) - 1

    if course_index < 0 or course_index >= len(courses):
        print("無效編號，找不到該課程。")
        return

    deleted_course = courses.pop(course_index)
    save_courses(courses)

    print(f"已刪除課程：{deleted_course.name}")


def create_grade_item() -> GradeItem:
    name = input("項目名稱：")
    weight = float(input("占比（%）："))

    completed = input("是否已完成（y/n）：").lower() == "y"
    is_bonus = input("是否為加分項目（y/n）：").lower() == "y"

    score = None

    if completed:
        score = float(input("成績："))

    return GradeItem(
        name=name,
        weight=weight,
        score=score,
        completed=completed,
        is_bonus=is_bonus
    )


def show_course_items(course: Course) -> None:
    if not course.items:
        print("這門課目前沒有成績項目。")
        return

    print("\n=== 成績項目 ===")

    for index, item in enumerate(course.items, start=1):
        score_text = item.score if item.score is not None else "未填寫"
        completed_text = "已完成" if item.completed else "未完成"
        bonus_text = "加分項" if item.is_bonus else "一般項目"

        print(f"{index}. {item.name}")
        print(f"   占比：{item.weight}%")
        print(f"   成績：{score_text}")
        print(f"   狀態：{completed_text}")
        print(f"   類型：{bonus_text}")


def edit_course_items(course: Course) -> None:
    while True:
        show_course_items(course)

        print("\n=== 編輯成績項目 ===")
        print("1. 修改項目名稱")
        print("2. 修改占比")
        print("3. 修改成績")
        print("4. 切換完成狀態")
        print("5. 切換加分項目")
        print("6. 刪除項目")
        print("7. 新增項目")
        print("8. 返回")

        choice = input("請輸入選項：")

        if choice == "8":
            break

        if choice == "7":
            course.items.append(create_grade_item())
            print("成績項目已新增。")
            continue

        if not course.items:
            print("目前沒有可編輯的成績項目。")
            continue

        item_choice = input("請輸入成績項目編號：")

        if not item_choice.isdigit():
            print("無效輸入，請輸入數字。")
            continue

        item_index = int(item_choice) - 1

        if item_index < 0 or item_index >= len(course.items):
            print("無效編號，找不到該成績項目。")
            continue

        item = course.items[item_index]

        if choice == "1":
            item.name = input("請輸入新的項目名稱：")
            print("項目名稱已更新。")

        elif choice == "2":
            item.weight = float(input("請輸入新的占比（%）："))
            print("占比已更新。")

        elif choice == "3":
            item.score = float(input("請輸入新的成績："))
            item.completed = True
            print("成績已更新，狀態已設為已完成。")

        elif choice == "4":
            item.completed = not item.completed

            if not item.completed:
                item.score = None

            print("完成狀態已切換。")

        elif choice == "5":
            item.is_bonus = not item.is_bonus
            print("加分項目狀態已切換。")

        elif choice == "6":
            deleted_item = course.items.pop(item_index)
            print(f"已刪除成績項目：{deleted_item.name}")

        else:
            print("無效選項，請重新輸入。")


def edit_course() -> None:
    courses = load_courses()

    if not courses:
        print("目前沒有可編輯的課程。")
        return

    print("\n=== 編輯課程 ===")

    for index, course in enumerate(courses, start=1):
        print(f"{index}. {course.name}")

    choice = input("請輸入要編輯的課程編號：")

    if not choice.isdigit():
        print("無效輸入，請輸入數字。")
        return

    course_index = int(choice) - 1

    if course_index < 0 or course_index >= len(courses):
        print("無效編號，找不到該課程。")
        return

    course = courses[course_index]

    while True:
        print(f"\n=== 編輯課程：{course.name} ===")
        print("1. 修改課程名稱")
        print("2. 修改目標分數")
        print("3. 編輯成績項目")
        print("4. 儲存並返回")

        edit_choice = input("請輸入選項：")

        if edit_choice == "1":
            course.name = input("請輸入新的課程名稱：")
            print("課程名稱已更新。")

        elif edit_choice == "2":
            course.target_score = float(input("請輸入新的目標分數："))
            print("目標分數已更新。")

        elif edit_choice == "3":
            edit_course_items(course)

        elif edit_choice == "4":
            save_courses(courses)
            print("課程修改已儲存。")

            if not course.is_weight_valid():
                print(
                    f"提醒：目前一般成績項目占比總和為 {course.total_weight():.2f}%，不是 100%。"
                )

            break

        else:
            print("無效選項，請重新輸入。")


