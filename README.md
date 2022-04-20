# Simpsons-paradox-in-the-NBA
## Summary 

[Simpson's paradox on Wikipedia](https://en.wikipedia.org/wiki/Simpson%27s_paradox) arises in a variety of settings where statistics are present. Here, I dive into a look into instances of it in NBA shooting data. I expect it to be heavily present because of the differences in playing styles and difficulties of certain shots. Specifically, three pointers are harder to make than two pointers, and the best shooters shoot them more than worse shooters, so we should see a bunch of examples of pairs of players, say player A & player B, where player A is a shooter and shoots lots of 2s and shoots both 2s and 3s at a higher percentage than player B, but since a bigger proportion of player B's shots are 3s, player A has a higher overall FG%.

Since I think there will be many cases of this, I'll only look at instances within the top scorers in the league, considering only the pairs of players within the top 25 scores.

Special shoutout to [Sports Reference](https://www.sports-reference.com/) (SR), specifically [Basketball Reference](https://www.basketball-reference.com/) (BR), for all of the data on the players' shooting percentages. This was partially inspired by a [reddit post](https://www.reddit.com/r/nba/comments/5wb6j7/oc_simpsons_paradox_lebrons_overall_3p_is_greater/) and also by the Derek Jeter-David Justice example of Simpson's paradox on Wikipedia

## Examples
There have been examples of Simpson's paradox in each year since the 3-point line was introduced. If we look at the most recent NBA regular season, we can see _ pairs of players within the top 25 scorers who exhibit the phenomenon. The table below shows these players. The code can be easily modified for any season between 1980-present.

For a snippet of the examples, check out the tables below. For each row in the first table, the player in the first column has a higher shooting percentage than the player in the second column, but the player in the second column has a higher 2-pointer percentage and 3-pointer percentage. This is further broken down for some of the examples in the second table. 

![alt text](https://github.com/gsarajian/Simpsons-paradox-in-the-NBA/blob/main/fig1.png?raw=false)
![alt text](https://github.com/gsarajian/Simpsons-paradox-in-the-NBA/blob/main/fig2.png?raw=false)
