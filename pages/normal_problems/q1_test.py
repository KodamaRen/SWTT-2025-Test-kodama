import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement_swt25

MAX_ATTEMPTS_MAIN = 100


def present_quiz(tab_name: str, max_attempts: int) -> str:
    header_animation()
    st.header(":red[過去忘却の鬼] 〜歴史の呼吸〜", divider="red")

    display_problem_statement_swt25(
    """
    <i>"時は流れ、記憶は薄れゆく。だが、真実は常に一つの道筋を持つもの。
    過去を正しく紡ぐことで、未来への扉は開かれる。"</i><br/><br/>

    時の流れの中で散り散りになってしまったSnowflakeの設定画面の記憶。<br/>
    これらの断片を、最も古いものから順に並べ直し、歴史の真実を取り戻せ。
    """
    )
    
    # st.write(f"**討伐回数制限**: {max_attempts}回まで")

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
    state = init_state(tab_name, session, MAX_ATTEMPTS_MAIN)
    main_attempt = init_attempt(
        max_attempts=MAX_ATTEMPTS_MAIN, tab_name=tab_name, session=session, key="main"
    )

    answer = present_quiz(tab_name, MAX_ATTEMPTS_MAIN)

    placeholder = st.empty()
    if check_is_failed(session, state):
        process_exceeded_limit(placeholder, state)
    elif placeholder.button("討伐開始", key=f"{tab_name}_submit"):
        if main_attempt.check_attempt():
            if answer:
                process_answer(answer, state, session)
            else:
                st.warning("記憶の断片を選択してください")

        else:
            process_exceeded_limit(placeholder, state)

    clear_submit_button(placeholder, state)
