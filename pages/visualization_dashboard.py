import streamlit as st
import pandas as pd
import plotly.express as px


def dashboard_page():
    """Page for the interactive visualization dashboard."""
    st.title("📈 Interactive Visualization Dashboard")

    if 'processed_df' not in st.session_state:
        st.warning("Please upload and process a dataset on the 'Data Upload' page first.")
        return

    df = st.session_state['processed_df']

    # --- Filters --- #
    with st.expander("**Adjust Dashboard Filters**", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            cities = st.multiselect("Select Areas", options=df['City'].unique(), default=df['City'].unique()[:5])
        with col2:
            unique_cuisines = df['Cuisines'].str.split(', ', expand=True).stack().unique()
            cuisines = st.multiselect("Select Cuisines", options=unique_cuisines, default=list(unique_cuisines)[:5])
        with col3:
            price_range = st.multiselect("Select Price Range", options=df['Price range'].unique(), default=df['Price range'].unique())

    # --- Filtered Dataframe --- #
    if not cities or not cuisines or not price_range:
        st.warning("Please select at least one option for each filter.")
        return

    filtered_df = df[
        df['City'].isin(cities) &
        df['Cuisines'].str.contains('|'.join(cuisines), na=False) &
        df['Price range'].isin(price_range)
    ]

    # --- Dashboard Layout --- #
    col1, col2 = st.columns((2, 1))

    with col1:
        with st.container():
            st.subheader("Filtered Data View")
            st.dataframe(filtered_df, height=500)
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Filtered Data", data=csv, file_name='filtered_zomato_data.csv', mime='text/csv')

    with col2:
        with st.container():
            st.subheader("Average Rating by Area")
            if not filtered_df.empty:
                avg_rating_city = filtered_df.groupby('City')['Aggregate rating'].mean().sort_values(ascending=False).reset_index()
                fig = px.bar(avg_rating_city, x='City', y='Aggregate rating', color='City', title='Average Rating by City')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data to display for the selected filters.")
        
        with st.container():
            st.subheader("Restaurant Count by Cuisine")
            if not filtered_df.empty:
                cuisine_counts = filtered_df['Cuisines'].str.split(', ', expand=True).stack().value_counts().nlargest(10).reset_index()
                cuisine_counts.columns = ['Cuisine', 'Count']
                fig2 = px.pie(cuisine_counts, names='Cuisine', values='Count', title='Top 10 Cuisines in Selected areas')
                st.plotly_chart(fig2, use_container_width=True)

