import streamlit as st
import pandas as pd
import plotly.express as px

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(page_title="🎬 Page to Screen", layout="wide", page_icon="🎬")

# ── Custom CSS ────────────────────────
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

# ── Session State & Data ─────────────────────────
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
    selected_genres = st.multiselect("Select Genre", options=df["Genre"].unique(), default=df["Genre"].unique())
    min_box_office = st.slider("Minimum Box Office ($M)", 0, 1500, 0, step=50)

# Filter Logic
filtered_df = df[(df["Genre"].isin(selected_genres)) & (df["Box_Office"] >= min_box_office * 1000000)]

# ── Main UI ──────────────────────────────────────────────────
st.markdown('<p class="big-title">🎬 From Page to Screen</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Adaptation Audience Retention & Financial ROI Dashboard</p>', unsafe_allow_html=True)

# Metrics Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Adaptations Analyzed", len(filtered_df))
m2.metric("Total Box Office", f"${filtered_df['Box_Office'].sum() / 1e9:.2f}B")
m3.metric("Avg Audience Score", f"{filtered_df['Movie_Rating'].mean():.1f}/100")
m4.metric("Avg Development Gap", f"{filtered_df['Time_Gap'].mean():.1f} Years")

st.markdown("---")

# ── Charts ───────────────────────────────────────────────────
st.subheader("⚖️ The Critical Divide: Book vs. Movie")
fig_scatter = px.scatter(
    filtered_df, x="Book_Rating", y="Movie_Rating", size="Box_Office", color="Genre",
    hover_name="Title", size_max=40, template="plotly_dark",
    labels={"Book_Rating": "Goodreads Rating (1-5)", "Movie_Rating": "TMDB Audience Score (1-100)"}
)
st.plotly_chart(fig_scatter, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("⏳ Development Gap vs Box Office")
    fig_bar = px.bar(
        filtered_df, x="Title", y="Box_Office", color="Time_Gap",
        color_continuous_scale="Reds", template="plotly_dark",
        labels={"Box_Office": "Box Office Revenue ($)", "Time_Gap": "Years to Screen"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("💰 Financial ROI by Genre")
    fig_donut = px.pie(
        filtered_df, names="Genre", values="Box_Office", hole=0.4,
        template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.subheader("📋 Core Dataset")
st.dataframe(
    filtered_df,
    column_config={
        "Box_Office": st.column_config.NumberColumn("Global Box Office (USD)", format="$%d"),
    },
    use_container_width=True, hide_index=True
)

st.markdown("---")
st.markdown('<div style="text-align:center; color:#94a3b8; font-size:0.9rem;">Film & Media Analysis — Final Project Dashboard</div>', unsafe_allow_html=True)
