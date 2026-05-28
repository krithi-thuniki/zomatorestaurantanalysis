import streamlit as st
import pandas as pd
from utils.helpers import load_data


def data_upload_page():
    """Page for uploading and previewing the dataset with column mapping."""
    st.title("📤 Dataset Upload and Processing")

    # ------------------------
    # STEP 1: Upload
    # ------------------------
    st.header("Step 1: Upload Your Data")
    uploaded_file = st.file_uploader(
        "Choose a Zomato dataset CSV file",
        type="csv"
    )

    if uploaded_file is None:
        return

    df = load_data(uploaded_file)

    if df is None:
        st.error("Failed to load the dataset.")
        return

    st.session_state["df"] = df
    st.success("File uploaded successfully! Please proceed to Step 2.")

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📄 View Dataset Preview", expanded=True):
            st.dataframe(df.head())

    with col2:
        with st.expander("🧬 View Column Data Types", expanded=True):
            st.dataframe(df.dtypes.astype(str), use_container_width=True)

    # ------------------------
    # STEP 2: Mapping
    # ------------------------
    st.header("Step 2: Map and Clean Your Data")
    st.info(
        "💡 **Smart Mapping:** We've analyzed your file and pre-selected the best "
        "unique column for each field. Please review and confirm."
    )

    required_cols = {
        "Restaurant Name": "Restaurant Name",
        "Cuisines": "Cuisines",
        "City": "City",
        "Average Cost for two": "Average Cost for two",
        "Price range": "Price range",
        "Aggregate rating": "Aggregate rating",
        "Has Online delivery": "Has Online delivery",
        "Votes": "Votes"
    }

    def get_best_match(req_col, df, used_cols):
        numeric_required = [
            "Average Cost for two",
            "Aggregate rating",
            "Votes",
            "Price range"
        ]

        available_cols = [c for c in df.columns if c not in used_cols]
        if not available_cols:
            return df.columns[0]

        # Prefer numeric-heavy columns for numeric fields
        if req_col in numeric_required:
            best_col = None
            best_ratio = -1
            for col in available_cols:
                numeric_ratio = pd.to_numeric(
                    df[col], errors="coerce"
                ).notna().mean()
                if numeric_ratio > best_ratio:
                    best_ratio = numeric_ratio
                    best_col = col
            if best_ratio > 0.8:
                return best_col

        # Prefer string-heavy columns for text fields
        if req_col in ["Restaurant Name", "Cuisines", "City"]:
            string_cols = [
                col for col in available_cols
                if pd.to_numeric(df[col], errors="coerce").notna().mean() < 0.2
            ]
            if string_cols:
                return string_cols[0]

        # Fallback: name similarity
        return available_cols[0]

    mapped_cols = {}
    used_columns = set()
    mapping_layout = st.columns(3)

    for idx, (req_col, display_name) in enumerate(required_cols.items()):
        with mapping_layout[idx % 3]:
            best_match = get_best_match(req_col, df, used_columns)
            used_columns.add(best_match)

            mapped_cols[req_col] = st.selectbox(
                f"Map '{display_name}'",
                options=df.columns,
                index=list(df.columns).index(best_match),
                help=f"Suggested based on content/name: {best_match}"
            )

    # ------------------------
    # PROCESS DATA
    # ------------------------
    if st.button("🚀 Process and Analyze Data"):
        with st.spinner("Processing data..."):
            processed_df = df[list(mapped_cols.values())].copy()
            processed_df.columns = list(mapped_cols.keys())

            numeric_required = [
                "Average Cost for two",
                "Aggregate rating",
                "Votes",
                "Price range"
            ]

            cleaning_report = []

            for col in numeric_required:
                original_rows = len(processed_df)
                processed_df[col] = pd.to_numeric(
                    processed_df[col], errors="coerce"
                )
                processed_df.dropna(subset=[col], inplace=True)

                dropped = original_rows - len(processed_df)
                if dropped > 0:
                    cleaning_report.append(
                        f"- **{col}**: removed {dropped} invalid rows"
                    )

            st.session_state["processed_df"] = processed_df
            st.success("✅ Data processed and saved! Available across all pages.")

            if cleaning_report:
                with st.expander("🧹 Automatic Cleaning Report"):
                    for line in cleaning_report:
                        st.write(line)

            with st.expander("📊 Processed Data Preview", expanded=True):
                if processed_df.empty:
                    st.warning(
                        "⚠️ The processed dataset is empty. "
                        "Please check column mappings."
                    )
                else:
                    st.dataframe(processed_df.head())
