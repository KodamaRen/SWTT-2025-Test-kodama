import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement_swt25

MAX_ATTEMPTS_MAIN = 100


def present_quiz(tab_name: str, max_attempts: int) -> list:
    header_animation()
    st.header("🌊:red[波紋の鬼] 〜コミュニティの呼吸〜", divider="red")

    display_problem_statement_swt25(
    """
    <i>"波紋のごとく広がるコミュニティの絆。
    その規模を正しく測り、真の繋がりを見極めよ。"</i><br/><br/>

    Snowflakeコミュニティの力を測る時が来た。<br/>
    的確な数字を見極め、コミュニティの真の姿を明らかにせよ。
    """
    )
    # st.write(f"**討伐回数制限**: {max_attempts}回まで")
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 問題1")
        st.write("2025年9月4日時点でのSnowflakeコミュニティ（日本）の参加者数は何人でしょうか？")

        options1 = [
            "約700人", 
            "約1,000人",
            "約1,300人", 
            "約1,600人",
            "約1,900人"
        ]

        answer1 = st.radio("選択肢:", options1, key=f"{tab_name}_answer1")

    with col2:
        st.write("#### 問題2") 
        st.write("検討中: コミュニティグループ系問題？チラシとか見て分かる問題？")

        options2 = [
            "Answer01",
            "Answer02", 
            "Answer03",
            "Answer04",
            "Answer05"
        ]

        answer2 = st.radio("選択肢:", options2, key=f"{tab_name}_answer2")

    return [answer1, answer2]


def process_answer(answers: list, state: dict, session: Session):
    # 正解の設定
    correct_answer1 = "約1,900人"
    correct_answer2 = "Answer01"
    
    is_correct1 = answers[0] == correct_answer1
    is_correct2 = answers[1] == correct_answer2

    if is_correct1 and is_correct2:
        state["is_clear"] = True
        st.success("**討伐成功！** 雷の速さで正確な数字を見抜いた！")
        st.balloons()
        st.write("""
        **解説**: 
        - 2025年9月時点で、Snowflakeコミュニティ（日本）の参加者数は約1,900人程度です。
        - 日本国内にはxxのユーザーグループが存在し、各地域で定期的な勉強会やミートアップを開催しています。
        """)
    else:
        state["is_clear"] = False
        
        if is_correct1:
            st.error("**討伐失敗！** 問題1は正解です！問題2の答えをもう一度考えてみましょう。")
        elif is_correct2:
            st.error("**討伐失敗！** 問題2は正解です！問題1の答えをもう一度考えてみましょう。")
        
        st.info("💡ヒント: Snowflakeコミュニティ「SnowVillage」を見てみよう！")

    save_table(state, session)


def run(tab_name: str, session: Session):
    state = init_state(tab_name, session, MAX_ATTEMPTS_MAIN)
    main_attempt = init_attempt(
        max_attempts=MAX_ATTEMPTS_MAIN, tab_name=tab_name, session=session, key="main"
    )

    answers = present_quiz(tab_name, MAX_ATTEMPTS_MAIN)

    placeholder = st.empty()
    if check_is_failed(session, state):
        process_exceeded_limit(placeholder, state)
    elif placeholder.button("Answer", key=f"{tab_name}_submit"):
        if main_attempt.check_attempt():
                process_answer(answers, state, session)
        else:
            process_exceeded_limit(placeholder, state)

    clear_submit_button(placeholder, state)