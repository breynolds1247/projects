# Web Scraping & Fantasy Football Stats Visualizations Project

## Introduction

As a scientist and an avid sports fan, I love fantasy sports. Given the huge amounts of data available about each player and team in a given professional sports league, it is an excellent venue use data to discover trends and insights. For a data enthusiast like myself, the possibilities are virtually endless. 

The problem is that while it is easy to find publicly available data, it is often not in a format usable for any sort of analysis or simple visualization. For this reason, I wanted to take the opportunity to try out web scraping techniques to create my own datasets. I set out to write an algorithm that could extract NFL player data from this past season (2021-22) while being simple enough to be easily adapted for future use in data extraction from other sources. To accomplish this, I used Python with the Beautiful Soup package to extract data from the pro-football-reference.com website.

Finally, after the web scraping was successfully performed, I obviously wanted to do something with my shiny new data set. To start, I decided to make some visualizations of the player stats most relevant to fantasy football for each major position group. More sophisticated analysis using machine learning techniques is coming soon in future projects!

The data visualizations that were created are in the form of radar charts (or, as I know them, "spider graphs") showing each player's percentile ranking in the major statistical categories for their position group. Spider graphs are commonly used to visualize the combine performance of NFL draft prospects, so I thought that it would be an interesting exercise to extend their use to fantasy-relevant data. In the "Results & Analysis" section, I present the spider graphs for most of the projected contributors in fantasy drafts for this upcoming NFL season and discuss some observations that can be made.

#### Technical skills used in this project:

Python (Pandas, Matplotlib, Numpy, BeautifulSoup), Web Scraping, Data Cleaning, Plotting/Visualizations

## Code

In this section, I briefly explain how to properly execute each script and provide a short description of their capabilities. There are two scripts used for this project- one that scrapes player data and produces output CSV files, and one that reads these files and produces the data visualizations.

#### Web Scraping Algorithm

First, the data is extraced from [pro-football-reference](https://www.pro-football-reference.com/) using `scrapePlayerStats.py`. This script should work out-of-the-box and is simply executed with the command:

```
python scrapePlayerData.py
```

If successful, the script will produce 5 output CSV files- one for each major position group (quarterbacks, running backs, wide receiviers, tight ends) and one with combined fantasy football data for all players.

Some important features of the code are:

- **Lines 16-20:** The URLs containing the data tables to be scraped are entered here.
- **Lines 186-190:** The output CSV file paths are defined here.

#### Visualizations Script

Next, the extracted data is visualized with `playerVisualizationsFF.py`. This script should work out-of-the-box (when provided with a CSV file) and is simply executed with the command:

```
python playerVisualizationsFF.py
```

The output of this script will be in the form of several png image files containing spider graphs for players at each position, broken into tiers (QB1, QB2, RB1, RB2, RB3, etc.).

Some important features of the code are:

- **Line 14:** The path to the input CSV file is defined here. As the script is currently written, it will accept the fantasy data CSV file as scraped using `scrapePlayerData.py`.
- **Lines 23-35:** The player position tiers are defined here. If left unchanged, the tiers include 14 players each, as ordered by the expert-consensus fantasy draft rankings from [FantasyPros.com](https://www.fantasypros.com/).
- **Lines 84-91:** Data selections are made here. For this analysis, percentile rankings were calculated including only player who appeared in 7 or more games and registered at least 5 PPR fantasy points per game. These selections serve to remove fantasy-irrelevant players who would artificially drive up the percentile rankings of the players being analyzed.
- **Lines 250, 258:** The output file paths are defined here.

## Results & Analysis

The players analyzed are divided by position and separated into tiers based on fantasy expert-consensus ranking for the upcoming season. As I play in a 14-team fantasy football league, I naturally divided the players up such that the top 1-14 players at each postion are in tier 1, 15-28 are in tier 2, and so on. The percentile rankings of each stat are still calculated using all players in the sample who meet the data selection requirements of having appeared in at least 7 games and accounted for at least 5 PPR points per game.

Note that some players who are projected to be top fantasy contributors in this upcoming season did not meet the data selection criteria from this past season, and in this case their spider graphs are left blank.

Without further ado, let's see how the top NFL players stacked up against each other (with some extra attention paid to fantasy football implications)!

#### Quaterbacks

#### QB1
![QB1s](visualizations/spiderGraphs_qb1.png)

#### QB2
![QB2s](visualizations/spiderGraphs_qb2.png)

#### Observations:
- The top QB1s are elite in most passing categories across the board, with the exception of Lamar JAckson and Jalen Hurts, who's value clearly comes from outlier rushing ability at the position.
- Joe Burrow has some outlier numbers (a very spikey spider graph), even with a middling pass attempts per game ranking. If the attempts go up, he could really jump into the top-level of fantasy QBs.
- In terms of value picks (QB2s who could jump into the next tier), Kirk Cousins looks much more similar to Dak Prescott than I would have expected, and Derek Carr also put up some good passing numbers.
- A note on rookie QBs (Justin Fields, Trevor Lawrence, Zach Wilson, Mac Jones): They all struggled mightily in their first year. This would sway me away from drafting a rookie QB to my fantasy team with any confidence of him being a reliable contributor.

#### Running Backs

#### RB1
![RB1s](visualizations/spiderGraphs_rb1.png)

#### RB2
![RB2s](visualizations/spiderGraphs_rb2.png)

#### RB3
![RB3s](visualizations/spiderGraphs_rb3.png)

#### Observations:
- Two RBs really set themselves apart- Jonathan Taylor and Austin Ekeler. They are elite in rushing and receiving categories, respectively, while still being great contributors in the opposite facets. They look like the clear top 2 to me.
- Leonard Fournette was unexpectedly great last season and seems to still be under-rated moving forward.
- There is a lot of value to be had in PPR leagues where some great receiving backs are ranked lower than they probably should be- Chase Edmonds, Cordarrelle Patterson, JD McKissic, etc.
- RBs who's value is inflated by high touchdown numbers worry me, so James Connor looks like someone to avoid.
- RBs with high yards per attempt might have a lot of room to grow if given more opportunity. Players like Miles Sanders, Chase Edmunds, Kareem Hunt, Rashaad Penny, and Tony Pollard could be great bargains in this respect.

#### Wide Receivers

#### WR1
![WR1s](visualizations/spiderGraphs_wr1.png)

#### WR2
![WR2s](visualizations/spiderGraphs_wr2.png)

#### WR3
![WR3s](visualizations/spiderGraphs_wr3.png)

#### Observations
- The very top receivers are obvious with elite contributions across the board, but there is a lot more depth of top-quality contributors at this position than the others.
- Mike Evans profiles closer to a WR1 than his projection as a WR3.
- Hunter Renfroe performed shockingly similar to Keenan Allen, and could be a great value if he continues his production.
- DK Metcalf, DeAndre Hopkins, and Adam Thielen all have their value rooted in a high touchdown percentage. They are all obviously good choices, but there is some risk there if their touchdown numbers fall.

#### Tight Ends

#### TE1
![TE1s](visualizations/spiderGraphs_te1.png)

#### TE2
![TE2s](visualizations/spiderGraphs_te2.png)

#### Observations
- Travis Kelce, Mark Andrews, George Kittle, and Rob Gronkowski are the clear top players at the position based on last year's performance.
- Outside of the very top options, there is a lot of parity in the mid-tier-1 tight ends. I wouldn't reach for anyone if I missed out on one of the top options.
- There is very little depth at this position- I wouldn't even consider drafting more than one tight end unless there were some exotic league rules that made it beneficial to roster more than one.

## Acknowlegements

All data comes from [pro-football-reference](https://www.pro-football-reference.com/) who curate an excellent resource for publicly available sports data.

Fantsy draft rankings come from [FantasyPros](https://www.fantasypros.com/), a great resource for fantasy sports information.