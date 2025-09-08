import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement_swt25

MAX_ATTEMPTS_MAIN = 100


def present_quiz(tab_name: str, max_attempts: int) -> list:
    header_animation()
    st.header("🧭:red[混迷の鬼] 〜判別の呼吸〜", divider="red")

    display_problem_statement_swt25(
    """
    <i>"混沌たる情報の海に、真の宝は埋もれている。
    その本質を見抜き、宝を手にする術を会得せよ。"</i><br/><br/>

    数あるデータの中から、Snowflake Marketplaceで提供されているデータはどれか。<br/>
    """
    )
    
    # st.write(f"**討伐回数制限**: {max_attempts}回まで")

    options = [
        # Japanese Store Data Master　　店舗マスター
        "約120万件の商品コードと豊富な属性情報を網羅する、消費財特化の商品データベース",
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
        "約120万件の商品コードと豊富な属性情報を網羅する、消費財特化の商品データベース",
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

    if state["is_clear"]:
        st.info("""
        #### 💡解説
        
        Snowflake Marketplaceでは、様々なデータセットが提供されています:

        1. **Japanese Product Master 商品マスター - INTAGE Inc. 株式会社インテージ**  
           約120万件の商品コードと約3万1千社の国内主要メーカー情報を網羅。  
           食品、日用品、OTC医薬品など多岐に渡るカテゴリを約330分目に分類

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
