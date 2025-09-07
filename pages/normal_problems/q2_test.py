import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement_swt25

MAX_ATTEMPTS_MAIN = 100


def present_quiz(tab_name: str, max_attempts: int) -> str:
    
    # セッション状態の初期化（初回のみ）
    if f"{tab_name}_show_hints" not in st.session_state:
        st.session_state[f"{tab_name}_show_hints"] = False
    
    header_animation()
    st.header("🧩:red[不規則の鬼] 〜法則の呼吸〜", divider="red")

    display_problem_statement_swt25(
    """
    <i>"法則は隠された真実への道標。
    その規則性を見抜き、正しい選択をすることで道は開かれる。"</i><br/><br/>

    Snowflakeのアイコンに隠された法則性。<br/>
    その規則を見抜き、失われた真実を取り戻せ。
    """
    )
    # st.write(f"回答回数の上限は {max_attempts}回です。")

    # 画像ファイルのパス
    image_paths_q = [
        # Document AI
        "pages/normal_problems/resources/q2_test/icon_document_ai.png",
        # Iceberg Tables
        "pages/normal_problems/resources/q2_test/icon_iceberg_tables.png",
        # ？マーク（Snowpark Containers）
        "pages/normal_problems/resources/q2_test/icon_question_mark.png",
        # Snowpark Copilot
        "pages/normal_problems/resources/q2_test/icon_snowflake_copilot.png",
        # Tag
        "pages/normal_problems/resources/q2_test/icon_tag.png"
    ]

    # 画像ファイルのパス
    image_paths_a = [
        # Dynamic Tables
        "pages/normal_problems/resources/q2_test/icon_dynamic_tables.png",
        # Database
        "pages/normal_problems/resources/q2_test/icon_database.png",
        # Role
        "pages/normal_problems/resources/q2_test/icon_role.png",
        # Geospatial Analytics
        "pages/normal_problems/resources/q2_test/icon_geospetial_analytics.png",
        # Snowpark
        "pages/normal_problems/resources/q2_test/icon_snowpark.png",
        # Snowpark Containers
        "pages/normal_problems/resources/q2_test/icon_snowpark_containers.png",
        # Streamlit in Snowflake
        "pages/normal_problems/resources/q2_test/icon_streamlit_in_snowflake.png",
        # Semi-Structured Data
        "pages/normal_problems/resources/q2_test/icon_semi-structured_data.png"
    ]

    # 1行×9列で画像と矢印を表示（画像5つ、矢印4つ）
    st.write("問題")
    cols = st.columns(9)
    for col_idx in range(9):
        with cols[col_idx]:
            if col_idx % 2 == 0:  # 偶数列に画像を表示
                img_idx = col_idx // 2
                if img_idx < len(image_paths_q):
                    if os.path.exists(image_paths_q[img_idx]):
                        st.markdown("<div style='height:100px; display:flex; align-items:center>", unsafe_allow_html=True)
                        st.image(image_paths_q[img_idx], width=80)
                        st.markdown("</div>", unsafe_allow_html=True)
            else:  # 奇数列に矢印を表示
                st.markdown("<div style='text-align: center; font-size: 18px; line-height:100px;'>→</div>", unsafe_allow_html=True)
    
    # ヒントボタンが押された場合のみ個別ヒントを表示
    if st.session_state[f"{tab_name}_show_hints"]:
        # 各画像に対応する異なる文字を表示
        hint_texts = ["Document AI", "Iceberg Tables", "", "Snowpark Copilot", "Tag"]
        for i in range(5):
            cols[i*2].markdown(f"<div style='font-size: 14px; text-align: center; height: 40px'><strong>{hint_texts[i]}</strong></div>", unsafe_allow_html=True)
        
        st.write("")
        
        st.warning("""💡ヒント: 各アイコンの名称と繋がりに注目してみよう！""")


    st.write("")  # Add space between containers

    st.write("---")
    
    # 2行×4列で画像を表示
    for row in range(2):
        cols = st.columns(4)
        for col_idx, col in enumerate(cols):
            img_idx = row * 4 + col_idx
            if img_idx < len(image_paths_a):  # Check if index is within bounds
                with col:
                    st.write(f"{'①②③④⑤⑥⑦⑧'[img_idx]}")  # Updated to include ⑧
                    if os.path.exists(image_paths_a[img_idx]):
                        st.image(image_paths_a[img_idx], width=120)

    st.write("---")

    # 選択ボックスを追加
    selected_number = st.selectbox(
        "？部分に入る、正しいアイコンの番号を選んでください:",
        ["選択してください", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧"],
        key=f"{tab_name}_selection"
    )

    return selected_number


def process_answer(answer: str, state, session: Session) -> None:
    if answer == "⑥":
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

    # ヒントボタンの配置
    if st.button("💡 ヒントを見る", key=f"{tab_name}_hint_button"):
        # セッション状態でヒント表示フラグを設定
        st.session_state[f"{tab_name}_show_hints"] = True
        st.rerun()

    clear_submit_button(placeholder, state)
