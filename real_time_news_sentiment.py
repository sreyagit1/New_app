# -*- coding: utf-8 -*-
"""
Real-Time News Sentiment Dashboard
Google RSS + VADER Sentiment Analysis
"""

import os
import uuid
import pandas as pd
import streamlit as st
import plotly.express as px
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

# ===================== CONFIG =====================
PRED_DIR = "predictions_parquet"
os.makedirs(PRED_DIR, exist_ok=True)

analyzer = SentimentIntensityAnalyzer()

# ===================== SENTIMENT (VADER) =====================
def classify_sentiment(df):
    if df.empty:
        return None

    sentiments = []
    prob_pos = []

    for title in df['title']:
        scores = analyzer.polarity_scores(title)

        if scores["compound"] >= 0.05:
            sentiments.append("Positive")
        elif scores["compound"] <= -0.05:
            sentiments.append("Negative")
        else:
            sentiments.append("Neutral")

        prob_pos.append(scores["pos"])

    df["sentiment"] = sentiments
    df["prob_pos"] = prob_pos

    # Save results
    fname = os.path.join(PRED_DIR, f"pred_{uuid.uuid4().hex}.parquet")
    df.to_parquet(fname, index=False)

    return df

# ===================== FETCH NEWS (GOOGLE RSS) =====================
def fetch_news(limit=20):
    rss_url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)

    rows = []
    for entry in feed.entries[:limit]:
        title = entry.get("title")
        link = entry.get("link")
        published = entry.get("published")

        try:
            published = pd.to_datetime(published)
        except:
            published = datetime.now()

        rows.append({
            "id": link,
            "source": "Google News",
            "title": title,
            "publishedAt": published
        })

    return pd.DataFrame(rows)

# ===================== STREAMLIT UI =====================
st.set_page_config(page_title="AI News Sentiment", layout="wide")
st.title("📰 Real-Time News Sentiment (Google RSS + VADER)")

if st.button("Fetch & Analyze Latest News"):
    df_new = fetch_news(20)
    out = classify_sentiment(df_new)

    if out is not None:
        st.success(f"Analyzed {len(out)} headlines with VADER")
    else:
        st.warning("No headlines fetched")

# ===================== LOAD SAVED DATA =====================
def load_recent(n=200):
    import glob
    files = sorted(
        glob.glob(os.path.join(PRED_DIR, "*.parquet")),
        key=os.path.getmtime,
        reverse=True
    )[:30]

    if not files:
        return pd.DataFrame(columns=["id","source","title","publishedAt","sentiment","prob_pos"])

    df = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    df = df.drop_duplicates(subset=['id'])

    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    df['publishedAt'] = df['publishedAt'].fillna(datetime.now())

    return df.sort_values('publishedAt', ascending=False).head(n)

df = load_recent()

# ===================== DISPLAY DATA =====================
st.subheader("Latest Headlines")
st.dataframe(
    df[['publishedAt','source','title','sentiment','prob_pos']]
    .rename(columns={'title':'headline'}),
    height=350
)

# ===================== CHARTS =====================
col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Sentiment Distribution")
    if not df.empty:
        counts = df['sentiment'].value_counts().rename_axis('sentiment').reset_index(name='count')
        fig = px.bar(counts, x='sentiment', y='count', color='sentiment')
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Positive Sentiment Trend")
    if not df.empty:
        df_sorted = df.sort_values('publishedAt')
        st.line_chart(df_sorted.set_index('publishedAt')['prob_pos'])

st.markdown(f"**Last updated:** {pd.Timestamp.now()}")
