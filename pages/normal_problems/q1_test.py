import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement

MAX_ATTEMPTS_MAIN = 3


def present_quiz(tab_name: str, max_attempts: int) -> str:
    header_animation()
    st.header("Q1 - Test", divider="rainbow")

    st.write("Question 1: 画像を正しい順序に並び替えてください")
    st.write(f"回答回数の上限は {max_attempts}回です。")

    # 画像ファイルのパス
    image_paths = [
        "pages/normal_problems/resources/q1_test/sample01.png",
        "pages/normal_problems/resources/q1_test/sample02.png",
        "pages/normal_problems/resources/q1_test/sample03.png", 
        "pages/normal_problems/resources/q1_test/sample04.png"
    ]
    
    # 画像の番号（①、②、③、④）
    image_numbers = ["①", "②", "③", "④"]
    
    # 画像を表示
    st.write("### 並び替える画像:")
    cols = st.columns(4)
    for i, (col, img_path, number) in enumerate(zip(cols, image_paths, image_numbers)):
        with col:
            if os.path.exists(img_path):
                st.image(img_path, caption=f"画像{number}", use_container_width=True)
    
    st.write("---")
    st.write("### 正しい順序を選択してください:")
    
    # コンテナを作成
    cols = st.columns(4)
    user_order = []
    
    for i, col in enumerate(cols):
        with col:
            selected = st.selectbox(
                f"Position {i+1}",
                options=image_numbers,
                key=f"{tab_name}_image_{i}"
            )
            user_order.append(selected)
            
    return user_order


def process_answer(answer: list, state, session: Session) -> None:
    correct_order = ["①", "③", "④", "②"]
    
    if answer == correct_order:
        state["is_clear"] = True
        st.success("正解です！")
    else:
        state["is_clear"] = False
        st.error("不正解です。もう一度試してください。")

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
    elif placeholder.button("Answer", key=f"{tab_name}_submit"):
        if main_attempt.check_attempt():
            if answer:
                process_answer(answer, state, session)
            else:
                st.warning("選択してください")

        else:
            process_exceeded_limit(placeholder, state)

    clear_submit_button(placeholder, state)
