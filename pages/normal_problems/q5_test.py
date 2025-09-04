import streamlit as st
import os
from snowflake.snowpark import Session

from utils.utils import save_table, init_state, clear_submit_button
from utils.designs import header_animation, display_problem_statement_swt25



def present_quiz(tab_name: str) -> str:
    header_animation()
    st.header(":blue[疾風の鬼] 〜Streamlitの呼吸〜", divider="blue")

    # Problem statement and demon image side by side
    col1, col2 = st.columns([2, 1])
    
    with col1:
        display_problem_statement_swt25(
        """
        <i>"疾風の如く、真実を見抜け。
        Streamlitの力で正しい画面構成を見極めよ。"</i><br/><br/>

        以下のStreamlitプログラムを実行した時の画面構成はどれか？<br/>
        正しい画面構成を選択せよ。
        """
        )
    
    with col2:
        # Demon image display with vertical centering
        demon_image_path = "pages/common/images/demons/demon5.jpg"
        try:
            # Use markdown with CSS for vertical centering
            st.markdown(
                """
                <div style="display: flex; align-items: center; height: 100%; justify-content: center;">
                """,
                unsafe_allow_html=True
            )
            st.image(demon_image_path, caption="疾風の鬼", use_container_width=True)
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
    

    # 上部にStreamlitプログラムを表示
    st.subheader("📝 Streamlitプログラム")
    st.code("""
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Sales Dashboard")

# データの準備
data = {
    'month': ['Jan', 'Feb', 'Mar', 'Apr'],
    'sales': [100, 150, 120, 180]
}
df = pd.DataFrame(data)

# グラフを作成
fig = px.bar(df, x='month', y='sales', 
            title='Monthly Sales',
            color='sales',
            color_continuous_scale='Blues')

st.plotly_chart(fig)
    """, language="python")
    
    st.divider()
    
    # 下部に4つの選択肢をStreamlitで実装
    st.subheader("🤔 どのグラフが表示されるか？")
    st.write("以下の4つの選択肢から正しいグラフデザインを選んでください：")
    
    # データの準備（選択肢で使用）
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    
    data = {
        'month': ['Jan', 'Feb', 'Mar', 'Apr'],
        'sales': [100, 150, 120, 180]
    }
    df = pd.DataFrame(data)
    
    # 4つの選択肢を2x2で配置
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.write("**選択肢A**")
            with st.container(border=True):
                fig_a = px.bar(df, x='month', y='sales', 
                              title='Monthly Sales',
                              color='sales',
                              color_continuous_scale='Blues')
                fig_a.update_layout(height=300)
                st.plotly_chart(fig_a, use_container_width=True, key="chart_a")
        
        st.write("")
        
        with st.container():
            st.write("**選択肢C**")
            with st.container(border=True):
                fig_c = px.bar(df, x='month', y='sales', 
                              title='Monthly Sales',
                              color_discrete_sequence=['green'])
                fig_c.update_layout(height=300)
                st.plotly_chart(fig_c, use_container_width=True, key="chart_c")
    
    with col2:
        with st.container():
            st.write("**選択肢B**")
            with st.container(border=True):
                fig_b = px.line(df, x='month', y='sales', 
                               title='Monthly Sales',
                               markers=True)
                fig_b.update_layout(height=300)
                st.plotly_chart(fig_b, use_container_width=True, key="chart_b")
        
        st.write("")
        
        with st.container():
            st.write("**選択肢D**")
            with st.container(border=True):
                fig_d = px.pie(df, values='sales', names='month', 
                              title='Monthly Sales')
                fig_d.update_layout(height=300)
                st.plotly_chart(fig_d, use_container_width=True, key="chart_d")

    st.divider()
    st.subheader("回答")
    options = [
        "選択肢A",
        "選択肢B", 
        "選択肢C",
        "選択肢D"
    ]
    
    selected_answer = st.radio("正しいグラフデザインを選択してください:", options, key=f"{tab_name}_answer")
    
    return selected_answer


def process_answer(answer: str, state: dict, session: Session):
    # 正解は選択肢A: 青色グラデーション棒グラフ
    correct_answer = "選択肢A"
    
    if answer == correct_answer:
        state["is_clear"] = True
        st.success("**討伐成功！** 疾風の如く正確にグラフデザインを見抜いた！")
        st.balloons()
        st.write("**解説**: `px.bar()`で`color='sales'`と`color_continuous_scale='Blues'`を指定すると、売上値に応じた青色のグラデーション棒グラフが作成されます。各棒の色の濃さが売上値の大きさを表現します。")
    else:
        state["is_clear"] = False
        st.error("**討伐失敗！** グラフデザインを読み間違えた！再挑戦せよ！")
        st.write("**ヒント**: `color='sales'`と`color_continuous_scale='Blues'`の組み合わせがどのような視覚効果を生み出すかを考えてみよう。")

    save_table(state, session)


def run(tab_name: str, session: Session):
    state = init_state(tab_name, session)

    answer = present_quiz(tab_name)

    placeholder = st.empty()
    if placeholder.button("討伐開始", key=f"{tab_name}_submit"):
        if answer:
            process_answer(answer, state, session)
        else:
            st.warning("画面構成を選択してください")

    clear_submit_button(placeholder, state)