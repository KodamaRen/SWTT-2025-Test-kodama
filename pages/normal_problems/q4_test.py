import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement_swt25

MAX_ATTEMPTS_MAIN = 100


def present_quiz(tab_name: str, max_attempts: int) -> list:
    header_animation()
    st.header(":red[真偽の鬼] 〜見極めの呼吸〜", divider="red")

    display_problem_statement_swt25(
    """
    <i>"真と偽、存在と不在。
    その境界線を見極めることが、道を切り開く鍵となる。"</i><br/><br/>

    Snowflakeの機能とサービスが、一定の法則で分けられている。<br/>
    それぞれの存在を正しく見分け、真実を見極めよ。
    """
    )
    st.write("まず、以下の例を見てください:")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #e6f3ff; padding: 20px; border-radius: 10px; border: 2px solid #0066cc'>
            <h4 style='color: #0066cc; text-align: center'>ある</h4>
            <ul style='margin-bottom: 0'>
                <li style='color: #000000'>Cloud Services</li>
                <li style='color: #000000'>Iceberg Tables</li>
                <li style='color: #000000'>Streamlit</li>
                <li style='color: #000000'>Horizon Catalog</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #fff2e6; padding: 20px; border-radius: 10px; border: 2px solid #ff8533'>
            <h4 style='color: #ff8533; text-align: center'>なし</h4>
            <ul style='margin-bottom: 0'>
                <li style='color: #000000'>Data Warehouse</li>
                <li style='color: #000000'>External Tables</li>
                <li style='color: #000000'>Intelligence</li>
                <li style='color: #000000'>Search Optimization Service</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    st.write("##### 以下の項目について「ある」「なし」のどちらに属するか選んでください:")
    # st.write(f"回答回数の上限は {max_attempts}回です。")

    options = [
        "Snowpark Container Service",
        "Data Lake", 
        "Data Mart",
        "Star Schema",
        "Openflow",
        "Retrieval Augmented Generation"
    ]

    if "selected_options" not in st.session_state:
        st.session_state.selected_options = {}
        for option in options:
            st.session_state.selected_options[option] = None

    selected_options = []

    for option in options:
        cols = st.columns([1, 2, 1, 1])
        
        with cols[1]:
            st.write(option)
            
        with cols[0]:
            if st.button("ある", key=f"button_{option}_left", 
                type="primary" if st.session_state.selected_options[option] == "ある" else "secondary"):
                st.session_state.selected_options[option] = "ある"
                if option not in selected_options:
                    selected_options.append(option)
                st.rerun()
                
        with cols[2]:
            if st.button("なし", key=f"button_{option}_right",
                type="primary" if st.session_state.selected_options[option] == "なし" else "secondary"):
                st.session_state.selected_options[option] = "なし"
                if option in selected_options:
                    selected_options.remove(option)
                st.rerun()

    return selected_options


def process_answer(answer: list, state, session: Session) -> None:
    correct_answers_exist = ["Snowpark Container Service", "Data Lake", "Star Schema"]
    correct_answers_not_exist = ["Data Mart", "Openflow", "Retrieval Augmented Generation"]
    
    # Get all options from session state
    all_options = list(st.session_state.selected_options.keys())
    print(all_options)
    
    selected_exist = [opt for opt in all_options if st.session_state.selected_options[opt] == "ある"]
    selected_not_exist = [opt for opt in all_options if st.session_state.selected_options[opt] == "なし"]
    print(selected_exist)
    print(selected_not_exist)

    if (sorted(selected_exist) == sorted(correct_answers_exist) and 
        sorted(selected_not_exist) == sorted(correct_answers_not_exist)):
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
            # Check if all options have been selected
            all_selected = all(value is not None for value in st.session_state.selected_options.values())
            if not all_selected:
                st.warning("全ての項目について「ある」「なし」を選択してください")
            else:
                process_answer(answer, state, session)
        else:
            process_exceeded_limit(placeholder, state)

    clear_submit_button(placeholder, state)
