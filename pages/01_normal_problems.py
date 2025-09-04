# from streamlit_profiler import Profiler

import streamlit as st
import os
import importlib

from utils.utils import (
    check_is_clear,
    update_clear_status,
    reset_problem_status,
    display_page_titles_sidebar,
    display_team_id_sidebar,
    get_session,
    get_team_id,
    TAB_TITLES,
    DEMON_NAME,
)
from utils.designs import (
    apply_default_custom_css,
    display_applied_message,
    background_image,
    display_demon_message_html
)

# with Profiler():  # 性能調査をする場合はコメントアウトを外して下記コードをすべてインデント下げる。

display_page_titles_sidebar()

st.title("⚔️柱の試練")
background_image("pages/common/images/wars.png")

team_id = get_team_id()
if f"{team_id}_display_preparation_message" not in st.session_state:
    st.session_state[f"{team_id}_display_preparation_message"] = True

session = get_session()
display_team_id_sidebar()

problems_dir = "pages/normal_problems"
problem_files = [f for f in os.listdir(problems_dir) if f.endswith(".py")]

tabs = {}
for file in problem_files:
    module_name = file[:-3]
    module_path = f"pages.normal_problems.{module_name}"
    tabs[module_name] = importlib.import_module(module_path)

tab_titles = []
problem_ids = []
state = {}
state["team_id"] = session.get_current_user()[1:-1]

progress_text = "Loading..."
progress_bar = st.progress(value=0, text=progress_text)
total_steps = len(tabs.keys())

for i, problem_id in enumerate(tabs.keys()):
    progress_bar.progress(int((i + 1) / total_steps * 100), progress_text)
    state["problem_id"] = problem_id

    # タブタイトルの定義にない問題はスキップする
    if problem_id not in TAB_TITLES:
        continue

    #
    if (
        f"{state['problem_id']}_{state['team_id']}_is_init_updated"
        not in st.session_state
    ):
        st.session_state[
            f"{state['problem_id']}_{state['team_id']}_is_init_updated"
        ] = True
        update_clear_status(session, state)

    # タブ名、タブステートの初期化
    if f"{state['problem_id']}_{state['team_id']}_title" not in st.session_state:

        # クリアフラグを追加するIFステートメント
        if check_is_clear(session, state):
            checker = "✅️ "
            st.session_state[f"{state['problem_id']}_{state['team_id']}_is_clear"] = (
                True
            )
        else:
            checker = ""
            st.session_state[f"{state['problem_id']}_{state['team_id']}_is_clear"] = (
                False
            )

        # タブタイトル（物理名）にフラグを追加する処理
        st.session_state[f"{state['problem_id']}_{state['team_id']}_title"] = (
            checker + TAB_TITLES[problem_id]
        )

    # タブタイトル（物理名）の追加
    tab_titles.append(
        st.session_state[f"{state['problem_id']}_{state['team_id']}_title"]
    )
    problem_ids.append(problem_id)

# st.button(
#    "クリスタルの復活状況を更新する",
#    on_click=reset_problem_status,
# )

success_placeholder = st.empty()
if st.session_state[f"{team_id}_display_preparation_message"]:
    success_placeholder.success("戦いの準備が整ったようだ。")
    st.session_state[f"{team_id}_display_preparation_message"] = False
else:
    success_placeholder.empty()

st.session_state["problem_ids"] = problem_ids


# セレクトボックスの実装の場合
if "rerun" not in st.session_state:
    st.session_state["rerun"] = False

selected_index_state_name = f"{team_id}_selected_index"
if selected_index_state_name not in st.session_state:
    st.session_state[selected_index_state_name] = 0


def update_selected_index():
    st.session_state[selected_index_state_name] = tab_titles.index(
        st.session_state[f"{team_id}_selected_problem"]
    )


selected_problem = st.selectbox(
    "討伐する鬼を選択するんだ！！",
    options=tab_titles,
    index=st.session_state[selected_index_state_name],
    on_change=update_selected_index,
    key=f"{team_id}_selected_problem",
)

selected_problem_id = problem_ids[tab_titles.index(selected_problem)]


message = f"""
お前らがあの <b>{team_id}</b> のものたちか。
この『{DEMON_NAME[selected_problem_id]}』を倒せるものなら倒してみよ！！
"""
avatar_image_path = f"pages/common/images/demons/{DEMON_NAME[selected_problem_id]}.png"

display_demon_message_html(
    message,
    avatar_image=avatar_image_path,
    avatar_size=72,
)

st.write("")
st.write("")

tabs[selected_problem_id].run(selected_problem_id, session)


# タブの実装の場合
# selected_tab = st.tabs(tab_titles)

# for i, tab_title in enumerate(problem_ids):
#     with selected_tab[i]:
#         tabs[tab_title].run(tab_title, session)


progress_bar.empty()
