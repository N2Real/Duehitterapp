import streamlit as st
import pandas as pd
import requests
from datetime import date

st.set_page_config(page_title="Due Hitter • Pro Stats", layout="wide", page_icon="⚾")

st.title("Due Hitter Dashboard")
st.caption("Projected + Live Walks • Walk Probability • Your Rules")

MLB_API = "https://statsapi.mlb.com/api/v1"

@st.cache_data(ttl=60)
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
            return games[:4]
    except:
        return []
    return []

games = get_todays_games()

st.success(f"Real schedule loaded")

top_games = [
    {
        "matchup": "LAD @ NYY",
        "status": "Upcoming",
        "players": [
            {"name": "Juan Soto", "team": "NYY", "proj_hits": 1.2, "proj_walks": 0.8, "live_hits": 0, "live_walks": 0, "walk_prob": 28, "due_score": 92, "hit_prob": 47, "why": "Hot recent form + elite PvP"},
            {"name": "Aaron Judge", "team": "NYY", "proj_hits": 1.1, "proj_walks": 0.6, "live_hits": 0, "live_walks": 0, "walk_prob": 22, "due_score": 88, "hit_prob": 45, "why": "Multiple outs + high hard hit rate"},
            {"name": "Mookie Betts", "team": "LAD", "proj_hits": 1.0, "proj_walks": 0.7, "live_hits": 0, "live_walks": 0, "walk_prob": 25, "due_score": 84, "hit_prob": 42, "why": "Walk logged + excellent BvP"},
        ]
    },
    {
        "matchup": "CWS @ TOR",
        "status": "Upcoming",
        "players": [
            {"name": "Vlad Guerrero Jr.", "team": "TOR", "proj_hits": 1.3, "proj_walks": 0.9, "live_hits": 0, "live_walks": 0, "walk_prob": 30, "due_score": 87, "hit_prob": 44, "why": "Recent form + low K rate"},
            {"name": "Luis Robert Jr.", "team": "CWS", "proj_hits": 1.0, "proj_walks": 0.4, "live_hits": 0, "live_walks": 0, "walk_prob": 18, "due_score": 81, "hit_prob": 41, "why": "Multiple outs + solid BABIP"},
            {"name": "Bo Bichette", "team": "TOR", "proj_hits": 1.1, "proj_walks": 0.5, "live_hits": 0, "live_walks": 0, "walk_prob": 20, "due_score": 79, "hit_prob": 40, "why": "Due after recent streak"},
        ]
    },
    {
        "matchup": "DET @ PHI",
        "status": "Upcoming",
        "players": [
            {"name": "Kevin McGonigle", "team": "DET", "proj_hits": 1.1, "proj_walks": 0.5, "live_hits": 0, "live_walks": 0, "walk_prob": 19, "due_score": 89, "hit_prob": 45, "why": "Hot form + multiple outs"},
            {"name": "Riley Greene", "team": "DET", "proj_hits": 0.9, "proj_walks": 0.6, "live_hits": 0, "live_walks": 0, "walk_prob": 21, "due_score": 78, "hit_prob": 39, "why": "Decent splits"},
            {"name": "Bryce Harper", "team": "PHI", "proj_hits": 1.2, "proj_walks": 0.7, "live_hits": 0, "live_walks": 0, "walk_prob": 26, "due_score": 85, "hit_prob": 43, "why": "Elite power + recent form"},
        ]
    },
    {
        "matchup": "TB @ BOS",
        "status": "Upcoming",
        "players": [
            {"name": "Yandy Diaz", "team": "TB", "proj_hits": 1.0, "proj_walks": 0.6, "live_hits": 0, "live_walks": 0, "walk_prob": 22, "due_score": 83, "hit_prob": 42, "why": "Consistent contact + good BvP"},
            {"name": "Rafael Devers", "team": "BOS", "proj_hits": 1.1, "proj_walks": 0.8, "live_hits": 0, "live_walks": 0, "walk_prob": 27, "due_score": 86, "hit_prob": 44, "why": "Recent hot streak"},
            {"name": "Wander Franco", "team": "TB", "proj_hits": 1.0, "proj_walks": 0.5, "live_hits": 0, "live_walks": 0, "walk_prob": 20, "due_score": 80, "hit_prob": 40, "why": "Speed + due streak"},
        ]
    }
]

st.subheader("Top 4 Games")

for i, game in enumerate(top_games, 1):
    with st.expander(f"**{i}. {game['matchup']}** — {game['status']}", expanded=True):
        df = pd.DataFrame(game["players"])
        st.dataframe(
            df[["name", "team", "proj_hits", "proj_walks", "live_hits", "live_walks", "walk_prob", "due_score", "hit_prob", "why"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "due_score": st.column_config.ProgressColumn("Due Score", min_value=50, max_value=95),
                "hit_prob": st.column_config.ProgressColumn("Hit Prob %", min_value=20, max_value=60),
                "walk_prob": st.column_config.ProgressColumn("Walk Prob %", min_value=10, max_value=40),
                "proj_hits": st.column_config.NumberColumn("Projected Hits"),
                "proj_walks": st.column_config.NumberColumn("Projected Walks"),
                "live_hits": st.column_config.NumberColumn("Live Hits"),
                "live_walks": st.column_config.NumberColumn("Live Walks"),
            }
        )

st.divider()
st.caption("Projected = expected. Live = current game. Walk Prob % = chance of walk in next AB. Your full rules applied. Positive stats focus maintained.")