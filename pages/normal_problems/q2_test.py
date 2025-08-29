import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement

MAX_ATTEMPTS_MAIN = 3


def present_quiz(tab_name: str, max_attempts: int) -> str:
    header_animation()
    st.header("Q2 - Test", divider="rainbow")

    st.write("Question 2: 次の法則に当てはまるアイコンはどれ？")
    st.write(f"回答回数の上限は {max_attempts}回です。")

    # 画像ファイルのパス
    image_paths_q = [
        "pages/normal_problems/resources/q2_test/q2_icon_01.png",
        "pages/normal_problems/resources/q2_test/q2_icon_02.png",
        "pages/normal_problems/resources/q2_test/q2_icon_13.png",
        "pages/normal_problems/resources/q2_test/q2_icon_03.png",
        "pages/normal_problems/resources/q2_test/q2_icon_04.png"
    ]

    # 画像ファイルのパス
    image_paths_a = [
        "pages/normal_problems/resources/q2_test/q2_icon_05.png",
        "pages/normal_problems/resources/q2_test/q2_icon_06.png",
        "pages/normal_problems/resources/q2_test/q2_icon_07.png",
        "pages/normal_problems/resources/q2_test/q2_icon_08.png",
        "pages/normal_problems/resources/q2_test/q2_icon_09.png",
        "pages/normal_problems/resources/q2_test/q2_icon_10.png",
        "pages/normal_problems/resources/q2_test/q2_icon_11.png",
        "pages/normal_problems/resources/q2_test/q2_icon_12.png"
    ]

    # 1行×5列で画像を表示
    cols = st.columns(5)
    for col_idx, col in enumerate(cols):
        with col:
            if os.path.exists(image_paths_q[col_idx]):
                st.image(image_paths_q[col_idx], width=100)

    st.write("")  # Add space between containers
    
    # 2行×4列で画像を表示
    for row in range(2):
        cols = st.columns(4)
        for col_idx, col in enumerate(cols):
            img_idx = row * 4 + col_idx
            if img_idx < len(image_paths_a):  # Check if index is within bounds
                with col:
                    st.write(f"{'①②③④⑤⑥⑦⑧'[img_idx]}")  # Updated to include ⑧
                    if os.path.exists(image_paths_a[img_idx]):
                        st.image(image_paths_a[img_idx], width=100)

    # 選択ボックスを追加
    selected_number = st.selectbox(
        "？部分に入る、正しいアイコンの番号を選んでください:",
        ["選択してください", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧"],
        key=f"{tab_name}_selection"
    )

    return selected_number


def process_answer(answer: str, state, session: Session) -> None:
    if answer == "④":
        state["is_clear"] = True
        st.success("正解です！")
    else:
        state["is_clear"] = False
        st.error("不正解です")

    save_table(state, session)


def run(tab_name: str, session: Session):
    state = init_state(tab_name, session, MAX_ATTEMPTS_MAIN)
    main_attempt = init_attempt(
        max_attempts=MAX_ATTEMPTS_MAIN, tab_name=tab_name, session=session, key="main"
    )

    answer = present_quiz(tab_name, MAX_ATTEMPTS_MAIN)

    placeholder = st.empty()
    if check_is_failed(session, state):
        process_exceeded_limit(placeholder, state)
    elif placeholder.button("回答する", key=f"{tab_name}_submit"):
        if main_attempt.check_attempt():
            if answer != "選択してください":
                process_answer(answer, state, session)
            else:
                st.warning("番号を選択してください")
        else:
            process_exceeded_limit(placeholder, state)

    clear_submit_button(placeholder, state)
