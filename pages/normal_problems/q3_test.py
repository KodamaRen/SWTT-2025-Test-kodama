import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.designs import header_animation, display_problem_statement_swt25



def present_quiz(tab_name: str) -> list:
    header_animation()
    st.header("🧭:red[混迷の鬼] 〜判別の呼吸〜", divider="red")

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
        # Japanese Store Data Master　　店舗マスター
        "全国小売チェーン（SM、CVS、HC/DS、DRUG）の位置情報付き店舗データベース",
        # Prepper Open Data Bank - Japanese City Data
        "日本の市区町村データ（人口、家計経済状況、住宅・土地、インフラ、...）",
        # Stock Master File
        "日本国内上場株式の銘柄属性情報",
        # 1km メッシュ過去天気データ（1km mesh Past Weather Data）
        "日本最大の気象観測網や全国のユーザーから寄せられる天気・体感情報",
        # IP Fan-Kit IPファン-kit
        "マンガ・アニメ・ゲームを中心とした、30万人規模の生活者×IPデータベース",
    ]
    
    selected_options = []
    
    st.write("#### 該当するものをすべて選択してください:")
    
    for i, option in enumerate(options):
        if st.checkbox(option, key=f"{tab_name}_option_{i}"):
            selected_options.append(option)
            
    return selected_options


def process_answer(answer: list, state, session: Session) -> None:
    correct_answers = [
        "全国小売チェーン（SM、CVS、HC/DS、DRUG）の位置情報付き店舗データベース",
        "日本の市区町村データ（人口、家計経済状況、住宅・土地、インフラ、...）",
        "日本国内上場株式の銘柄属性情報",
        "日本最大の気象観測網や全国のユーザーから寄せられる天気・体感情報",
        "マンガ・アニメ・ゲームを中心とした、30万人規模の生活者×IPデータベース",
    ]
    
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

    if state["is_clear"]:
        st.info("""
        #### 💡解説
        
        Snowflake Marketplaceでは、様々なデータセットが提供されています:

        1. **Japanese Store Data Master - INTAGE Inc. 株式会社インテージ**  
           全国の小売店舗の位置情報と属性データを提供

        2. **Prepper Open Data Bank - truestar inc.**  
           日本の市区町村の詳細な統計データを提供

        3. **Stock Master File - QUICK Corp.**  
           日本の上場企業の株式情報を網羅的に収録

        4. **1km メッシュ過去天気データ - Weathernews Inc.**  
           高精度な気象データと体感情報を組み合わせた気象データベース

        5. **IP Fan-Kit - INTAGE Inc. 株式会社インテージ**  
           エンタメ業界向けの大規模なファン行動データベース

        これらは全て、Snowflakeのマーケットプレイスを通じて、安全かつ効率的に利用可能です。
        
        各データセットは定期的に更新され、高品質なデータを提供しています。
        """)
