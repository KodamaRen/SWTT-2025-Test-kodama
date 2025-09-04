import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.designs import header_animation, display_problem_statement_swt25



def present_quiz(tab_name: str) -> list:
    header_animation()
    st.header("🔍️:red[真偽の鬼] 〜見極めの呼吸〜", divider="red")

    # Problem statement and demon image side by side
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_problem_statement_swt25(
        """
        <i>"真と偽、存在と不在。
        その境界線を見極めることが、道を切り開く鍵となる。"</i><br/><br/>

        Snowflakeの機能とサービスが、一定の法則で分けられている。<br/>
        それぞれの存在を正しく見分け、真実を見極めよ。
        """
        )
    
    with col2:
        # Demon image display with vertical centering
        demon_image_path = "pages/common/images/demons/demon4.jpg"
        try:
            # Use markdown with CSS for vertical centering
            st.markdown(
                """
                <div style="display: flex; align-items: center; height: 100%; justify-content: center;">
                """,
                unsafe_allow_html=True
            )
            st.image(demon_image_path, caption="真偽の鬼", use_container_width=True)
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
    st.write("まず、以下の例を見てください:")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #ffe6e6; padding: 20px; border-radius: 10px; border: 3px solid #cc0000'>
            <h4 style='color: #cc0000; text-align: center'>ある</h4>
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
        <div style='background-color: #ffe0cc; padding: 20px; border-radius: 10px; border: 3px solid #ff8533'>
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
    
<<<<<<< HEAD
    st.write("以下の項目が「ある」「なし」のどちらに属するか選択してください")
    # st.write(f"回答回数の上限は {max_attempts}回です。")

=======
    st.write("##### 以下の項目について「ある」「なし」のどちらに属するか選んでください:")
>>>>>>> bc9c4f1 (基礎問題の作成)

    options = [
        "Snowpark Container Services",
        "Data Lake", 
        "Data Mart",
        "Star Schema",
        "Openflow",
        "Retrieval Augmented Generation"
    ]

    # 選択状態を保持するためのsession_stateを初期化
    if "selected_options" not in st.session_state:
        # 選択肢ごとの状態を格納する辞書を作成
        st.session_state.selected_options = {}
        st.session_state.selected_options = {option: None for option in options}

    for option in options:
        cols = st.columns([1, 2, 1, 1])
        
        with cols[1]:
            st.write(option)
            
        with cols[0]:
            # 「ある」ボタン
            # session_stateから現在の選択状態を取得
            current_value = st.session_state.selected_options.get(option, None)
            # 選択状態に応じてボタンの見た目を変更（選択中はprimary、未選択はsecondary）
            if st.button("ある", key=f"button_{option}_left", 
                type="primary" if current_value == "ある" else "secondary"):
                # 「ある」を選択状態として保存
                st.session_state.selected_options[option] = "ある"
                st.rerun()
                
        with cols[2]:
            # 「なし」ボタン
            # session_stateから現在の選択状態を取得
            current_value = st.session_state.selected_options.get(option, None)
            # 選択状態に応じてボタンの見た目を変更（選択中はprimary、未選択はsecondary）
            if st.button("なし", key=f"button_{option}_right",
                type="primary" if current_value == "なし" else "secondary"):
                # 「なし」を選択状態として保存
                st.session_state.selected_options[option] = "なし"
                st.rerun()

    # 選択されたオプションをリストとして返す
    selected_options = []
    for option, value in st.session_state.selected_options.items():
        if value == "ある":
            selected_options.append(option)
    
    return selected_options


def process_answer(answer: list, state, session: Session) -> None:
    correct_answers_exist = ["Snowpark Container Services", "Data Lake", "Star Schema"]
    correct_answers_not_exist = ["Data Mart", "Openflow", "Retrieval Augmented Generation"]
    
    # Get all options from session state
    all_options = list(st.session_state.selected_options.keys())
    
    selected_exist = [opt for opt in all_options if st.session_state.selected_options[opt] == "ある"]
    selected_not_exist = [opt for opt in all_options if st.session_state.selected_options[opt] == "なし"]

    if (sorted(selected_exist) == sorted(correct_answers_exist) and 
        sorted(selected_not_exist) == sorted(correct_answers_not_exist)):
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
        # Check if all options have been selected
        all_selected = all(value is not None for value in st.session_state.selected_options.values())
        if not all_selected:
            st.warning("全ての項目について「ある」「なし」を選択してください")
        else:
            process_answer(answer, state, session)

    st.write("---")

    if state["is_clear"]:
        st.warning("☝️解説：あるの方は、「Snow」や「Lake」など、自然に関連する単語が含まれています。")
    else:
        with st.expander("💡ヒントを見る"):
            st.warning("💡ヒント：「Ice」や「Horizon」といった単語に注目してみましょう！")

    clear_submit_button(placeholder, state)
