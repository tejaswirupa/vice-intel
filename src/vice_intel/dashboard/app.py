from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from vice_intel.sentiment import analyze_sentiment

# Find the project folder regardless of terminal location.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "demo" / "gta6_sentiment_sample.csv"

# Configure the page before displaying anything.
st.set_page_config(
    page_title="VICE INTEL | GTA VI Intelligence Hub",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load our synthetic GTA VI demo dataset."""
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


df = load_data()

# Main heading
st.title("🌴 VICE INTEL")
st.subheader("GTA VI Intelligence & Analytics Platform")

st.info(
    "DEMO MODE: This dashboard uses synthetic example reactions, "
    "not real GTA VI community data."
)

st.divider()

# Sentiment analysis
summary = analyze_sentiment(df)

total_reactions = len(df)

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

# Interactive sentiment chart
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

st.divider()

# Sidebar controls
st.sidebar.title("🎮 VICE INTEL")
st.sidebar.markdown("### Filters")

selected_sentiments = st.sidebar.multiselect(
    "Select sentiment",
    options=["positive", "neutral", "negative"],
    default=["positive", "neutral", "negative"],
)

filtered_df = df[df["sentiment"].isin(selected_sentiments)]

# Dataset explorer
st.header("🔎 Explore Community Reactions")

if filtered_df.empty:
    st.warning(
        "No reactions match your selected filters. "
        "Please select at least one sentiment."
    )
else:
    st.dataframe(
        filtered_df,
        width="stretch",
        hide_index=True,
    )

st.caption(f"Showing {len(filtered_df)} of {len(df)} synthetic demo reactions.")

st.divider()

st.markdown("**VICE INTEL** | Open-source GTA VI Data Science Platform")
