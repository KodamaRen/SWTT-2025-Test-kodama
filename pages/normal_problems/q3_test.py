import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.designs import header_animation, display_problem_statement_swt25



def present_quiz(tab_name: str) -> list:
    header_animation()
    st.header(":red[混迷の鬼] 〜判別の呼吸〜", divider="red")

    # Problem statement and demon image side by side
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_problem_statement_swt25(
        """
        <i>"混沌たる情報の海に、真の宝は埋もれている。
        その本質を見抜き、宝を手にする術を会得せよ。"</i><br/><br/>

        数あるデータの中から、Snowflake Marketplaceで提供されているデータはどれか。<br/>
        """
        )
    
    with col2:
        # Demon image display with vertical centering
        demon_image_path = "pages/common/images/demons/demon3.jpg"
        try:
            # Use markdown with CSS for vertical centering
            st.markdown(
                """
                <div style="display: flex; align-items: center; height: 100%; justify-content: center;">
                """,
                unsafe_allow_html=True
            )
            st.image(demon_image_path, caption="混迷の鬼", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception:
            st.markdown(
                """
                <div style="display: flex; align-items: center; height: 100%; justify-content: center;">
                    <p style="text-align: center;">📷 鬼の姿を撮影中...</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    

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
    state = init_state(tab_name, session)

    answer = present_quiz(tab_name)

    placeholder = st.empty()
    if placeholder.button("Answer", key=f"{tab_name}_submit"):
        if answer:
            process_answer(answer, state, session)
        else:
            st.warning("選択してください")

    clear_submit_button(placeholder, state)
