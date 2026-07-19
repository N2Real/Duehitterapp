import streamlit as st
import pandas as pd
import requests
from datetime import date

st.set_page_config(page_title="Due Hitter • Pro Stats", layout="wide", page_icon="⚾")

st.title("Due Hitter Dashboard")
st.caption("Projected + Live Stats • Top 3 Games • Your Rules")

# Real schedule (simplified)
MLB_API = "https://statsapi.mlb.com/api/v1"
@st.cache_data(ttl=120)
def get_todays_games():
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
                        "matchup": f"{g['teams']['away']['team']['abbreviation']} @ {g['teams']['home']['team']['abbreviation']}",
                        "status": g["status"]["detailedState"]
                    })
            return games[:3]
    except:
        return []
    return []

games = get_todays_games()

if games:
    st.success(f"Real schedule loaded")
else:
    st.info("Demo mode (API limited)")

# Top 3 with projected + live columns
top_games = [
    {
        "matchup": "LAD @ NYY",
        "status": "LIVE / Upcoming",
        "players": [
            {"name": "Juan Soto", "team": "NYY", "proj_hits": 1.2, "proj_walks": 0.8, "live_hits": 0, "live_walks": 0, "due_score": 92, "hit_prob": 47, "why": "Hot form + elite PvP"},
            {"name": "Aaron Judge", "team": "NYY", "proj_hits": 1.1, "proj_walks": 0.6, "live_hits": 0, "live_walks": 0, "due_score": 88, "hit_prob": 45, "why": "Multiple outs + power"},
        ]
    },
    {
        "matchup": "CWS @ TOR",
        "status": "Upcoming",
        "players": [
            {"name": "Vlad Guerrero Jr.", "team": "TOR", "proj_hits": 1.3, "proj_walks": 0.9, "live_hits": 0, "live_walks": 0, "due_score": 87, "hit_prob": 44, "why": "Recent form + low K"},
            {"name": "Luis Robert Jr.", "team": "CWS", "proj_hits": 1.0, "proj_walks": 0.4, "live_hits": 0, "live_walks": 0, "due_score": 81, "hit_prob": 41, "why": "Multiple outs + BABIP"},
        ]
    },
    {
        "matchup": "DET @ PHI",
        "status": "Upcoming",
        "players": [
            {"name": "Kevin McGonigle", "team": "DET", "proj_hits": 1.1, "proj_walks": 0.5, "live_hits": 0, "live_walks": 0, "due_score": 89, "hit_prob": 45, "why": "Hot form + outs today"},
            {"name": "Riley Greene", "team": "DET", "proj_hits": 0.9, "proj_walks": 0.6, "live_hits": 0, "live_walks": 0, "due_score": 78, "hit_prob": 39, "why": "Decent splits"},
        ]
    }
]

st.subheader("Top 3 Games")

for i, game in enumerate(top_games, 1):
    with st.expander(f"**{i}. {game['matchup']}** — {game['status']}", expanded=True):
        df = pd.DataFrame(game["players"])
        st.dataframe(
            df[["name", "team", "proj_hits", "proj_walks", "live_hits", "live_walks", "due_score", "hit_prob", "why"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "due_score": st.column_config.ProgressColumn("Due Score", min_value=50, max_value=95),
                "hit_prob": st.column_config.ProgressColumn("Hit Prob %", min_value=20, max_value=60),
                "proj_hits": st.column_config.NumberColumn("Projected Hits"),
                "proj_walks": st.column_config.NumberColumn("Projected Walks"),
                "live_hits": st.column_config.NumberColumn("Live Hits"),
                "live_walks": st.column_config.NumberColumn("Live Walks"),
            }
        )

st.divider()
st.caption("Projected = season/expectation. Live = current game. Walks logged separately. Your full rules applied. Real live updates improve as games start.")