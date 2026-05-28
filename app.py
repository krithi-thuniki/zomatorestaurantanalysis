import streamlit as st
#
#  ---- ROLE RESET / LOGOUT ----
if "role" in st.session_state:
    with st.sidebar:
        if st.button("🔄 Switch Role"):
            del st.session_state["role"]
            st.rerun()


st.set_page_config(
    page_title="Zomato Restaurant Analytics",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- ROLE SELECTION ----------------
if "role" not in st.session_state:
    st.title("🍽️ Zomato Restaurant Analytics")
    st.markdown("### Select your role to proceed")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("👨‍💼 Admin"):
            st.session_state.role = "admin"
            st.rerun()
    with col2:
        if st.button("👤 User"):
            st.session_state.role = "user"
            st.rerun()

# ---------------- AFTER ROLE SELECTION ----------------
else:
    role = st.session_state.role

    if role == "admin":
        st.sidebar.title("Admin Navigation")
        page = st.sidebar.radio(
            "Go to",
            ["Data Upload", "Machine Learning Predictions"]
        )

        if page == "Data Upload":
            from pages import data_upload
            data_upload.data_upload_page()

        elif page == "Machine Learning Predictions":
            from pages import machine_learning_predictions
            machine_learning_predictions.ml_predictions_page()

    elif role == "user":
        st.sidebar.title("User Navigation")
        page = st.sidebar.radio(
            "Go to",
            ["EDA Dashboard", "Visualization Dashboard", "The Best Restaurant For You"]  # ✅ Added page
        )

        if page == "EDA Dashboard":
            from pages import exploratory_data_analysis
            exploratory_data_analysis.eda_page()

        elif page == "Visualization Dashboard":
            from pages import visualization_dashboard
            visualization_dashboard.dashboard_page()

        elif page == "The Best Restaurant For You":
            from pages.best_restaurant import best_restaurant_page
            best_restaurant_page()   # ✅ call directly

