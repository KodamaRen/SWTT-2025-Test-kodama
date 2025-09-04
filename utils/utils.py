import hashlib
from datetime import datetime

import pandas as pd
import streamlit as st
import snowflake.snowpark.functions as F
from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSQLException



TAB_TITLES = {
    "q1_test": "⌛️過去忘却の鬼 ~ 歴史の呼吸 ~",
    "q2_test": "🧩不規則の鬼 ~ 法則の呼吸 ~",
    "q3_test": "🧭混迷の鬼 ~ 判別の呼吸 ~",
    "q4_test": "🔍️真偽の鬼 ~ 見極めの呼吸 ~",
    "q5_test": "⚡️疾風の鬼 ~ Streamlitの呼吸 ~",
    "q6_test": "🌊波紋の鬼 ~ コミュニティの呼吸 ~",
}


# Key: 表示されるチーム名
# Value: secretsに記載されているチームID
TEAMS = {
    "": "",
    "一月上旬": "Jan_First",
    "一月下旬": "Jan_Second",
    "二月上旬": "Feb_First",
    "二月下旬": "Feb_Second",
    "三月上旬": "Mar_First",
    "三月下旬": "Mar_Second",
    "四月上旬": "Apr_First",
    "四月下旬": "Apr_Second",
    "五月上旬": "May_First",
    "五月下旬": "May_Second",
    "六月上旬": "Jun_First",
    "六月下旬": "Jun_Second",
    "七月上旬": "Jul_First",
    "七月下旬": "Jul_Second",
    "八月上旬": "Aug_First",
    "八月下旬": "Aug_Second",
    "九月上旬": "Sep_First",
    "九月下旬": "Sep_Second",
    "十月上旬": "Oct_First",
    "十月下旬": "Oct_Second",
    "十一月上旬": "Nov_First",
    "十一月下旬": "Nov_Second",
    "十二月上旬": "Dec_First",
    "十二月下旬": "Dec_Second",
}


def create_session(team_id: str, is_info: bool = True) -> Session:
    try:
        session = st.connection(team_id, type="snowflake", max_entries=1).session()
        session.sql("SELECT 1").collect()
        print("セッションの作成に成功しました。")
        if is_info:
            st.success("鬼との戦いの準備は整った！いざ、決戦の地へ！")
        return session

    except SnowparkSQLException as e:
        print(e)
        print("セッションの有効期限切れエラーが発生しました。")
        print("セッションの再作成を試みます。")
        session = st.connection(team_id, type="snowflake", max_entries=1).session()
        session.sql("SELECT 1").collect()
        print("セッションの再作成に成功しました。")
        if is_info:
            st.success("鬼との戦いの準備は整った！いざ、決戦の地へ！")
        return session

    except Exception as e:
        if is_info:
            st.error("複雑空城の結界が強固すぎる...！なにか問題が発生したようだ。")
            print(e)
            st.stop()


def get_session():
    if "snow_session" not in st.session_state:
        st.warning("そなたらは、まだ討伐隊として誓いが結ばれていないようだの・・・。")
        if st.button("討伐隊の結成に戻る"):
            st.switch_page("app.py")
        st.stop()
    else:
        session = st.session_state.snow_session
        return session


def display_page_titles_sidebar():
    with st.sidebar:
        st.page_link("app.py", label="討伐隊の結成", icon="🤝")
        st.page_link("pages/01_normal_problems.py", label="柱の試練", icon="⚔️")
        st.page_link(
            "pages/03_aggregate_results.py", label="鬼討伐進捗の帳", icon="📜"
        )


def display_team_id_sidebar():
    with st.sidebar:
        try:
            st.divider()
            if "team_id" in st.session_state:
                st.write(f"討伐隊名: {st.session_state.team_id}")
            else:
                st.write(f"討伐隊名: 未結成")
        except AttributeError as e:
            print(e)


def display_team_id():
    st.write(f"そなたらの討伐隊は 「**{st.session_state.team_id}**」 だ。")


def get_team_id():
    if "team_id" not in st.session_state:
        st.warning("そなたらは、まだ討伐隊として誓いが結ばれていないようだの・・・。")
        if st.button("討伐隊の結成に戻る"):
            st.switch_page("app.py")
        st.stop()
    else:
        return st.session_state.team_id


def init_state(tab_name: str, session: Session):
    state_name = f"{tab_name}_state"
    if state_name not in st.session_state:
        st.session_state.state = {}

    state = st.session_state.state

    state["team_id"] = session.get_current_user()[1:-1]
    state["problem_id"] = tab_name

    state["is_clear"] = check_is_clear(session, state)
    state["max_attempts"] = None  # 制限撤廃のためNullを設定

    return state


def save_table(state: dict, session: Session):
    df = pd.DataFrame(
        [
            {
                "team_id": state["team_id"],
                "problem_id": state["problem_id"],
                "timestamp": datetime.now(),
                "is_clear": state["is_clear"],
                "key": "main",
                "max_attempts": state["max_attempts"],
            }
        ],
        columns=[
            "team_id",
            "problem_id",
            "timestamp",
            "is_clear",
            "key",
            "max_attempts",
        ],
    )

    with st.spinner("鬼と激闘中..."):
        # session.write_pandas(df, "SUBMIT2", auto_create_table=False, overwrite=False)
        snow_df = session.create_dataframe(df)
        snow_df.write.mode("append").save_as_table("submit2")

        if state["is_clear"]:
            # はじめてのクリアの場合、if文内のロジックを実行する。
            if not st.session_state[
                f"{state['problem_id']}_{state['team_id']}_is_clear"
            ]:
                update_clear_status(session, state)
                st.session_state[f"{state['problem_id']}_{state['team_id']}_title"] = (
                    "✅️ "
                    + st.session_state[
                        f"{state['problem_id']}_{state['team_id']}_title"
                    ]
                )
                st.session_state[
                    f"{state['problem_id']}_{state['team_id']}_is_clear"
                ] = True

                st.rerun()



def update_clear_status(session: Session, state: dict) -> None:
    submit_table = session.table("submit2")

    try:
        result = submit_table.filter(
            (F.col("team_id") == state["team_id"])
            & (F.col("problem_id") == state["problem_id"])
            & (F.col("is_clear") == True)
        ).count()

        st.session_state[f"{state['problem_id']}_{state['team_id']}_is_clear"] = (
            result > 0
        )

    except IndexError as e:
        print(e)
        st.session_state[f"{state['problem_id']}_{state['team_id']}_is_clear"] = False


def check_is_clear(session: Session, state: dict):
    # 呼び出し側が session 引数を入力しているため、一旦この関数では使っていないが定義する。
    return st.session_state[f"{state['problem_id']}_{state['team_id']}_is_clear"]


def reset_problem_status() -> None:
    team_id = TEAMS[get_team_id()]

    for problem_id in st.session_state["problem_ids"]:
        # if f"{problem_id}_{team_id}_title" in st.session_state:
        del st.session_state[f"{problem_id}_{team_id}_title"]

    st.session_state[f"{team_id}_display_preparation_message"] = True


def clear_submit_button(placeholder, state):
    if st.session_state[f"{state['problem_id']}_{state['team_id']}_is_clear"]:
        placeholder.empty()
        placeholder.success("そなたらはすでにこの鬼を討伐している！")


def string_to_hash_int(base_string: str) -> int:
    # 文字列をUTF-8でエンコードし、SHA256ハッシュを計算
    hash_object = hashlib.sha256(base_string.encode("utf-8"))
    hash_hex = hash_object.hexdigest()

    # 16進数の文字列を整数に変換
    hash_int = int(hash_hex, 16)

    # 整数値をシードとして返す
    return hash_int
