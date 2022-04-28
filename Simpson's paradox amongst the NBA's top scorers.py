#!/usr/bin/env python
# coding: utf-8

# # Simpson's Paradox

# ## Summary 

# Simpson's paradox arises in a variety of settings where statistics are present. Here, I dive into a look into instances of it in NBA shooting data. I expect it to be heavily present because of the differences in playing styles and difficulties of certain shots. Specifically, three pointers are harder to make than two pointers, and the best shooters shoot them more than worse shooters, so we should see a bunch of examples of pairs of players, say player A & player B, where player A is a shooter and shoots lots of 2s and shoots both 2s and 3s at a higher percentage than player B, but since a bigger proportion of player B's shots are 3s, player A has a higher overall FG%.
# 
# Since I think there will be many cases of this, I'll only look at instances within the top scorers in the league, considering only the pairs of players within the top 25 scores.

# Special shoutout to [Sports Reference](https://www.sports-reference.com/) (SR), specifically [Basketball Reference](https://www.basketball-reference.com/) (BR), for all of the data on the players' minutes played, positions, and birth places. This was partially inspired by a [reddit post](https://www.reddit.com/r/nba/comments/5wb6j7/oc_simpsons_paradox_lebrons_overall_3p_is_greater/) and also by the Derek Jeter-David Justice example of [Simpson's paradox on Wikipedia](https://en.wikipedia.org/wiki/Simpson%27s_paradox)

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as BS
import plotly.graph_objects as go
import plotly.express as px
import mplcursors


# In[2]:


year = 2022              # which year you'd like to take a look at (keep in mind 3pt-line introduced in '79')

url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_totals.html#totals_stats::pts"
tables = pd.read_html(url) 
table = pd.DataFrame(tables[0])                                     # This gives the desired table
clean_Table = table[["Player","G", "FG%", "2P%", "3P%", "3P", "3PA", "2P", "2PA", "PTS"]]   # Select the relevant cols
clean_Table = clean_Table[clean_Table.Player != 'Player']               # Eliminate bad rows
clean_Table.fillna("0", inplace = True)                                 # In case some players didn't attempt 3s or 2s

# This for loop converts the strings to floats so that we can compare them later
for cat in ["G", "FG%", "2P%", "3P%", "3P", "3PA", "2P", "2PA", "PTS"]:
    clean_Table[cat] = [np.float(clean_Table.iloc[i][cat]) if clean_Table.iloc[i][cat][0] != "0" else 0.0 for i in range(len(clean_Table[cat]))]

clean_Table["PPG"] = clean_Table["PTS"]/clean_Table["G"]      # adda column with points per game
players = clean_Table.to_numpy()                              # convert the pd DataFrame to a numpy array

players = players[players[:, -1].argsort()][::-1]             # sort by leading scorers
plyrs = players[players[:, 1] >= 58][:25]                     # only take the top 25 of those who played >= 58 games


# In[3]:


def compute_simpsons(players):
    """
    This function takes in a numpy array of the players with their stats and 
    returns a dataframe of the pairs players whose FG%, 2P%, and 3P% satisfy Simpson's paradox
    """
    d = {"namesA":[], "percA" : [], "2percA" : [], "3percA" : [], "2attA": [] , "3attA" : [],"namesB":[], "percB" : [], "2percB" : [], "3percB" : [], "2attB": [] , "3attB" : []}
    for i in range(25):
        player1 = players[i]
        for j in range(i+1, 25):
            player2 = players[j]
            if player1[2] > player2[2] and player1[3] < player2[3] and player1[4] < player2[4]:
                playerA = player1
                playerB = player2
                d["namesA"].append(playerA[0])
                d["percA"].append(playerA[2])
                d["2percA"].append(playerA[3])
                d["3percA"].append(playerA[4])
                d["3attA"].append(playerA[6])
                d["2attA"].append(playerA[8])
                d["namesB"].append(playerB[0])
                d["percB"].append(playerB[2])
                d["2percB"].append(playerB[3])
                d["3percB"].append(playerB[4])
                d["3attB"].append(playerB[6])
                d["2attB"].append(playerB[8])

            elif player1[2] < player2[2] and player1[3] > player2[3] and player1[4] > player2[4]:
                playerA = player2
                playerB = player1
                d["namesA"].append(playerA[0])
                d["percA"].append(playerA[2])
                d["2percA"].append(playerA[3])
                d["3percA"].append(playerA[4])
                d["3attA"].append(playerA[6])
                d["2attA"].append(playerA[8])
                d["namesB"].append(playerB[0])
                d["percB"].append(playerB[2])
                d["2percB"].append(playerB[3])
                d["3percB"].append(playerB[4])
                d["3attB"].append(playerB[6])
                d["2attB"].append(playerB[8])

    return pd.DataFrame(d)


# This table shows all of the pairs of players in the top 25 scorers (min 58 games) whose shooting percentages demonstrate Simpson's paradox. For each row, the player in the first column has a higher shooting percentage than the player in the second column, but the player in the second column has a higher 2-point percentage and a higher 3-point percentage than the player in the first column. Despite shooting better in both categories, the player in the second column has a worse overall shooting percentage because of the number of shots taken at the different distances. 
# 
# Players tend to make 2-pointers at higher percentage rates than 3-pointers, so if a player shoots more 2s, their shooting percentage will likely be higher. Conversely, if a player shoots a lot of 3s, their shooting percentage will likely be lower. This is why many of the players in the first column are known to be high volume 2-point shooters and many in the right column are high volume 3-point shooters. 

# In[4]:


examples = compute_simpsons(plyrs)


# In[5]:


plyrsDF = pd.DataFrame(plyrs)
plyrsDF.head()
plyrsDF.set_axis(["Name", "G", "FG%", "2P%", "3P%", "3P", "3PA", "2P", "2PA", "PTS", "PPG"], axis=1, inplace=True)
plyrsDF["2Prop"] = (50*np.array([plyrsDF["2PA"][i]/(plyrsDF["2PA"][i] + plyrsDF["3PA"][i]) for i in range(len(plyrsDF["2PA"]))]))**2
plyrsDF["FG%"] = plyrsDF["FG%"].astype(np.float)


# In[6]:


X_coords = [[examples["2percA"][i], examples["2percB"][i]] for i in range(len(examples["2percA"]))]
Y_coords = [[examples["3percA"][i], examples["3percB"][i]] for i in range(len(examples["3percA"]))]


# ## Graphic explanation
# In the following graphic, I've plotted 
# 1. 2-pointer field goal percentage (2P%, x-axis),
# 2. 3-pointer field goal percentage (3P%, y-axis),
# 3. Overall field goal percentage (FG%, color of the markers),
# 4. Relative proportion of field goal attempts that are 2-pointers (size of markers)
# for the top 25 scorers, and
# 5. Line segments connecting pairs of players whose 2P%, 3P%, and FG% satisfy Simpson's paradox
# 
# One thing you can notice is that a necessary (but not sufficient) condition for a pair of players Player A (better overall FG%) and Player B (better 2P% and 3P%) to satisfy the "paradox'' is that Player B must be above and to the right of Player A on the graph, but Player A has a larger and darker marker, since Player A shoots more 2s overall. This is under the (not true for all players but true here) assumption that all players shoot 2-pointers at a higher percentage than 3-pointers.
# 
# The property is also transitive, as exhibited with DeMar DeRozan, Joel Embiid, and Zach Lavine, and also by Dejounte Murray, Anthony Edwards, and Steph Curry.
# 
# This analysis isn't meant to judge any players as better than others; it's simply an interesting phenomenon that occurs between the best scorers in the league because of their different ways of scoring. 

# In[38]:


fig = px.scatter(plyrsDF, x="2P%", y="3P%", color = 'FG%', size = "2Prop", 
                 color_continuous_scale=px.colors.sequential.Emrld,
                 title="Simpson's Paradox Amongst Top NBA Scorers, '21-'22", hover_name = "Name")

for i in range(len(X_coords)):
    reference_line = go.Scatter(x=X_coords[i],
                                y=Y_coords[i],
                                mode="lines",
                                line=go.scatter.Line(color="gray"),
                                showlegend=False)
    fig.add_trace(reference_line, row=1, col=1)


fig.show()

