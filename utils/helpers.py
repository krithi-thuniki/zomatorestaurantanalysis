import pandas as pd
import streamlit as st


def load_data(uploaded_file):
    """
    Robust CSV loader with encoding fallback.
    """
    encodings = ["utf-8", "latin1", "ISO-8859-1", "cp1252"]

    for enc in encodings:
        try:
            df = pd.read_csv(uploaded_file, encoding=enc)

            # Clean column names
            df.columns = df.columns.str.strip()

            # Strip string values
            for col in df.select_dtypes(include="object"):
                df[col] = df[col].astype(str).str.strip()

            st.info(f"✅ File loaded successfully using **{enc}** encoding.")
            return df

        except UnicodeDecodeError:
            continue
        except Exception as e:
            st.error(f"❌ Unexpected error while reading file: {e}")
            return None

    st.error(
        "❌ Failed to decode the CSV file.\n\n"
        "Tried encodings: utf-8, latin1, ISO-8859-1, cp1252.\n"
        "Please re-save the file as UTF-8 and try again."
    )
    return None
