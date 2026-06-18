from course_manager import (
    add_course,
    delete_course,
    edit_course,
    list_courses,
    show_loaded_courses
)


def main() -> None:
    show_loaded_courses()

    while True:
        print("\n=== 學期成績計算器 ===")
        print("1. 查看課程")
        print("2. 新增課程")
        print("3. 編輯課程")
        print("4. 刪除課程")
        print("5. 離開程式")

        choice = input("請輸入選項：")

        if choice == "1":
            list_courses()

        elif choice == "2":
            add_course()

        elif choice == "3":
            edit_course()

        elif choice == "4":
            delete_course()

        elif choice == "5":
            print("感謝使用！")
            break

        else:
            print("無效選項，請重新輸入。")


if __name__ == "__main__":
    main()