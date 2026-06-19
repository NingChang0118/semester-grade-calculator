import streamlit as st

from storage import load_courses
from streamlit_ui.styles import apply_custom_style
from streamlit_ui.components import (
    render_hero,
    show_course_items,
    show_course_summary
)
from streamlit_ui.pages import (
    create_course_page,
    delete_course_page,
    edit_course_page
)


st.set_page_config(
    page_title="學期成績計算器",
    page_icon="📘",
    layout="wide"
)


def load_courses_to_session() -> None:
    if "current_page" not in st.session_state:
        st.session_state.current_page = "查看課程"

    if "courses" not in st.session_state:
        st.session_state.courses = load_courses()

    if "new_items" not in st.session_state:
        st.session_state.new_items = []

    if "edit_items" not in st.session_state:
        st.session_state.edit_items = []

    if "editing_course_index" not in st.session_state:
        st.session_state.editing_course_index = None

    if "selected_course_index" not in st.session_state:
        st.session_state.selected_course_index = 0


def get_grouped_courses() -> dict:
    grouped_courses = {}

    for index, course in enumerate(st.session_state.courses):
        academic_year = course.academic_year
        semester = course.semester

        if academic_year not in grouped_courses:
            grouped_courses[academic_year] = {}

        if semester not in grouped_courses[academic_year]:
            grouped_courses[academic_year][semester] = []

        grouped_courses[academic_year][semester].append((index, course))

    return grouped_courses


def get_gpa_grouped_courses(courses: list) -> dict:
    grouped_courses = {}

    for course in courses:
        if course.credits <= 0:
            continue

        academic_year = course.academic_year
        semester = course.semester

        if academic_year == "未設定" and semester == "未設定":
            academic_year = "未分類"

        if academic_year not in grouped_courses:
            grouped_courses[academic_year] = {}

        if semester not in grouped_courses[academic_year]:
            grouped_courses[academic_year][semester] = []

        grouped_courses[academic_year][semester].append(course)

    return grouped_courses


def calculate_gpa(courses: list) -> tuple[float, float]:
    total_credits = 0.0
    total_weighted_grade_points = 0.0

    for course in courses:
        if course.credits <= 0:
            continue

        total_credits += course.credits
        total_weighted_grade_points += course.weighted_grade_points()

    if total_credits <= 0:
        return 0.0, 0.0

    return total_credits, total_weighted_grade_points / total_credits


def show_selected_course() -> None:
    courses = st.session_state.courses

    if not courses:
        st.info("目前沒有已儲存課程。請先新增一門課程。")
        return

    selected_index = st.session_state.selected_course_index

    if selected_index >= len(courses):
        selected_index = 0
        st.session_state.selected_course_index = 0

    course = courses[selected_index]

    st.header(course.name)
    st.caption(f"{course.academic_year}｜{course.semester}")

    with st.container(border=True):
        show_course_summary(course)
        show_course_items(course)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("編輯這門課程", use_container_width=True):
                st.session_state.current_page = "編輯課程"
                st.session_state.editing_course_index = selected_index
                st.rerun()

        with col2:
            if st.button("刪除這門課程", use_container_width=True):
                st.session_state.current_page = "刪除課程"
                st.rerun()


def show_gpa_summary_page() -> None:
    courses = st.session_state.courses

    st.header("GPA 統計")

    if not courses:
        st.info("目前沒有已儲存課程。")
        return

    total_credits, cumulative_gpa = calculate_gpa(courses)

    if total_credits <= 0:
        st.info("目前沒有可計算 GPA 的課程，請先設定課程學分。")
        return

    grouped_courses = get_gpa_grouped_courses(courses)

    academic_year_options = sorted(grouped_courses.keys())

    selected_academic_year = st.selectbox(
        "選擇學年",
        academic_year_options,
        key="gpa_academic_year_selector"
    )

    semester_options = sorted(grouped_courses[selected_academic_year].keys())

    selected_semester = st.selectbox(
        "選擇學期",
        semester_options,
        key="gpa_semester_selector"
    )

    semester_courses = grouped_courses[selected_academic_year][selected_semester]
    semester_credits, semester_gpa = calculate_gpa(semester_courses)

    st.divider()

    st.subheader(f"{selected_academic_year}｜{selected_semester}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("修課數量", len(semester_courses))

    with col2:
        st.metric("學期總學分", f"{semester_credits:.1f}")

    with col3:
        st.metric("學期 GPA", f"{semester_gpa:.2f}")

    course_rows = []

    for course in semester_courses:
        course_rows.append(
            {
                "科目": course.name,
                "學分": f"{course.credits:.1f}",
                "等第": course.letter_grade(),
                "GPA": f"{course.grade_point():.2f}"
            }
        )

    st.table(course_rows)

    st.divider()

    st.subheader("累積 GPA")

    col4, col5 = st.columns(2)

    with col4:
        st.metric("累積總學分", f"{total_credits:.1f}")

    with col5:
        st.metric("累積 GPA", f"{cumulative_gpa:.2f}")


def render_sidebar() -> None:
    with st.sidebar:
        st.title("查看成績")

        courses = st.session_state.courses

        if not courses:
            st.info("目前沒有已儲存課程。")
        else:
            grouped_courses = get_grouped_courses()

            for academic_year in sorted(grouped_courses.keys()):
                with st.expander(academic_year, expanded=False):
                    semesters = grouped_courses[academic_year]

                    for semester in sorted(semesters.keys()):
                        with st.expander(
                            semester,
                            expanded=False
                        ):
                            for index, course in semesters[semester]:
                                if st.button(
                                    course.name,
                                    key=f"sidebar_course_{index}",
                                    use_container_width=True
                                ):
                                    st.session_state.selected_course_index = index
                                    st.session_state.current_page = "查看課程"
                                    st.rerun()

        st.divider()

        if st.button("新增課程", use_container_width=True):
            st.session_state.current_page = "新增課程"
            st.rerun()

        if st.button("GPA 統計", use_container_width=True):
            st.session_state.current_page = "GPA 統計"
            st.rerun()


def main() -> None:
    apply_custom_style()
    load_courses_to_session()

    render_hero()
    render_sidebar()

    page = st.session_state.current_page

    if page == "查看課程":
        show_selected_course()

    elif page == "新增課程":
        create_course_page()

    elif page == "編輯課程":
        edit_course_page()

    elif page == "刪除課程":
        delete_course_page()

    elif page == "GPA 統計":
        show_gpa_summary_page()


if __name__ == "__main__":
    main()