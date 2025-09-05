import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.designs import header_animation, display_problem_statement_swt25


def present_quiz(tab_name: str) -> str:
    header_animation()
    st.header(":red[不規則の鬼] 〜法則の呼吸〜", divider="red")

    # Problem statement and demon image side by side
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_problem_statement_swt25(
        """
        <i>"法則は隠された真実への道標。
        その規則性を見抜き、正しい選択をすることで道は開かれる。"</i><br/><br/>

        Snowflakeのアイコンに隠された法則性。<br/>
        その規則を見抜き、失われた真実を取り戻せ。
        """
        )
    
    with col2:
        # Demon image display with vertical centering
        demon_image_path = "pages/common/images/demons/demon2.jpg"
        try:
            # Use markdown with CSS for vertical centering
            st.markdown(
                """
                <div style="display: flex; align-items: center; height: 100%; justify-content: center;">
                """,
                unsafe_allow_html=True
            )
            st.image(demon_image_path, caption="不規則の鬼", use_container_width=True)
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

    # 画像ファイルのパス
    image_paths_q = [
        "pages/normal_problems/resources/q2_test/q2_01.png",
        "pages/normal_problems/resources/q2_test/q2_02.png",
        "pages/normal_problems/resources/q2_test/q2_13.png",
        "pages/normal_problems/resources/q2_test/q2_03.png",
        "pages/normal_problems/resources/q2_test/q2_04.png"
    ]

    # 画像ファイルのパス
    image_paths_a = [
        "pages/normal_problems/resources/q2_test/q2_05.png",
        "pages/normal_problems/resources/q2_test/q2_06.png",
        "pages/normal_problems/resources/q2_test/q2_07.png",
        "pages/normal_problems/resources/q2_test/q2_08.png",
        "pages/normal_problems/resources/q2_test/q2_09.png",
        "pages/normal_problems/resources/q2_test/q2_10.png",
        "pages/normal_problems/resources/q2_test/q2_11.png",
        "pages/normal_problems/resources/q2_test/q2_12.png"
    ]

    # 1行×9列で画像と矢印を表示（画像5つ、矢印4つ）
    cols = st.columns(9)
    for col_idx in range(9):
        with cols[col_idx]:
            if col_idx % 2 == 0:  # 偶数列に画像を表示
                img_idx = col_idx // 2
                if img_idx < len(image_paths_q):
                    if os.path.exists(image_paths_q[img_idx]):
                        st.image(image_paths_q[img_idx], width=100)
            else:  # 奇数列に矢印を表示
                st.markdown("<div style='text-align: center; font-size: 24px; line-height: 100px;'>→</div>", unsafe_allow_html=True)

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
                        st.image(image_paths_a[img_idx], width=80)

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
    state = init_state(tab_name, session)

    answer = present_quiz(tab_name)

    placeholder = st.empty()
    if placeholder.button("回答する", key=f"{tab_name}_submit"):
        if answer != "選択してください":
            process_answer(answer, state, session)
        else:
            st.warning("番号を選択してください")

    clear_submit_button(placeholder, state)
