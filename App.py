import streamlit as st
from dashboards import init_da_state, show_dashboard
import base64


# ---------------------------------------------------
# LOAD LOGO
# ---------------------------------------------------
def load_logo():
    try:
        with open("assets/logo.png", "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None


# ---------------------------------------------------
# SESSION INITIALIZATION
# ---------------------------------------------------
def init_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "role" not in st.session_state:
        st.session_state.role = None


# ---------------------------------------------------
# LOGIN SCREEN
# ---------------------------------------------------
def login_screen():
    # ========== GLOBAL CSS ==========
    st.markdown(
        """
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}

            .block-container {
                padding-top: 40px !important;
                max-width: 500px !important;
            }

            .marketpulse-title {
                text-align: center;
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 30px;
                color: #111827;
            }

            .stTextInput>div>div>input {
                padding: 14px;
                border-radius: 10px;
                background: #f9fafb;
                border: 1px solid #e5e7eb;
            }

            .stSelectbox>div>div {
                padding: 12px;
                border-radius: 10px;
                background: #f9fafb;
                border: 1px solid #e5e7eb;
            }

            .stButton>button {
                width: 100%;
                background: linear-gradient(135deg, #c084fc 0%, #a855f7 100%);
                color: white;
                padding: 12px 18px;
                border-radius: 10px;
                font-size: 16px;
                border: none;
                font-weight: 600;
                margin-top: 20px;
            }

            .stButton>button:hover {
                background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ========== LOGO ==========
    logo_data = load_logo()
    if logo_data:
        st.markdown(
            f"""
            <div style='text-align:center; margin-bottom: 20px;'>
                <img src="data:image/png;base64,{logo_data}" width="140" style="margin-bottom:10px;">
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========== TITLE ==========
    st.markdown("<div class='marketpulse-title'>MarketPulse</div>", unsafe_allow_html=True)

    # ========== WELCOME TEXT ==========
    st.markdown(
        """
        ### Welcome back
        <p style='color:#6b7280; font-size:14px; margin-top:-10px;'>
            New to MarketPulse?
            <a href='#' style='color:#a855f7;'>Create an account.</a>
        </p>
        """,
        unsafe_allow_html=True,
    )

    # ========== FORM ==========
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    role = st.selectbox(
        "Role",
        ["Select role", "Manager", "Marketing Analyst", "Data Analyst", "Employee", "Admin"],
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        remember = st.checkbox("Remember for 30 days")
    with col2:
        st.markdown(
            """
            <div style='text-align:right; margin-top: 10px;'>
                <a href='#' style='color:#a855f7; font-size:14px;'>Forgot password</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========== SUBMIT BUTTON ==========
    valid = email.strip() and password.strip() and role != "Select role"

    if st.button("Sign in", disabled=not valid):
        st.session_state.logged_in = True
        st.session_state.role = role
        st.rerun()


# ---------------------------------------------------
# MAIN ROUTER
# ---------------------------------------------------
def main():
    init_session()

    if not st.session_state.logged_in:
        login_screen()
        init_da_state()
        st.stop()   # IMPORTANT: Stops rendering anything below

    # Logged in → Show dashboard
    show_dashboard()


# ---------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(page_title="MarketPulse", page_icon="📊", layout="wide")
    main()
