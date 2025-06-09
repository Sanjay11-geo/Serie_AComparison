import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import requests

# --- Streamlit page setup ---
st.set_page_config(page_title="Serie A Team Comparison", layout="wide")

# --- Custom CSS for dark theme ---
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #232526, #414345);
    color: white;
}
.stApp {
    background: linear-gradient(to right, #232526, #414345);
}
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 1rem;
}
h1, h2, h3 {
    color: white !important;
}
.stSelectbox > div > div {
    background-color: rgba(255, 255, 255, 0.1);
    color: white;
}
div[data-testid="metric-container"] {
    background: linear-gradient(45deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02));
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1rem;
    border-radius: 10px;
    backdrop-filter: blur(5px);
}
div[data-testid="metric-container"] > div > div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("⚔️ Serie A 2022–23 Team Comparison Dashboard")

# --- Load data ---
file_path = r"C:\Users\USER\OneDrive\Desktop\myfirstjupy\DS\2022-2023 Football Player Stats.csv"
df = pd.read_csv(file_path, encoding="ISO-8859-1", sep=";")

# --- Filter Serie A teams ---
serie_a_df = df[df["Comp"] == "Serie A"]
serie_a_teams = sorted(serie_a_df["Squad"].unique())

# --- Logo URL placeholder ---
def get_logo(team_name):
    base_url = "https://via.placeholder.com/60x60.png?text="
    return f"{base_url}{team_name.replace(' ', '+')}"

def validate_image_url(url):
    try:
        r = requests.head(url)
        return r.status_code == 200
    except:
        return False

# --- Team selectors ---
col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Select Team 1", serie_a_teams, index=serie_a_teams.index("Milan"))
    logo1 = get_logo(team1)
    if validate_image_url(logo1):
        st.image(logo1, width=60)
with col2:
    team2 = st.selectbox("Select Team 2", serie_a_teams, index=serie_a_teams.index("Napoli"))
    logo2 = get_logo(team2)
    if validate_image_url(logo2):
        st.image(logo2, width=60)

# --- Filter dataframes ---
team1_df = serie_a_df[serie_a_df["Squad"] == team1].copy()
team2_df = serie_a_df[serie_a_df["Squad"] == team2].copy()

# --- Stats to compare ---
stats = ["Goals", "Assists", "Shots", "Tkl", "Int", "PasTotCmp", "PasTotAtt"]

# --- Team Summary ---
st.markdown("### 📊 Team Summary Stats")
c1, c2 = st.columns(2)
with c1:
    st.subheader(f"🔴 {team1}")
    st.dataframe(team1_df[["Player", "Pos"] + stats].sort_values(by="Goals", ascending=False))
    st.metric("Total Goals", int(team1_df["Goals"].sum()))
    st.metric("Total Assists", int(team1_df["Assists"].sum()))
with c2:
    st.subheader(f"🔵 {team2}")
    st.dataframe(team2_df[["Player", "Pos"] + stats].sort_values(by="Goals", ascending=False))
    st.metric("Total Goals", int(team2_df["Goals"].sum()))
    st.metric("Total Assists", int(team2_df["Assists"].sum()))

# --- Radar Chart for Top Scorers ---
st.markdown("### 🕸️ Radar Chart: Top Scorer Comparison")

# Normalize stats
combined_df = pd.concat([team1_df, team2_df])
scaler = MinMaxScaler()
combined_df[stats] = scaler.fit_transform(combined_df[stats])

# Get top scorers
p1 = team1_df.sort_values(by="Goals", ascending=False).iloc[0]["Player"]
p2 = team2_df.sort_values(by="Goals", ascending=False).iloc[0]["Player"]
p1_data = combined_df[combined_df["Player"] == p1][stats].values.flatten().tolist()
p2_data = combined_df[combined_df["Player"] == p2][stats].values.flatten().tolist()

# Radar data setup
angles = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()
angles += angles[:1]
p1_data += p1_data[:1]
p2_data += p2_data[:1]

# Radar chart
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
fig.patch.set_facecolor('none')
ax.set_facecolor('none')

ax.plot(angles, p1_data, label=p1 + f" ({team1})", color='#ff6b6b', linewidth=3)
ax.fill(angles, p1_data, alpha=0.2, color='#ff6b6b')
ax.plot(angles, p2_data, label=p2 + f" ({team2})", color='#4ecdc4', linewidth=3)
ax.fill(angles, p2_data, alpha=0.2, color='#4ecdc4')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(stats, color='white', fontsize=12, fontweight='bold')
ax.set_yticklabels([])
ax.set_title("Top Scorer Stat Radar", color='white', fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), facecolor='none', edgecolor='white', labelcolor='white')
ax.grid(True, color='white', alpha=0.3)
ax.set_ylim(0, 1)

st.pyplot(fig)
