from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from vice_intel.sentiment import analyze_sentiment

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "demo" / "gta6_sentiment_sample.csv"

st.set_page_config(
    page_title="VICE INTEL | GTA VI Intelligence Hub",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load synthetic GTA VI demo reactions."""
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


df = load_data()

# Page heading
st.title("🌴 VICE INTEL")
st.subheader("GTA VI Intelligence & Analytics Platform")

st.info(
    "DEMO MODE: This dashboard uses fictional example reactions, "
    "not real GTA VI community data."
)

st.divider()

# Sidebar filters
st.sidebar.title("🎮 VICE INTEL")
st.sidebar.markdown("### Filters")

selected_sentiments = st.sidebar.multiselect(
    "Select sentiment",
    options=["positive", "neutral", "negative"],
    default=["positive", "neutral", "negative"],
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Apply filters
filtered_df = df[df["sentiment"].isin(selected_sentiments)].copy()

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = filtered_df[filtered_df["date"].dt.date.between(start_date, end_date)]
elif isinstance(selected_dates, tuple):
    st.sidebar.info("Select an end date to complete the range.")
    filtered_df = filtered_df.iloc[0:0]

# Calculate analytics from filtered data
summary = analyze_sentiment(filtered_df)

total_reactions = len(filtered_df)

positive_pct = summary.loc[summary["sentiment"] == "positive", "percentage"].iloc[0]

neutral_pct = summary.loc[summary["sentiment"] == "neutral", "percentage"].iloc[0]

negative_pct = summary.loc[summary["sentiment"] == "negative", "percentage"].iloc[0]

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Reactions", total_reactions)
col2.metric("Positive", f"{positive_pct:.1f}%")
col3.metric("Neutral", f"{neutral_pct:.1f}%")
col4.metric("Negative", f"{negative_pct:.1f}%")

st.divider()

# Sentiment chart
st.header("📊 Sentiment Distribution")

fig = px.bar(
    summary,
    x="sentiment",
    y="count",
    color="sentiment",
    color_discrete_map={
        "positive": "#F0D393",
        "neutral": "#9FB8D0",
        "negative": "#E58C91",
    },
    labels={
        "sentiment": "Sentiment",
        "count": "Number of Reactions",
    },
    title="GTA VI Demo Sentiment Breakdown",
)

fig.update_layout(
    plot_bgcolor="#1A3E65",
    paper_bgcolor="#1A3E65",
    font_color="#F5F1E8",
    showlegend=False,
)

st.plotly_chart(fig, width="stretch")

# Sentiment trends over time
st.subheader("📈 Sentiment Trends Over Time")

if filtered_df.empty:
    st.info("No trend data available for the selected filters.")
else:
    daily_sentiment = (
        filtered_df.groupby([pd.Grouper(key="date", freq="D"), "sentiment"])
        .size()
        .reset_index(name="count")
    )

    trend_fig = px.line(
        daily_sentiment,
        x="date",
        y="count",
        color="sentiment",
        markers=True,
        color_discrete_map={
            "positive": "#F0D393",
            "neutral": "#9FB8D0",
            "negative": "#E58C91",
        },
        labels={
            "date": "Date",
            "count": "Number of Reactions",
            "sentiment": "Sentiment",
        },
    )

    trend_fig.update_layout(
        plot_bgcolor="#1A3E65",
        paper_bgcolor="#1A3E65",
        font_color="#F5F1E8",
        hovermode="x unified",
    )

    st.plotly_chart(trend_fig, width="stretch")

st.divider()

# Reactions table
st.header("🔎 Explore Community Reactions")

if filtered_df.empty:
    st.warning(
        "No reactions match your selected filters. "
        "Try changing the sentiment or date range."
    )
else:
    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True,
    )

st.caption(f"Showing {len(filtered_df)} of {len(df)} synthetic demo reactions.")

# Download filtered dataset
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Reactions (CSV)",
    data=csv_data,
    file_name="vice_intel_filtered_reactions.csv",
    mime="text/csv",
    disabled=filtered_df.empty,
)

st.divider()

st.markdown("**VICE INTEL** | Open-source GTA VI Data Science Platform")
