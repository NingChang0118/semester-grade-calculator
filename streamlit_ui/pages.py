import streamlit as st

from grade_calculator import Course, GradeItem
from storage import save_courses
from streamlit_ui.components import (
    render_items_editor,
    show_course_items,
    show_course_summary
)


def grade_item_to_dict(item: GradeItem) -> dict:
    return {
        "name": item.name,
        "weight": item.weight,
        "score": item.score,
        "completed": item.completed,
        "is_bonus": item.is_bonus
    }


def dict_to_grade_item(item_data: dict) -> GradeItem:
    score = item_data["score"]

    if not item_data["completed"]:
        score = None

    return GradeItem(
        name=item_data["name"],
        weight=item_data["weight"],
        score=score,
        completed=item_data["completed"],
        is_bonus=item_data["is_bonus"]
    )


def build_grade_items(session_key: str) -> list[GradeItem]:
    items = []

    for item_data in st.session_state[session_key]:
        items.append(dict_to_grade_item(item_data))

    return items


def validate_course(course: Course) -> bool:
    if course.name.strip() == "":
        st.error("課程名稱不能空白。")
        return False

    if course.academic_year.strip() == "":
        st.error("學年不能空白。")
        return False

    if course.semester.strip() == "":
        st.error("學期不能空白。")
        return False

    if course.credits < 0:
        st.error("學分不能小於 0。")
        return False

    if not course.items:
        st.error("至少需要新增一個成績項目。")
        return False

    for item in course.items:
        if item.name.strip() == "":
            st.error("成績項目名稱不能空白。")
            return False

    if not course.is_weight_valid():
        st.error(
            f"成績占比總和應為 100%，目前為 {course.total_weight():.2f}%。"
        )
        return False

    return True


def show_courses_page() -> None:
    st.header("查看課程")
    st.caption("查看已儲存課程的目前分數、剩餘占比與成績項目。")

    courses = st.session_state.courses

    if not courses:
        st.info("目前沒有已儲存課程。請先新增一門課程。")
        return

    for index, course in enumerate(courses, start=1):
        with st.expander(
            f"{index}. {course.name}｜{course.academic_year}｜{course.semester}",
            expanded=False
        ):
            show_course_summary(course)
            show_course_items(course)


def create_course_page() -> None:
    st.header("新增課程")
    st.caption("建立一門課程，輸入學年、學期、學分、目標分數與各項成績占比。")

    with st.container(border=True):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            course_name = st.text_input("課程名稱", key="new_course_name")

        with col2:
            target_score = st.number_input(
                "目標分數",
                min_value=0.0,
                max_value=100.0,
                value=60.0,
                step=1.0,
                key="new_target_score"
            )

        with col3:
            credits = st.number_input(
                "學分",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key="new_credits"
            )

        col4, col5 = st.columns(2)

        with col4:
            academic_year = st.text_input(
                "學年",
                value="未設定",
                key="new_academic_year"
            )

        with col5:
            semester = st.selectbox(
                "學期",
                ["未設定", "第一學期", "第二學期", "暑修"],
                key="new_semester"
            )

    st.subheader("成績項目")
    render_items_editor("new_items", "new")

    items = build_grade_items("new_items")

    preview_course = Course(
        name=course_name,
        target_score=target_score,
        items=items,
        academic_year=academic_year,
        semester=semester,
        credits=credits
    )

    st.subheader("即時計算結果")
    show_course_summary(preview_course)

    if st.button("儲存課程", type="primary"):
        if not validate_course(preview_course):
            return

        st.session_state.courses.append(preview_course)
        save_courses(st.session_state.courses)

        st.session_state.new_items = []
        st.session_state.current_page = "查看課程"
        st.session_state.selected_course_index = len(st.session_state.courses) - 1

        st.success("課程資料已儲存。")
        st.rerun()


def edit_course_page() -> None:
    st.header("編輯課程")
    st.caption("修改課程名稱、學年、學期、學分、目標分數或成績項目。")

    courses = st.session_state.courses

    if not courses:
        st.info("目前沒有可編輯的課程。")
        return

    course_options = [
        f"{index + 1}. {course.name}｜{course.academic_year}｜{course.semester}"
        for index, course in enumerate(courses)
    ]

    default_index = 0

    if st.session_state.editing_course_index is not None:
        default_index = st.session_state.editing_course_index

    if default_index < 0 or default_index >= len(course_options):
        default_index = 0

    selected_course_label = st.selectbox(
        "請選擇要編輯的課程",
        course_options,
        index=default_index,
        key="edit_course_selector"
    )

    selected_index = course_options.index(selected_course_label)

    if (
        st.session_state.editing_course_index != selected_index
        or not st.session_state.edit_items
    ):
        selected_course = courses[selected_index]
        st.session_state.editing_course_index = selected_index
        st.session_state.edit_items = [
            grade_item_to_dict(item)
            for item in selected_course.items
        ]

    course = courses[selected_index]

    with st.container(border=True):
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            course_name = st.text_input(
                "課程名稱",
                value=course.name,
                key=f"edit_course_name_{selected_index}"
            )

        with col2:
            target_score = st.number_input(
                "目標分數",
                min_value=0.0,
                max_value=100.0,
                value=float(course.target_score),
                step=1.0,
                key=f"edit_target_score_{selected_index}"
            )

        with col3:
            credits = st.number_input(
                "學分",
                min_value=0.0,
                value=float(course.credits),
                step=1.0,
                key=f"edit_credits_{selected_index}"
            )

        col4, col5 = st.columns(2)

        with col4:
            academic_year = st.text_input(
                "學年",
                value=course.academic_year,
                key=f"edit_academic_year_{selected_index}"
            )

        with col5:
            semester_options = ["未設定", "第一學期", "第二學期", "暑修"]

            if course.semester in semester_options:
                semester_index = semester_options.index(course.semester)
            else:
                semester_index = 0

            semester = st.selectbox(
                "學期",
                semester_options,
                index=semester_index,
                key=f"edit_semester_{selected_index}"
            )

    st.subheader("成績項目")

    render_items_editor(
        "edit_items",
        f"edit_{selected_index}"
    )

    items = build_grade_items("edit_items")

    preview_course = Course(
        name=course_name,
        target_score=target_score,
        items=items,
        academic_year=academic_year,
        semester=semester,
        credits=credits
    )

    st.subheader("修改後預覽")
    show_course_summary(preview_course)

    if st.button("儲存修改", type="primary", key=f"save_edit_course_{selected_index}"):
        if not validate_course(preview_course):
            return

        st.session_state.courses[selected_index] = preview_course
        save_courses(st.session_state.courses)

        st.session_state.current_page = "查看課程"
        st.session_state.selected_course_index = selected_index
        st.session_state.editing_course_index = None
        st.session_state.edit_items = []

        st.success("課程修改已儲存。")
        st.rerun()


def delete_course_page() -> None:
    st.header("刪除課程")
    st.caption("刪除後會直接更新本機 JSON 資料。")

    courses = st.session_state.courses

    if not courses:
        st.info("目前沒有可刪除的課程。")
        return

    course_options = [
        f"{index + 1}. {course.name}｜{course.academic_year}｜{course.semester}"
        for index, course in enumerate(courses)
    ]

    selected_course_label = st.selectbox(
        "請選擇要刪除的課程",
        course_options,
        key="delete_course_selector"
    )

    selected_index = course_options.index(selected_course_label)
    selected_course = courses[selected_index]

    st.markdown(
        f"""
        <div class="danger-box">
            你即將刪除課程：<strong>{selected_course.name}</strong><br>
            學年：<strong>{selected_course.academic_year}</strong><br>
            學期：<strong>{selected_course.semester}</strong><br>
            這個操作會從 data/courses.json 移除資料。
        </div>
        """,
        unsafe_allow_html=True
    )

    confirm_delete = st.checkbox("我確認要刪除此課程")

    if st.button("刪除課程", type="primary"):
        if not confirm_delete:
            st.error("請先勾選確認刪除。")
            return

        deleted_course = st.session_state.courses.pop(selected_index)
        save_courses(st.session_state.courses)

        st.session_state.current_page = "查看課程"
        st.session_state.editing_course_index = None
        st.session_state.edit_items = []

        if st.session_state.selected_course_index >= len(st.session_state.courses):
            st.session_state.selected_course_index = 0

        st.success(f"已刪除課程：{deleted_course.name}")
        st.rerun()