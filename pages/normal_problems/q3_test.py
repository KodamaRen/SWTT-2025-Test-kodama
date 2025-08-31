import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement_swt25

MAX_ATTEMPTS_MAIN = 3


def present_quiz(tab_name: str, max_attempts: int) -> list:
    header_animation()
    st.header(":red[混迷の鬼] 〜判別の呼吸〜", divider="red")

    display_problem_statement_swt25(
    """
    <i>"混沌たる情報の海に、真の宝は埋もれている。
    その本質を見抜き、宝を手にする術を会得せよ。"</i><br/><br/>

    数あるデータの中から、Snowflake Marketplaceで提供されているデータはどれか。<br/>
    """
    )
    
    st.write(f"**討伐回数制限**: {max_attempts}回まで")

    options = [
        "飲食店の出店情報",
        "国勢調査情報 xxxx年",
        "株価・・・",
        "天気情報（xx kmメッシュ）",
        "・・・"
    ]
    
    selected_options = []
    
    st.write("#### 該当するものをすべて選択してください:")
    
    for i, option in enumerate(options):
        if st.checkbox(option, key=f"{tab_name}_option_{i}"):
            selected_options.append(option)
            
    return selected_options


def process_answer(answer: list, state, session: Session) -> None:
    correct_answers = ["飲食店の出店情報", "株価・・・"]
    
    if sorted(answer) == sorted(correct_answers):
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
