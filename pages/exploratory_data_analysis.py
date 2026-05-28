import streamlit as st
import plotly.express as px


def eda_page():
    st.title("📊 Exploratory Data Analysis Dashboard")

    if 'processed_df' not in st.session_state:
        st.warning("Please upload and process a dataset first.")
        return

    df = st.session_state['processed_df'].copy()

    # Type safety
    if 'Cuisines' in df.columns:
        df['Cuisines'] = df['Cuisines'].astype(str)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cuisine Popularity")
        if 'Cuisines' in df.columns:
            cuisine_counts = (
                df['Cuisines']
                .str.split(',')
                .explode()
                .str.strip()
                .value_counts()
                .nlargest(10)
                .reset_index()
            )
            cuisine_counts.columns = ['Cuisine', 'Number of Restaurants']
            fig = px.bar(cuisine_counts, x='Cuisine', y='Number of Restaurants')
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Rating vs Average Cost")
        if all(col in df.columns for col in ['Average Cost for two', 'Aggregate rating', 'Price range']):
            fig = px.scatter(
                df,
                x='Average Cost for two',
                y='Aggregate rating',
                color='Price range'
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top Areas by Restaurant Count")
        if 'City' in df.columns:
            city_counts = df['City'].value_counts().nlargest(10).reset_index()
            city_counts.columns = ['City', 'Count']
            fig = px.pie(city_counts, names='City', values='Count')
            st.plotly_chart(fig, use_container_width=True)

      

    st.subheader("Votes vs Rating")
    if all(col in df.columns for col in ['Votes', 'Aggregate rating']):
        fig = px.scatter(df, x='Votes', y='Aggregate rating')
        st.plotly_chart(fig, use_container_width=True)
