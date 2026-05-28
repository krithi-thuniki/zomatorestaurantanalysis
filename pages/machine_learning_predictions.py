import streamlit as st
from utils.ml_models import train_and_save_model, train_and_save_autogluon_model

def ml_predictions_page():
    st.title("🤖 Machine Learning Predictions")

    if 'processed_df' not in st.session_state:
        st.warning("Please upload and process a dataset on the 'Data Upload' page first.")
        return

    df = st.session_state['processed_df']

    # Default success thresholds (used internally for training)
    success_rating_threshold = 4.0
    success_votes_threshold = 500

    # --------------------------
    # Training Button
    # --------------------------
    if 'training_done' not in st.session_state:
        st.session_state.training_done = False

    if not st.session_state.training_done:
        if st.button("Train and Save Models"):
            with st.spinner("Training models... Please wait."):
                # Train all models
                _, msg1 = train_and_save_model(df, 'rating')
                _, msg2 = train_and_save_model(df, 'success', success_rating_threshold, success_votes_threshold)
                _, msg3 = train_and_save_model(df, 'price_range')
                _, msg4 = train_and_save_autogluon_model(df, 'success', success_rating_threshold, success_votes_threshold)
                
                # Mark training done
                st.session_state.training_done = True
                st.success("All models trained and saved successfully!")
    else:
        st.success("All models are already trained and saved!")
