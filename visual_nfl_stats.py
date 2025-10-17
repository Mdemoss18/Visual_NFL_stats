# Import necessary libraries
import streamlit as stlit
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page setup for webpage
stlit.set_page_config(page_title="NFL Player Stats Visualization", layout="wide", pageicon="🏈")
stlit.title("NFL Player Stats Visualization")
stlit.markdown("Visualize and analyze NFL player statistics with interactive charts.")


# Load data
def load_data():
    url = "https://raw.githubusercontent.com/your-repo/nfl-stats/main/nfl_player_stats.csv"
    data = pd.read_csv(url)
    return data

data = load_data()

# Sidebar controls for user to select season, and stat type (passing, rushing, receiving)
stlit.sidebar.header("Filter Options")
season = stlit.sidebar.selectbox("Select Season", sorted(data['Season'].unique()), index=len(data['Season'].unique())-1)
stat_type = stlit.sidebar.selectbox("Select Stat Type", ["Passing", "Rushing", "Receiving"])


# Filter data based on user selection
if stat_type == "Passing":
    filtered_data = data[(data['Season'] == season) & (data['Position'] == 'QB')]
    stat_column = 'PassingYards'

elif stat_type == "Rushing":
    filtered_data = data[(data['Season'] == season) & (data['Position'].isin(['RB', 'FB', 'QB']))]
    stat_column = 'RushingYards'

else:  # Receiving
    filtered_data = data[(data['Season'] == season) & (data['Position'].isin(['WR', 'TE', 'RB']))]
    stat_column = 'ReceivingYards'


# Process data to get top 10 players based on selected stat
top_players = filtered_data.nlargest(10, stat_column)

# Visualize the data
stlit.subheader(f"Top 10 Players in {stat_column} for {season} Season")
plt.figure(figsize=(10, 6))
sns.barplot(x=stat_column, y='Player', data=top_players, palette='Blues_d')
plt.xlabel(stat_column)
plt.ylabel('Player')
plt.title(f"Top 10 {stat_type} Players in {season}")
stlit.pyplot(plt)