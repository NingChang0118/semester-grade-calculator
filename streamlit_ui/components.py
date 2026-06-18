import streamlit as st

from grade_calculator import Course, GradeItem


def render_hero() -> None:
    st.markdown(
        """
        <div class="app-hero">
            <h1>📘 學期成績計算器</h1>
            <p>管理多門課程、追蹤目前成績，快速估算剩餘項目需要多少分。</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_course_summary(course: Course) -> None:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("目標分數", f"{course.target_score:.2f}")
    col2.metric("目前加權分數", f"{course.current_score():.2f}")
    col3.metric("總占比", f"{course.total_weight():.2f}%")
    col4.metric("剩餘占比", f"{course.remaining_weight():.2f}%")

    st.metric(
        "剩餘項目平均需要",
        f"{course.required_average_score():.2f} 分"
    )

    st.info(course.status_message())

    if not course.is_weight_valid():
        st.warning(
            f"提醒：目前一般成績項目占比總和為 {course.total_weight():.2f}%，不是 100%。"
        )


def get_course_items_table(course: Course) -> list[dict]:
    rows = []

    for index, item in enumerate(course.items, start=1):
        score_text = "未填寫"

        if item.score is not None:
            score_text = f"{item.score:.2f}"

        rows.append(
            {
                "編號": index,
                "項目名稱": item.name,
                "占比": f"{item.weight:.2f}%",
                "成績": score_text,
                "狀態": "已完成" if item.completed else "未完成",
                "類型": "加分項" if item.is_bonus else "一般項目"
            }
        )

    return rows


def show_course_items(course: Course) -> None:
    st.subheader("成績項目")

    if not course.items:
        st.write("這門課目前沒有成績項目。")
        return

    st.table(get_course_items_table(course))


def add_item_to_session(session_key: str) -> None:
    st.session_state[session_key].append(
        {
            "name": "",
            "weight": 0.0,
            "score": None,
            "completed": False,
            "is_bonus": False
        }
    )


def render_items_editor(session_key: str, key_prefix: str) -> None:
    if st.button("＋ 新增成績項目", key=f"{key_prefix}_add_item"):
        add_item_to_session(session_key)
        st.rerun()

    for index, item_data in enumerate(st.session_state[session_key]):
        with st.container(border=True):
            st.markdown(f"#### 成績項目 {index + 1}")

            col1, col2 = st.columns([2, 1])

            with col1:
                item_data["name"] = st.text_input(
                    "項目名稱",
                    value=item_data["name"],
                    key=f"{key_prefix}_item_name_{index}"
                )

            with col2:
                item_data["weight"] = st.number_input(
                    "占比（%）",
                    min_value=0.0,
                    value=float(item_data["weight"]),
                    step=1.0,
                    key=f"{key_prefix}_item_weight_{index}"
                )

            col3, col4, col5 = st.columns([1, 1, 1])

            with col3:
                item_data["completed"] = st.checkbox(
                    "已完成",
                    value=item_data["completed"],
                    key=f"{key_prefix}_item_completed_{index}"
                )

            with col4:
                item_data["is_bonus"] = st.checkbox(
                    "加分項目",
                    value=item_data["is_bonus"],
                    key=f"{key_prefix}_item_bonus_{index}"
                )

            with col5:
                if item_data["completed"]:
                    item_data["score"] = st.number_input(
                        "成績",
                        min_value=0.0,
                        max_value=100.0,
                        value=0.0 if item_data["score"] is None else float(item_data["score"]),
                        step=1.0,
                        key=f"{key_prefix}_item_score_{index}"
                    )
                else:
                    item_data["score"] = None
                    st.text_input(
                        "成績",
                        value="未完成",
                        disabled=True,
                        key=f"{key_prefix}_item_score_disabled_{index}"
                    )

            if st.button("刪除此項目", key=f"{key_prefix}_delete_item_{index}"):
                st.session_state[session_key].pop(index)
                st.rerun()