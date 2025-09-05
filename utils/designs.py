import streamlit as st


DEFAULT_TOP_TEXT_AREA = "custom-text-area"
DEFAULT_HEADER_ANIMATION_AREA = "custom-animation-header-area"
DEFAULT_PROBLEM_STATEMENT_AREA = "custom-problem-statement-area"


def apply_default_custom_css():
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Zen+Antique&display=swap" rel="stylesheet">
        <style>
        h1, h2, div, p {
            font-family: "Zen Antique", serif !important;
        }
        ."""
        + DEFAULT_TOP_TEXT_AREA
        + """ {
            background-color: #2b1810;
            padding: 20px;
            border-radius: 10px;
	@@ -28,45 +27,87 @@ def apply_default_custom_css():
            font-size: 16px;
            line-height: 1.6;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.3);  /* 炎のような光彩効果 */
        }
        ."""
        + DEFAULT_TOP_TEXT_AREA
        + """ h3 {
            color: #ffa07a;  /* 明るい橙色 */
            text-shadow: 2px 2px 4px rgba(139, 0, 0, 0.8);  /* 赤い影効果 */
        }
        ."""
        + DEFAULT_TOP_TEXT_AREA
        + """ strong {
            color: #ffffff;  /* 白い炎 */
        }
        ."""
        + DEFAULT_TOP_TEXT_AREA
        + """ p:last-child {
            margin-bottom: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    return DEFAULT_TOP_TEXT_AREA


def display_applied_message(message: str, css_name: str = DEFAULT_TOP_TEXT_AREA):
    if css_name == DEFAULT_TOP_TEXT_AREA:
        apply_default_custom_css()
    else:
        apply_default_custom_css()

    st.markdown(
        f"""
        <div class='{css_name}'>
        {message}
        """,
        unsafe_allow_html=True,
    )

@st.cache_data
def header_animation(
    css_name: str = DEFAULT_HEADER_ANIMATION_AREA,
    image_file: str = "pages/common/images/background.png",
) -> None:
    import base64

    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.html(
        f"""
        <div class="{css_name}">
            {"".join(['<div class="fireball"></div>' for _ in range(20)])}
        </div>
        <style>
        .{css_name} {{
            position: relative;
            overflow: hidden;
            background-color: rgba(0, 64, 128, 0.8);
            background-image: url(data:image/{"png"};base64,{encoded_string});
            margin: 0 calc(50% - 50vw);
            width: 100vw;
            height: 30px;
        }}
        .fireball {{
            position: absolute;
            background: radial-gradient(circle at center, #ff6600, #ff4500);
            border-radius: 50%;
            width: 10px;
            height: 10px;
            opacity: 0.9;
            box-shadow: 0 0 10px #ff4500, 0 0 20px #ff6600;
            animation: float 3s ease-in-out infinite;
        }}
        {" ".join([f'''
        .fireball:nth-child({i+1}) {{
            left: {5 * i}%;
            animation-delay: {0.15 * i}s;
        }}''' for i in range(20)])}
        @keyframes float {{
            0% {{
                bottom: -20px;
                transform: scale(1);
                filter: brightness(1);
            }}
            50% {{
                bottom: 20px;
                transform: scale(1.3);
                filter: brightness(1.2);
            }}
            100% {{
                bottom: -20px;
                transform: scale(1);
                filter: brightness(1);
            }}
        }}
        </style>
        """
    )


def display_problem_statement(
    html_message: str,
    css_name: str = DEFAULT_PROBLEM_STATEMENT_AREA,
    image_file: str = "pages/common/images/quest.jpeg",
):
    import base64

    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.html(
        f"""
        <p>
            <div class="{css_name}">
            {html_message}
            </div>
            <style>
            .{css_name} .box {{
                border-radius: 10px;
            }}
            .{css_name} {{
                background-color: rgba(2, 2, 2, 0);
                background-image: url(data:image/{"png"};base64,{encoded_string});
                background-position: top;
                padding: 40px 5%;
                color: #9e1717;
            }}
            </style>
        </p>
        """
    )

def display_problem_statement_swt25(
    html_message: str,
    css_name: str = DEFAULT_PROBLEM_STATEMENT_AREA
):
    
    st.html(
        f"""
        <p>
            <div class="{css_name}">
            {html_message}
            </div>
            <style>
            .{css_name} .box {{
                border-radius: 10px;
            }}
            .{css_name} {{
                background-color: rgba(128, 128, 128, 0.5);
                background-position: top;
                padding: 40px 5%;
                color: #ffffff;
            }}
            </style>
        </p>
        """
    )


@st.cache_data
def background_image(
    image_file: str = "pages/common/images/sky.png", dark_mode: bool = True
):
    import base64

    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    dark_mode_css = ""
    if dark_mode:
        dark_mode_css = """
            .main::before {
                background-color: rgba(0,0,0,0.4);
                position: fixed;
                top: 0;
                right: 0;
                bottom: 0;
                left: 0;
                content: ' ';
        }
        """

    st.markdown(
        f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url(data:image/{"png"};base64,{encoded_string});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    {dark_mode_css}
    .stApp > header {{
        display: none;
    }}
    .stAlert{{
        background-color: rgba(0, 0, 0, 0.4);
        border-radius: 0.5rem;
    }}
    .stAlert p, .stTabs button p{{
        color: #fff !important;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


DEFAULT_DEMON_ROW = "sf-demon-row"
DEFAULT_DEMON_AVATAR = "sf-demon-avatar"
DEFAULT_DEMON_BUBBLE = "sf-demon-bubble"

def apply_demon_ui_css():
    """鬼アバター用の最小CSS。既存のフォント指定を継承（font-familyは書かない）。"""
    st.markdown(
        """
        <style>
        .""" + DEFAULT_DEMON_ROW + """ {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin: .5rem 0;
        }
        .""" + DEFAULT_DEMON_AVATAR + """ {
            width: var(--avatar-size, 64px);
            height: var(--avatar-size, 64px);
            aspect-ratio: 1/1;
            object-fit: cover;
            border-radius: 10px;     /* 丸にしたいときは 50% */
            flex: 0 0 auto;
        }
        .""" + DEFAULT_DEMON_BUBBLE + """ {
            flex: 1 1 auto;
            min-width: 0;
            background-color: #2b1810;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #8b0000;
            border-left: 5px solid #ff4500;
            color: #ffffff;
            font-size: 16px;
            line-height: 1.6;
            box-shadow: 0 0 15px rgba(255,69,0,.3);
        }
        .""" + DEFAULT_DEMON_BUBBLE + """ p:last-child { margin-bottom: 0; }

        @media (max-width: 480px) {
            .""" + DEFAULT_DEMON_ROW + """ { gap: 8px; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    return DEFAULT_DEMON_ROW

def display_demon_message_html(
    html_message,
    avatar_image=None, 
    avatar_size=64,
    avatar_alt="avatar",
):
    apply_default_custom_css()
    apply_demon_ui_css()

    # 画像（任意）
    img_html = ""
    if avatar_image:
        import base64, mimetypes, os
        if os.path.exists(avatar_image):
            mime = mimetypes.guess_type(avatar_image)[0] or "image/png"
            with open(avatar_image, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            img_html = (
                "<img class='" + DEFAULT_DEMON_AVATAR + "' src='data:" + mime +
                ";base64," + b64 + "' alt='" + avatar_alt + "' />"
            )

    html = (
        "<div class='" + DEFAULT_DEMON_ROW + "' style='--avatar-size:" + str(avatar_size) + "px'>"
        + img_html +
        "<div class='" + DEFAULT_DEMON_BUBBLE + "'>"
        + html_message +
        "</div></div>"
    )
    st.markdown(html, unsafe_allow_html=True)