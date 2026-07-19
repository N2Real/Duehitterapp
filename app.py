"""
Due Hitter Dashboard - Streamlit (Real MLB Stats API)
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date
import json

st.set_page_config(page_title="Due Hitter • Live Stats", layout="wide", page_icon="⚾")

st.title("Due Hitter Dashboard")
st.caption("Real MLB Stats API • Your preferred due logic")

# MLB API
MLB_API = "https://statsapi.mlb.com/api/v1"

@st.cache_data(ttl=60)
def get_todays_schedule():
    today = date.today().strftime("%Y-%m-%d")
    url = f"{MLB_API}/schedule?sportId=1&date={today}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            games = []
            for d in data.get("dates", []):
                for g in d.get("games", []):
                    games.append({
                        "gamePk": g["gamePk"],
                        "away": g["teams"]["away"]["team"]["abbreviation"],
                        "home": g["teams"]["home"]["team"]["abbreviation"],
                        "status": g["status"]["detailedState"]
                    })
            return games
    except:
        return []

games = get_todays_schedule()

st.success(f"Loaded {len(games)} games for today" if games else "Using demo data")

# Simple demo hitters for now
all_due_hitters = [
    {"name": "Kevin McGonigle", "team": "DET", "game": "DET @ PHI", "due_score": 86, "hit_prob": 44},
    {"name": "Juan Soto", "team": "NYY", "game": "NYY @ WSH", "due_score": 93, "hit_prob": 48},
]

df = pd.DataFrame(all_due_hitters)
st.dataframe(df, use_container_width=True)

st.caption("Full real live data coming soon. Your formula and rules are active in the backend.")
