# Import necessary libraries
import streamlit as stlit
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup for webpage
stlit.set_page_config(page_title="NFL Player Stats Visualization", layout="wide", page_icon="🏈")
stlit.title("NFL Player Stats Visualization")
stlit.markdown("Visualize and analyze NFL player statistics from the 2023 season!")


# Load data
def load_data():
    url = "play_by_play_2023.parquet"
    data = pd.read_parquet(url)
    return data

data = load_data()

# Sidebar controls are for the user to select stat type (passing, rushing, receiving)
stlit.sidebar.header("Filter Options")
stat_type = stlit.sidebar.selectbox("Select Stat Type", ["Passing Yards", "Rushing Yards", "Receiving Yards"])

teams = sorted(data['posteam'].dropna().unique())
team = stlit.sidebar.selectbox("Select Team (Optional)", ["All Teams"] + teams)

# Filter data based on user selection
filtered_data = data.copy()

if team != "All Teams":
    filtered_data = filtered_data[filtered_data['posteam'] == team]

# Choose player column and filter based on stat type
if stat_type == "Passing Yards":
    filtered_data = filtered_data[filtered_data['pass'] == 1]
    stat_col = "yards_gained"
    player_col = "passer_player_name"
elif stat_type == "Rushing Yards":
    filtered_data = filtered_data[filtered_data['rush'] == 1]
    stat_col = "yards_gained"
    player_col = "rusher_player_name"
else:  # Receiving Yards
    filtered_data = filtered_data[filtered_data['pass'] == 1]  # receptions counted from pass plays
    stat_col = "yards_gained"
    player_col = "receiver_player_name"


# Process data to get top 10 players based on selected stat
top_players = filtered_data.groupby(player_col)[stat_col].sum().sort_values(ascending=False).head(10)

# Visualize the data
stlit.subheader(f"Top 10 Players by {stat_type}")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_players.values, y=top_players.index, ax=ax, palette="Blues_d")
ax.set_xlabel(stat_type)
ax.set_ylabel("Player")
ax.set_title(f"Top 10 Players by {stat_type} (2023)")
stlit.pyplot(fig)
