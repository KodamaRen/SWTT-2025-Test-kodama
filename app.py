import streamlit as st
from snowflake.snowpark import Session

from utils.utils import (
    create_session,
    display_team_id_sidebar,
    display_page_titles_sidebar,
    TEAMS,
)
from utils.designs import (
    apply_default_custom_css,
    display_applied_message,
    background_image,
)


display_page_titles_sidebar()


st.title("🏯複雑空城、決戦の時")
display_team_id_sidebar()

css_name = apply_default_custom_css()
message = """
*部門ごとに分断されたデータ、その場凌ぎの改修、無秩序に散在したデータ*

これらの混沌が重なり合い、突如として現れた異形の迷宮「複雑空城」

この城で暴走する鬼たちにより、世界中のデータ基盤が崩壊の危機にある。

—— しかし、まだ希望は残されている。

データの世界で磨き上げた「Snowflakeの呼吸」を駆使して、鬼たちを討伐せよ。

選ばれし柱たちよ、立ち上がれ。
"""

display_applied_message(message, css_name)
background_image("pages/common/images/sky.png", dark_mode=False)

st.write("")
team_id = st.selectbox(
    label="結成する討伐隊を選択",
    options=list(TEAMS.keys()),
)

if team_id:
    st.session_state.clear()
    st.session_state.team_id = team_id
    st.session_state.snow_session = create_session(TEAMS[team_id])

    if st.button("戦場へ進む"):
        print(st.session_state)
        st.switch_page("pages/01_normal_problems.py")
