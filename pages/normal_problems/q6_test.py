import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.designs import header_animation, display_problem_statement_swt25



def present_quiz(tab_name: str) -> str:
    header_animation()
    st.header("🌊波紋の鬼 ~ コミュニティの呼吸 ~", divider="blue")

    # 問題説明と鬼の画像を横並びに配置
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_problem_statement_swt25(
        """
        <i>"波紋のごとく広がるコミュニティの絆。
        その規模を正しく測り、真の繋がりを見極めよ。"</i><br/><br/>

        Snowflakeコミュニティの力を測る時が来た。<br/>
        的確な数字を見極め、コミュニティの真の姿を明らかにせよ。
        """
        )
    
    with col2:
        # Demon image display with vertical centering
        demon_image_path = "pages/common/images/demons/demon6.jpg"
        try:
            # Use markdown with CSS for vertical centering
            st.markdown(
                """
                <div style="display: flex; align-items: center; height: 100%; justify-content: center;">
                """,
                unsafe_allow_html=True
            )
            st.image(demon_image_path, caption="🌊波紋の鬼", use_container_width=True)
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
    
    st.subheader("🌟 Snowflakeコミュニティ関連問題")
    st.write("2025年9月4日時点でのSnowflakeコミュニティ（日本）の参加者数はおおよそ何人でしょうか？")
    
    # 選択肢を表示
    options = [
        "選択してください",
        "約1,000人", 
        "約1,500人",
        "約1,900人", 
        "約2,500人",
        "約3,500人"
    ]
    
    selected_answer = st.radio("正しい参加者数を選択してください:", options, key=f"{tab_name}_answer")
    
    st.info("💡 ヒント: Snowflakeコミュニティは日本でも活発に活動しており、多くのデータエンジニアやアナリストが参加しています。")
    
    return selected_answer


def process_answer(answer: str, state: dict, session: Session):
    # 正解は約1,900人（2025年9月時点の実際の数値）
    correct_answer = "約1,900人"
    
    if answer == correct_answer:
        state["is_clear"] = True
        st.success("**討伐成功！** 雷の速さで正確な数字を見抜いた！")
        st.balloons()
        st.write("**解説**: 2025年9月時点で、Snowflakeコミュニティ（日本）の参加者数は約1,900人程度です。日本のデータエンジニアリング分野の成長とともに、コミュニティも着実に拡大を続けています。")
    else:
        state["is_clear"] = False
        st.error("**討伐失敗！** コミュニティの規模を読み間違えた！再挑戦せよ！")
        st.write("**ヒント**: 日本におけるSnowflakeの普及状況とデータエンジニアリング市場の成長を考慮してみましょう。")

    save_table(state, session)


def run(tab_name: str, session: Session):
    state = init_state(tab_name, session)

    answer = present_quiz(tab_name)

    placeholder = st.empty()
    if placeholder.button("討伐開始", key=f"{tab_name}_submit"):
        if answer != "選択してください":
            process_answer(answer, state, session)
        else:
            st.warning("参加者数を選択してください")

    clear_submit_button(placeholder, state)