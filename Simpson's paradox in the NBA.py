#!/usr/bin/env python
# coding: utf-8

# # Simpson's Paradox

# ## Summary 

# Simpson's paradox arises in a variety of settings where statistics are present. Here, I dive into a look into instances of it in NBA shooting data. I expect it to be heavily present because of the differences in playing styles and difficulties of certain shots. Specifically, three pointers are harder to make than two pointers, and the best shooters shoot them more than worse shooters, so we should see a bunch of examples of pairs of players, say player A & player B, where player A is a shooter and shoots lots of 2s and shoots both 2s and 3s at a higher percentage than player B, but since a bigger proportion of player B's shots are 3s, player A has a higher overall FG%.
# 
# Since I think there will be many cases of this, I'll only look at instances within the top scorers in the league, considering only the pairs of players within the top 25 scores.

# Special shoutout to [Sports Reference](https://www.sports-reference.com/) (SR), specifically [Basketball Reference](https://www.basketball-reference.com/) (BR), for all of the data on the players' minutes played, positions, and birth places. This was partially inspired by a [reddit post](https://www.reddit.com/r/nba/comments/5wb6j7/oc_simpsons_paradox_lebrons_overall_3p_is_greater/) and also by the Derek Jeter-David Justice example of [Simpson's paradox on Wikipedia](https://en.wikipedia.org/wiki/Simpson%27s_paradox)

# In[7]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as BS
import plotly.graph_objects as go
import plotly.figure_factory as ff


# In[2]:


year = 2022              # which year you'd like to take a look at (keep in mind 3pt-line introduced in '79')

url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
tables = pd.read_html(url) 
table = pd.DataFrame(tables[0])                                         # This gives the desired table
clean_Table = table[["Player","G", "FG%", "2P%", "3P%", "PTS"]]         # Select the relevant columns
clean_Table = clean_Table[clean_Table.Player != 'Player']               # Eliminate bad rows
clean_Table.fillna("0", inplace = True)                                 # In case some players didn't attempt 3s or 2s


# This for loop converts the strings to floats so that we can compare them later
for cat in ["G", "FG%", "2P%", "3P%", "PTS"]:
    clean_Table[cat] = [float(clean_Table.iloc[i][cat]) if clean_Table.iloc[i][cat][0] != "0" else 0.0 for i in range(len(clean_Table[cat]))]

players = clean_Table.to_numpy()                              # convert the pd DataFrame to a numpy array

players = players[players[:, -1].argsort()][::-1]             # sort by leading scorers
plyrs = players[players[:, 1] >= 41][:25]                     # only take the top 25 of those who played >= 41 games


# In[4]:


def compute_simpsons(players):
    
    examples_of_simpsons = []

    for i in range(25):
        playerA = players[i]
        for j in range(i+1, 25):
            playerB = players[j]
            if playerA[2] > playerB[2] and playerA[3] < playerB[3] and playerA[4] < playerB[4]:
                examples_of_simpsons.append([playerA, playerB])
            elif playerA[2] < playerB[2] and playerA[3] > playerB[3] and playerA[4] > playerB[4]:
                examples_of_simpsons.append([playerB, playerA])

    return examples_of_simpsons


# This table shows all of the pairs of players in the top 25 scorers (min 41 games) whose shooting percentages demonstrate Simpson's paradox. For each row, the player in the first column has a higher shooting percentage than the player in the second column, but the player in the second column has a higher 2-point percentage and a higher 3-point percentage than the player in the first column. Despite shooting better in both categories, the player in the second column has a worse overall shooting percentage because of the number of shots taken at the different distances. 
# 
# Players tend to make 2-pointers at higher percentage rates than 3-pointers, so if a player shoots more 2s, their shooting percentage will likely be higher. Conversely, if a player shoots a lot of 3s, their shooting percentage will likely be lower. This is why many of the players in the first column are known to be high volume 2-point shooters and many in the right column are high volume 3-point shooters. 
# 
# An asterisk (*) by a players name indicates Hall-of-Famer

# In[5]:


examples = compute_simpsons(plyrs)


# In[6]:


aplayers = [a[0][0] for a in examples]
bplayers = [a[1][0] for a in examples]

fig = go.Figure(data=[go.Table(header=dict(values=['Higher Overall Shooting Percentage', 'Lower Overall Shooting Percentage']),
                 cells=dict(values=[aplayers, bplayers]))
                     ])
fig.show()


# This cell is just to reformat the examples so that we can look at a table that compares the shooting percentages in the pairs.

# In[9]:


adf = [a[0] for a in examples]
bdf = [a[1] for a in examples]
combdf = [0]*(2*len(examples))
for i in range(2*len(examples)):
    if i % 2 == 0:
        combdf[i] = adf[i//2]
    else:
        combdf[i] = bdf[i//2]

dfa = pd.DataFrame(adf[:len(examples)])
dfb = pd.DataFrame(bdf[:len(examples)])
df = pd.DataFrame(combdf[:len(examples)])
df = df[[0, 2, 3, 4]]
df.rename(columns={0: "Player", 2: "FG%", 3:"2FG%", 4:"3FG%"}, inplace = True)


# In[12]:


color1 = 'white'
color2 = 'lightgrey'
  
fig = go.Figure(data=[go.Table(
    # Ratio for column width
    columnwidth=[0.5, 0.1, 0.1, 0.1],
    header=dict(values=['Players', 'FG%', "2FG%", '3FG%']),
    cells=dict(values=[df['Player'],
                       df['FG%'], df['2FG%'], df['3FG%']],
               fill_color=[[color1, color1, color2,
                            color2]*(len(examples)//2)],))
])
fig.show()

