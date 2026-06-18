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


def render_sidebar() -> None:
    with st.sidebar:
        st.title("查看成績")

        courses = st.session_state.courses

        if not courses:
            st.info("目前沒有已儲存課程。")
        else:
            grouped_courses = get_grouped_courses()

            for academic_year in sorted(grouped_courses.keys()):
                with st.expander(academic_year, expanded=True):
                    semesters = grouped_courses[academic_year]

                    for semester in sorted(semesters.keys()):
                        st.markdown(f"**{semester}**")

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


if __name__ == "__main__":
    main()