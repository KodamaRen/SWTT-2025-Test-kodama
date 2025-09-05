import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.designs import header_animation, display_problem_statement_swt25


def present_quiz(tab_name: str) -> str:
    header_animation()
    st.header(":red[過去忘却の鬼] 〜歴史の呼吸〜", divider="red")

    # Problem statement and demon image side by side
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_problem_statement_swt25(
        """
        <i>"時は流れ、記憶は薄れゆく。だが、真実は常に一つの道筋を持つもの。
        過去を正しく紡ぐことで、未来への扉は開かれる。"</i><br/><br/>

        時の流れの中で散り散りになってしまったSnowflakeの設定画面の記憶。<br/>
        これらの断片を、最も古いものから順に並べ直し、歴史の真実を取り戻せ。
        """
        )
    
    with col2:
        # Demon image display with vertical centering
        demon_image_path = "pages/common/images/demons/demon1.jpg"
        try:
            # Use markdown with CSS for vertical centering
            st.markdown(
                """
                <div style="display: flex; align-items: center; height: 100%; justify-content: center;">
                """,
                unsafe_allow_html=True
            )
            st.image(demon_image_path, caption="過去忘却の鬼", use_container_width=True)
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
    image_paths = [
        "pages/normal_problems/resources/q1_test/q1_01.png",
        "pages/normal_problems/resources/q1_test/q1_02.png",
        "pages/normal_problems/resources/q1_test/q1_03.png", 
        "pages/normal_problems/resources/q1_test/q1_04.png"
    ]
    
    # 画像の番号（①、②、③、④）
    image_numbers = ["①", "②", "③", "④"]
    
    # 画像を表示
    st.write("#### 記憶の断片:")
    
    # 最初の3つの画像を横並びで表示
    cols = st.columns(3)
    for i, (col, img_path, number) in enumerate(zip(cols, image_paths[:3], image_numbers[:3])):
        with col:
            if os.path.exists(img_path):
                st.image(img_path, caption=f"画像{number}", use_container_width=True)
    
    # 4つ目の画像を下に表示
    if os.path.exists(image_paths[3]):
        st.image(image_paths[3], caption=f"画像{image_numbers[3]}", width=700)
    
    st.write("---")
    st.write("#### 歴史の真実を復元せよ:")
    
    # コンテナを作成
    cols = st.columns(4)
    user_order = []
    
    for i, col in enumerate(cols):
        with col:
            selected = st.selectbox(
                f"時系列の順番 {i+1}",
                options=image_numbers,
                key=f"{tab_name}_image_{i}"
            )
            user_order.append(selected)
            
    return user_order


def process_answer(answer: list, state, session: Session) -> None:
    correct_order = ["①", "③", "④", "②"]
    
    if answer == correct_order:
        state["is_clear"] = True
        st.success("**討伐成功！** 記憶の迷宮を突破した！")
    else:
        state["is_clear"] = False
        st.error("**討伐失敗！** 鬼の記憶に惑わされた。再挑戦せよ！")

    save_table(state, session)


def run(tab_name: str, session: Session):
    state = init_state(tab_name, session)

    answer = present_quiz(tab_name)

    placeholder = st.empty()
    if placeholder.button("討伐開始", key=f"{tab_name}_submit"):
        if answer:
            process_answer(answer, state, session)
        else:
            st.warning("記憶の断片を選択してください")

    clear_submit_button(placeholder, state)
