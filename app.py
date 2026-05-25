import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(page_title="🎬 Page to Screen", layout="wide", page_icon="🎬")

# ── Custom CSS (영화 느낌의 다크 테마) ────────────────────────
st.markdown("""
<style>
    .big-title {
        font-size: 3rem; font-weight: 900; text-align: center;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #e11d48);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .subtitle { text-align: center; color: #94a3b8; margin-bottom: 30px; }
    div[data-testid="stMetric"] {
        background: #111827; border: 1px solid #374151;
        border-radius: 15px; padding: 20px; box-shadow: 2px 2px 15px rgba(0,0,0,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ── Session State & Data (샘플 데이터) ─────────────────────────
if "adaptations" not in st.session_state:
    st.session_state.adaptations = [
        {"Title": "Gone Girl", "Genre": "Crime", "Book_Rating": 4.1, "Movie_Rating": 87, "Box_Office": 369000000, "Book_Year": 2012, "Movie_Year": 2014},
        {"Title": "The Silence of the Lambs", "Genre": "Crime", "Book_Rating": 4.2, "Movie_Rating": 95, "Box_Office": 272000000, "Book_Year": 1988, "Movie_Year": 1991},
        {"Title": "The Godfather", "Genre": "Crime", "Book_Rating": 4.3, "Movie_Rating": 98, "Box_Office": 243000000, "Book_Year": 1969, "Movie_Year": 1972},
        {"Title": "Harry Potter", "Genre": "Fantasy", "Book_Rating": 4.4, "Movie_Rating": 89, "Box_Office": 974000000, "Book_Year": 1997, "Movie_Year": 2001},
        {"Title": "Dune", "Genre": "Sci-Fi", "Book_Rating": 4.2, "Movie_Rating": 90, "Box_Office": 402000000, "Book_Year": 1965, "Movie_Year": 2021},
        {"Title": "Jurassic Park", "Genre": "Sci-Fi", "Book_Rating": 4.0, "Movie_Rating": 93, "Box_Office": 1046000000, "Book_Year": 1990, "Movie_Year": 1993},
        {"Title": "The Girl with the Dragon Tattoo", "Genre": "Crime", "Book_Rating": 4.1, "Movie_Rating": 86, "Box_Office": 232000000, "Book_Year": 2005, "Movie_Year": 2011}
    ]

df = pd.DataFrame(st.session_state.adaptations)
df["Time_Gap"] = df["Movie_Year"] - df["Book_Year"]

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.header("🎛️ Filter Adaptations")
    selected_genres = st.multiselect("Select Genre", options=df["Genre"].unique(), default=df["Genre"].
