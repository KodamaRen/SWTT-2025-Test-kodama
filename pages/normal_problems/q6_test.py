import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from typing import Dict, Any, List, Optional
import os
import time

from utils.utils import save_table, init_state, clear_submit_button
from utils.attempt_limiter import check_is_failed, init_attempt, process_exceeded_limit
from utils.designs import header_animation, display_problem_statement_swt25

MAX_ATTEMPTS_MAIN = 100
MAX_HINTS = 2

# Cortex Analyst設定
DATABASE = "SNOWFLAKE_LEARNING_DB"
SCHEMA = "CORTEX_ANALYST_DEMO"
STAGE = "RAW_DATA"
FILE = "semantic_model_J_CI_FD20.yaml"


# === Snowflake接続関数 ===
def build_connector(session):
    return session.connection

# === Cortex Analyst関連関数 ===

def send_cortex_message(prompt: str, connector) -> Optional[Dict[str, Any]]:
    """Cortex Analystにメッセージを送信"""
    try:
        request_body = {
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            "semantic_model_file": f"@{DATABASE}.{SCHEMA}.{STAGE}/{FILE}",
        }
        
        # ホスト情報を取得
        host = getattr(connector, 'host', 'FSUOFLI-SQ50969.snowflakecomputing.com')
        
        # トークンを取得
        if hasattr(connector, 'rest') and hasattr(connector.rest, 'token'):
            token = connector.rest.token
        else:
            # トークンが取得できない場合はエラー
            st.error("認証トークンの取得に失敗しました")
            return None
        
        resp = requests.post(
            url=f"https://{host}/api/v2/cortex/analyst/message",
            json=request_body,
            headers={
                "Authorization": f'Snowflake Token="{token}"',
                "Content-Type": "application/json",
            },
            timeout=30
        )
        
        if resp.status_code < 400:
            return resp.json()
        else:
            st.error(f"Cortex Analyst API Error: {resp.status_code}")
            return None
            
    except Exception as e:
        st.error(f"Cortex Analystエラー: {str(e)}")
        return None

def display_cortex_content(content: List[Dict[str, str]], connector) -> None:
    """Cortexレスポンスを表示"""
    for item in content:
        if item["type"] == "text":
            st.markdown(item["text"])
        elif item["type"] == "sql":
            with st.expander("SQLクエリ", expanded=False):
                st.code(item["statement"], language="sql")
            with st.expander("実行結果", expanded=True):
                try:
                    with st.spinner("SQL実行中..."):
                        df = pd.read_sql(item["statement"], connector)
                        st.dataframe(df, use_container_width=True)
                except Exception as e:
                    st.error(f"SQL実行エラー: {str(e)}")

# === メイン関数 ===
def present_quiz(tab_name: str = "q6_test", connector=None) -> str:
    """クイズ問題を表示"""
    
    header_animation()
    st.header(":blue[分析の鬼] 〜言葉の呼吸〜", divider="blue")
    
    display_problem_statement_swt25(
    f"""
    <i>"序列に隠された真実への道標。<br/>
その位置を正確に見抜くことで、データの扉は開かれる。"</i><br/><br/>

2020年国勢調査が記した47都道府県の人口順位。<br/>
ちょうど20番目に存在する地域。その名を突き止めよ。<br/><br/>

<b>ヒント：Cortex Analystの刀に{MAX_HINTS}回まで質問可能。データを賢く分析し、答えを導き出せ。</b>
    """
    )
    
    # データサンプル表示
    if connector:
        with st.expander("📊 データテーブル構造を確認", expanded=False):
            try:
                sample_query = f"""
                SELECT * FROM {DATABASE}.{SCHEMA}.J_CI_FD20 
                LIMIT 5
                """
                sample_df = pd.read_sql(sample_query, connector)
                st.dataframe(sample_df, use_container_width=True)
                st.caption(f"データソース: {DATABASE}.{SCHEMA}.J_CI_FD20")
            except Exception as e:
                st.error(f"データ取得エラー: {str(e)}")
    else:
        st.warning("データベースに接続されていません")
    
    # セッション状態の初期化
    if f'{tab_name}_hint_count' not in st.session_state:
        st.session_state[f'{tab_name}_hint_count'] = 0
    if f'{tab_name}_hints_history' not in st.session_state:
        st.session_state[f'{tab_name}_hints_history'] = []
    
    # ヒント状態の表示
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ヒント使用回数", f"{st.session_state[f'{tab_name}_hint_count']} / {MAX_HINTS}")
    with col2:
        remaining = MAX_HINTS - st.session_state[f'{tab_name}_hint_count']
        st.metric("残りヒント", remaining)
    with col3:
        if remaining == 0:
            st.warning("ヒント枯渇")
        else:
            st.info("ヒント利用可能")
    
    # ヒント機能
    st.markdown("### 💡 Cortex Analyst の刀システム")
    
    if st.session_state[f'{tab_name}_hint_count'] < MAX_HINTS:
        hint_question = st.text_input(
            "Cortex Analystの刀への質問",
            placeholder="例: 2020年の人口ランキング15位から25位を表示して",
            key=f"{tab_name}_hint_input"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            get_hint = st.button(
                "ヒント取得",
                key=f"{tab_name}_get_hint",
                type="primary",
                disabled=(st.session_state[f'{tab_name}_hint_count'] >= MAX_HINTS or not connector)
            )
        
        if get_hint and hint_question and connector:
            st.session_state[f'{tab_name}_hint_count'] += 1
            with st.spinner("Cortex Analystが分析中..."):
                response = send_cortex_message(hint_question, connector)
                if response:
                    hint_result = {
                        'question': hint_question,
                        'response': response["message"]["content"]
                    }
                    st.session_state[f'{tab_name}_hints_history'].append(hint_result)
                    
                    st.success(f"ヒント {st.session_state[f'{tab_name}_hint_count']} 取得完了")
                    display_cortex_content(response["message"]["content"], connector)
                else:
                    st.session_state[f'{tab_name}_hint_count'] -= 1
    else:
        st.warning("⚠️ ヒントの使用回数が上限に達しました。自力で解答してください。")
    
    # 過去のヒント表示
    if st.session_state[f'{tab_name}_hints_history']:
        with st.expander("📜 取得済みヒント履歴", expanded=False):
            for i, hint in enumerate(st.session_state[f'{tab_name}_hints_history'], 1):
                st.markdown(f"**ヒント {i}: {hint['question']}**")
                if connector:
                    display_cortex_content(hint['response'], connector)
                st.markdown("---")
    
    # 回答入力
    st.markdown("---")
    st.markdown("### 🎯 最終回答")
    answer = st.text_input(
        "都道府県名を入力",
        placeholder="例: 東京都、大阪府、青森県",
        key=f"{tab_name}_answer_input"
    )
    
    return answer

def process_answer(answer: str, state: Dict, session) -> None:
    """回答を処理"""
    correct_answer = "岡山県"
    
    if answer and answer.strip():
        state['attempts'] = state.get('attempts', 0) + 1
        
        if answer.strip() == correct_answer:
            state["is_clear"] = True
            st.balloons()
            st.success(f"**討伐成功！** 正解は{correct_answer}でした！分析の鬼を撃破した！")
        else:
            state["is_clear"] = False
            st.error(f"**討伐失敗！** 「{answer}」は不正解... 鬼に惑わされた。")
            
            # ヒントが残っている場合は案内
            tab_name = state.get("tab_name", "q6_test")
            remaining = MAX_HINTS - st.session_state.get(f'{tab_name}_hint_count', 0)
            if remaining > 0:
                st.info(f"💡 ヒントをあと{remaining}回使用できます。")
    else:
        st.warning("回答を入力してください")
    
    save_table(state, session)

def run(tab_name: str = "q6_test", session = None):
    """メイン実行関数（スタンドアロン版）"""
    state = init_state(tab_name, session, MAX_ATTEMPTS_MAIN)
    main_attempt = init_attempt(
        max_attempts=MAX_ATTEMPTS_MAIN, tab_name=tab_name, session=session, key="main"
    )
    
    connector = build_connector(session)
    answer = present_quiz(tab_name, connector)
    
    placeholder = st.empty()
    if check_is_failed(session, state):
        process_exceeded_limit(placeholder, state)
    elif placeholder.button("Answer", key=f"{tab_name}_submit"):
        if main_attempt.check_attempt():
                process_answer(answer, state, session)
        else:
            process_exceeded_limit(placeholder, state)

    clear_submit_button(placeholder, state)

# === エントリーポイント ===

if __name__ == "__main__":
    st.set_page_config(
        page_title="分析の鬼",
        page_icon="🗾",
        layout="wide"
    )
    
    # .envファイルから環境変数を読み込む（オプション）
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    run()
