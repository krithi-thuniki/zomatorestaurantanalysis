import streamlit as st
import plotly.express as px
import pandas as pd


def best_restaurant_page():
    st.title("🍴 The Best Restaurant For You")
    st.caption("Recommendations based on trained datasets")

    # ------------------------
    # Dataset availability
    # ------------------------
    if "processed_df" not in st.session_state:
        st.error("❌ Dataset not available. Please ask Admin to upload and process data first.")
        return

    df = st.session_state["processed_df"].copy()

    # ------------------------
    # Required columns check
    # ------------------------
    required_cols = [
        "Restaurant Name",
        "City",
        "Cuisines",
        "Aggregate rating",
        "Votes"
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"❌ Missing required columns: {missing}")
        return

    # ------------------------
    # Type safety
    # ------------------------
    df["Restaurant Name"] = df["Restaurant Name"].astype(str)
    df["City"] = df["City"].astype(str)
    df["Cuisines"] = df["Cuisines"].astype(str)
    df["Aggregate rating"] = pd.to_numeric(df["Aggregate rating"], errors="coerce")
    df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce")
    df = df.dropna(subset=["Aggregate rating", "Votes"])

    # ------------------------
    # HARD SAFETY CHECK (Cuisine column)
    # ------------------------
    if df["Cuisines"].str.replace(".", "", regex=False).str.isnumeric().all():
        st.error(
            "❌ Cuisines column contains numeric values.\n\n"
            "Please go to **Admin → Dataset Upload** and remap columns correctly."
        )
        return

    # ------------------------
    # DATA SANITY FILTERS (CRITICAL FIX)
    # ------------------------
    df = df[
        (df["Aggregate rating"] >= 0) &
        (df["Aggregate rating"] <= 5) &
        (df["Votes"] >= 0) &
        (df["Votes"] <= 100000)
    ]

    if df.empty:
        st.error("❌ No valid data left after sanity filtering. Dataset mapping is incorrect.")
        return

    # ------------------------
    # Filters
    # ------------------------
    cities = sorted(df["City"].unique())
    cuisines = sorted({
        c.strip()
        for x in df["Cuisines"].str.split(",")
        for c in x if c.strip()
    })

    col1, col2, col3 = st.columns([3, 3, 2])
    with col1:
        city = st.selectbox("📍 Select City", cities)
    with col2:
        cuisine = st.selectbox("🍽️ Select Cuisine", cuisines)
    with col3:
        if st.button("🔄 Reset"):
            st.rerun()

    # ------------------------
    # PRIMARY FILTER (City + Cuisine)
    # ------------------------
    filtered = df[
        (df["City"] == city) &
        (df["Cuisines"].str.contains(cuisine, case=False, na=False))
    ]

    source_label = city

    # ------------------------
    # FALLBACK → NEARBY AREAS
    # ------------------------
    if filtered.empty:
        nearby_df = df[df["Cuisines"].str.contains(cuisine, case=False, na=False)]

        if nearby_df.empty:
            st.warning(f"⚠️ No restaurants found serving **{cuisine}**.")
            return

        nearby_areas = nearby_df["City"].unique()[:5]
        source_label = ", ".join(nearby_areas)

        st.info(
            f"ℹ️ **{cuisine}** cuisine not found in **{city}**.\n\n"
            f"Showing top **{cuisine}** restaurants from nearby areas:\n"
            f"**{source_label}**"
        )
        filtered = nearby_df

    # ------------------------
    # AGGREGATE RESTAURANTS (FIXED)
    # ------------------------
   # ------------------------
# AGGREGATE RESTAURANTS (FIXED PROPERLY)
# ------------------------
    aggregated = (
        filtered
        .groupby(["Restaurant Name", "City", "Cuisines"], as_index=False)
        .agg({
            "Aggregate rating": "mean",
            "Votes": "mean"
        })
    )

    # ------------------------
    # FINAL SANITY CHECK
    # ------------------------
    if aggregated["Aggregate rating"].max() > 5:
        st.error("❌ Rating values exceed 5. Dataset mapping is incorrect.")
        return

    if aggregated["Votes"].max() > 100000:
        st.error("❌ Votes values are unrealistically high. Dataset mapping is incorrect.")
        return

    # ------------------------
    # SCORING LOGIC
    # ------------------------
    max_votes = aggregated["Votes"].max()
    aggregated["Votes_norm"] = aggregated["Votes"] / max_votes if max_votes > 0 else 0

    aggregated["Score"] = (
        aggregated["Aggregate rating"] * 0.7 +
        aggregated["Votes_norm"] * 0.3
    )

    top_restaurants = (
        aggregated
        .sort_values("Score", ascending=False)
        .head(4)
        .reset_index(drop=True)
    )

    # ------------------------
    # BEST RESTAURANT
    # ------------------------
    best = top_restaurants.iloc[0]

    st.markdown("## 🌟 Best Restaurant For You")
    st.success(
    f"""
    **{best['Restaurant Name']}**  
    📍 Area: **{best['City']}**  
    🍽️ Cuisine: **{best['Cuisines']}**  
    ⭐ Rating: **{round(best['Aggregate rating'], 2)}**  
    👍 Votes: **{int(best['Votes'])}**

    **Why?** Highest combined score based on rating and popularity.
    """
)

    st.divider()

    # ------------------------
    # OTHER TOP PICKS
    # ------------------------
    # ------------------------
# OTHER TOP PICKS
# ------------------------
    # ------------------------
    # OTHER TOP PICKS
    # ------------------------
    st.markdown("## 🏆 Other Top Recommendations")

    for _, row in top_restaurants.iloc[1:].iterrows():
        st.markdown(
            f"**{row['Restaurant Name']}**  \n"
            f"📍 {row['City']}  \n"
            f"🍽️ {row['Cuisines']}  \n"
            f"⭐ {round(row['Aggregate rating'], 2)} | 👍 {int(row['Votes'])}"
        )
        st.divider()

    # ------------------------
    # VISUALIZATION
    # ------------------------
    fig = px.bar(
        top_restaurants,
        x="Restaurant Name",
        y="Score",
        color="City",
        title=f"Top {cuisine} Restaurants ({source_label})"
    )

    st.plotly_chart(fig, width="stretch")