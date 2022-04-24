#This script will read created dataframes to produce spider graphs of fantasy football-relevant NFL stats for 3 important position groups using data from the 2021-22 NFL season

#Import data manipulation packages
import pandas as pd
import numpy as np

#Import data visualization packages
import matplotlib as mpl
from matplotlib import pyplot as plt

def main():

    #Open dataframes of scraped data
    fantData = pd.read_csv("scrapedData/NFLFantasyData2021.csv")

    #Create dataframe for each position group
    qbData = fantData[fantData['FantPos'] == "QB"]
    rbData = fantData[fantData['FantPos'] == "RB"]
    wrData = fantData[fantData['FantPos'] == "WR"]
    teData = fantData[fantData['FantPos'] == "TE"]

    #Create player fantasy position tiers
    qb1s = ['Josh Allen', 'Patrick Mahomes', 'Justin Herbert', 'Kyler Murray', 'Lamar Jackson', 'Joe Burrow', 'Dak Prescott', 'Matthew Stafford', 'Russell Wilson', 'Deshaun Watson', 'Jalen Hurts', 'Tom Brady', 'Aaron Rodgers', 'Trey Lance']
    qb2s = ['Justin Fields', 'Derek Carr', 'Kirk Cousins', 'Tua Tagovailoa', 'Ryan Tannehill', 'Trevor Lawrence', 'Mac Jones', 'Matt Ryan', 'Zach Wilson', 'Jameis Winston', 'Carson Wentz', 'Daniel Jones', 'Jared Goff', 'Mitchell Trubisky']

    rb1s = ['Jonathan Taylor', 'Austin Ekeler', 'Derrick Henry', 'Christian McCaffrey', 'Dalvin Cook', 'Najee Harris', 'Javonte Williams', 'Joe Mixon', 'Cam Akers', "D'Andre Swift", 'Alvin Kamara', 'Nick Chubb', 'Leonard Fournette', 'Antonio Gibson']
    rb2s = ['Aaron Jones', 'Saquon Barkley', 'David Montgomery', 'James Conner', 'Josh Jacobs', 'Ezekiel Elliott', 'Elijah Mitchell', 'J.K. Dobbins', 'Michael Carter', 'AJ Dillon', 'Miles Sanders', 'Damien Harris', 'Clyde Edwards-Helaire', 'Travis Etienne']
    rb3s = ['Chase Edmonds', 'Devin Singletary', 'Kareem Hunt', 'Tony Pollard', 'Cordarrelle Patterson', 'Rashaad Penny', 'Melvin Gordon', 'James Robinson', 'Alexander Mattison', 'Rhamondre Stevenson', 'Darrell Henderson', 'Ronald Jones II', 'Chris Carson', 'J.D. McKissic']

    wr1s = ['Cooper Kupp', 'Justin Jefferson', "Ja'Marr Chase", 'Davante Adams', 'Stefon Diggs', 'Deebo Samuel', 'A.J. Brown', 'Tyreek Hill', 'CeeDee Lamb', 'Keenan Allen', 'Jaylen Waddle', 'Mike Evans', 'Diontae Johnson', 'Tee Higgins']
    wr2s = ['DeAndre Hopkins', 'D.K. Metcalf', 'D.J. Moore', 'Chris Godwin', 'Michael Pittman Jr.', 'Terry McLaurin', 'Brandin Cooks', 'Jerry Jeudy', 'Amari Cooper', 'Elijah Moore', 'Allen Robinson', 'Courtland Sutton', 'Hunter Renfrow', 'Amon-Ra St. Brown']
    wr3s = ['DeVonta Smith', 'Tyler Lockett', 'Darnell Mooney', 'Marquise Brown', 'JuJu Smith-Schuster', 'Adam Thielen', 'Mike Williams', 'Brandon Aiyuk', 'Michael Thomas', 'Rashod Bateman', 'Kadarius Toney', 'Chase Claypool', 'Robert Woods', 'Gabriel Davis']

    te1s = ['Travis Kelce', 'Mark Andrews', 'Kyle Pitts', 'George Kittle', 'Darren Waller', 'T.J. Hockenson', 'Dallas Goedert', 'Dalton Schultz', 'Dawson Knox', 'Pat Freiermuth', 'Mike Gesicki', 'Rob Gronkowski', 'Zach Ertz', 'Cole Kmet']
    te2s = ['Noah Fant', 'Hunter Henry', 'Logan Thomas', 'Albert Okwuegbunam', 'Evan Engram', 'Tyler Higbee', 'Gerald Everett', 'Robert Tonyan', 'David Njoku', 'Austin Hooper', 'Jonnu Smith', 'Adam Trautman', 'Dan Arnold', 'Jared Cook']

    #Sort data by PPR points (the right league setting) because the scraped data is ranked by standard scoring (the wrong league setting)
    #Assume QBs are not affected by PPR scoring
    rbData = rbData.sort_values(by = 'PPR', ascending = False)
    wrData = wrData.sort_values(by = 'PPR', ascending = False)
    teData = teData.sort_values(by = 'PPR', ascending = False)

    #List categories to place on spider graphs
    qbCats = ['Cmp%', 'PassAtt', 'PassYds', 'PassTD', 'Int', 'PassYds/Att', 'RushYds', 'RushTD']
    rbCats = ['RushAtt', 'RushYds', 'Y/A', 'RushTD', 'Tgt', 'Rec', 'RecYds', 'RecTD']
    wrCats = ['Tgt', 'Rec', 'RecYds', 'RecTD', 'Y/R']
    teCats = ['Tgt', 'Rec', 'RecYds', 'RecTD', 'Y/R']

    #Some of the desired stats must be calculated from those already in the tables
    qbData['Cmp%'] = (qbData['Cmp']/qbData['PassAtt'])*100.0
    qbData['PassYds/Att'] = qbData['PassYds']/qbData['PassAtt']
    qbData['PPR'] = qbData['PPR']/qbData['G']
    rbData['PPR'] = rbData['PPR']/rbData['G']
    wrData['PPR'] = wrData['PPR']/wrData['G']
    teData['PPR'] = teData['PPR']/teData['G']

    #Convert cumulative stats to per game stats 
    ##(avoid skewing percentiles to favor players who did not miss games)
    for cat in qbCats:
        if cat != 'Cmp%' and cat != 'PassYds/Att':
            qbData[cat] = qbData[cat]/qbData['G']
    
    for cat in rbCats:
        if cat != 'Y/A':
           rbData[cat] = rbData[cat]/rbData['G']

    for cat in wrCats:
        if cat != 'Y/R':
            wrData[cat] = wrData[cat]/wrData['G']

    for cat in teCats:
        if cat != 'Y/R':
            teData[cat] = teData[cat]/teData['G']        

    #Trim dataframes to include only categories necessary for spider graphs and data selections
    qbDataTrimmed = qbData[['Player', 'Tm', 'G', 'PPR'] + qbCats]
    rbDataTrimmed = rbData[['Player', 'Tm', 'G', 'PPR'] + rbCats]
    wrDataTrimmed = wrData[['Player', 'Tm', 'G', 'PPR'] + wrCats]
    teDataTrimmed = teData[['Player', 'Tm', 'G', 'PPR'] + teCats]

    #Data selections
    #Remove very small samples- players who did not play in at least 7 games (roughly half of a fantasy football season)
    #Remove fantasy irrelevant playerys- players who did not register at least 5 PPR fantasy points per game
    qbDataTrimmed = qbDataTrimmed[qbDataTrimmed['G'] >= 7] 
    qbDataTrimmed = qbDataTrimmed[qbDataTrimmed['PPR'] > 5]
    rbDataTrimmed = rbDataTrimmed[rbDataTrimmed['G'] >= 7]
    rbDataTrimmed = rbDataTrimmed[rbDataTrimmed['PPR'] > 5]
    wrDataTrimmed = wrDataTrimmed[wrDataTrimmed['G'] >= 7]
    wrDataTrimmed = wrDataTrimmed[wrDataTrimmed['PPR'] > 5]
    teDataTrimmed = teDataTrimmed[teDataTrimmed['G'] >= 7]
    teDataTrimmed = teDataTrimmed[teDataTrimmed['PPR'] > 5]
    #For reference, we are now left with:
    #38 QBs
    #68 RBs
    #100 WRs
    #32 TEs

    #Calculate percentile rank for each important stat in each position group
    for cat in qbCats:
        qbDataTrimmed[cat + '_Rank'] = qbDataTrimmed[cat].rank(pct=True)
    for cat in rbCats:
        rbDataTrimmed[cat + '_Rank'] = rbDataTrimmed[cat].rank(pct=True)
    for cat in wrCats:
        wrDataTrimmed[cat + '_Rank'] = wrDataTrimmed[cat].rank(pct=True)
    for cat in teCats:
        teDataTrimmed[cat + '_Rank'] = teDataTrimmed[cat].rank(pct=True)

    #Flip interections percentile for QBs so that higher rank means fewer ints
    qbDataTrimmed['Int_Rank'] = 1 - qbDataTrimmed['Int_Rank']

    #quality control print statements
    #print(fantData.head())
    #print(qbData.head())
    #print(qbData.dtypes)
    #print(rbData.head())
    #print(wrData.head())
    #print(teData.head())
    print(qbDataTrimmed.head(14))
    print(qbDataTrimmed.shape)
    print(rbDataTrimmed.shape)
    print(wrDataTrimmed.shape)
    print(teDataTrimmed.shape)

    #Plot parameters
    #mpl.rcParams['font.family'] = 'Avenir'
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['axes.linewidth'] = 0
    mpl.rcParams['xtick.major.pad'] = 15

    #Calculate angles for polar graphs
    qbAngles = np.linspace(0, 2*np.pi, len(qbCats) + 1)
    rbAngles = np.linspace(0, 2*np.pi, len(rbCats) + 1)
    wrAngles = np.linspace(0, 2*np.pi, len(wrCats) + 1)
    teAngles = np.linspace(0, 2*np.pi, len(teCats) + 1)

    #Make the plots!

    #Define figure for each position grouping and rank
    qb1Fig = plt.figure()
    qb2Fig = plt.figure()
    rb1Fig = plt.figure()
    rb2Fig = plt.figure()
    rb3Fig = plt.figure()
    wr1Fig = plt.figure()
    wr2Fig = plt.figure()
    wr3Fig = plt.figure()
    te1Fig = plt.figure()
    te2Fig = plt.figure()
    fig = plt.figure(figsize=(16,9))

    #Set up axes for each spider graph on the figure
    ax1 = fig.add_subplot(3, 5, 1, projection='polar', facecolor='#ededed')
    ax2 = fig.add_subplot(3, 5, 2, projection='polar', facecolor='#ededed')
    ax3 = fig.add_subplot(3, 5, 3, projection='polar', facecolor='#ededed')
    ax4 = fig.add_subplot(3, 5, 4, projection='polar', facecolor='#ededed')
    ax5 = fig.add_subplot(3, 5, 5, projection='polar', facecolor='#ededed')
    ax6 = fig.add_subplot(3, 5, 6, projection='polar', facecolor='#ededed')
    ax7 = fig.add_subplot(3, 5, 7, projection='polar', facecolor='#ededed')
    ax8 = fig.add_subplot(3, 5, 8, projection='polar', facecolor='#ededed')
    ax9 = fig.add_subplot(3, 5, 9, projection='polar', facecolor='#ededed')
    ax10 = fig.add_subplot(3, 5, 10, projection='polar', facecolor='#ededed')
    ax11 = fig.add_subplot(3, 5, 11, projection='polar', facecolor='#ededed')
    ax12 = fig.add_subplot(3, 5, 12, projection='polar', facecolor='#ededed')
    ax13 = fig.add_subplot(3, 5, 13, projection='polar', facecolor='#ededed')
    ax14 = fig.add_subplot(3, 5, 14, projection='polar', facecolor='#ededed')

    plt.subplots_adjust(hspace=0.9, wspace=0.5)

    #Make list of axes
    axes = []
    axes.extend((ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14))

    plotsByFantasyRanking(qb1s, qbDataTrimmed, axes, qbAngles, qbCats, "qb1")
    clearAxes(axes)
    plotsByFantasyRanking(qb2s, qbDataTrimmed, axes, qbAngles, qbCats, "qb2")
    clearAxes(axes)
    plotsByFantasyRanking(rb1s, rbDataTrimmed, axes, rbAngles, rbCats, "rb1")
    clearAxes(axes)
    plotsByFantasyRanking(rb2s, rbDataTrimmed, axes, rbAngles, rbCats, "rb2")
    clearAxes(axes)
    plotsByFantasyRanking(rb3s, rbDataTrimmed, axes, rbAngles, rbCats, "rb3")
    clearAxes(axes)
    plotsByFantasyRanking(wr1s, wrDataTrimmed, axes, wrAngles, wrCats, "wr1")
    clearAxes(axes)
    plotsByFantasyRanking(wr2s, wrDataTrimmed, axes, wrAngles, wrCats, "wr2")
    clearAxes(axes)
    plotsByFantasyRanking(wr3s, wrDataTrimmed, axes, wrAngles, wrCats, "wr3")
    clearAxes(axes)
    plotsByFantasyRanking(te1s, teDataTrimmed, axes, teAngles, teCats, "te1")
    clearAxes(axes)
    plotsByFantasyRanking(te2s, teDataTrimmed, axes, teAngles, teCats, "te2")
    
    #print(rbDataTrimmed.dtypes)

    #print(rbDataTrimmed.head(42))

    #print(rbDataTrimmed['Player'=='Ronald Jones II '])
    """
    #Loop over player groups and plot stats
    for i,player in enumerate(qb1s):
        
        if len(qb1s) != len(axes):
            print("Must define set of axes for each player. Exiting...")
            break
        
        playerData = getPlayerData(qbDataTrimmed, player)
        
        #Check that a filled array is passed
        if not playerData.size:
            axes[i].set_xticklabels([])
            axes[i].set_yticklabels([])
            axes[i].text(np.pi/2, 1.7, player, ha='center', va='center', size=14, color='black')
            if i == len(qb1s)-1:
                plt.savefig()
            continue

        print(playerData)
        color = team_colors[playerData[1]]
        axes[i] = createSpiderGraph(axes[i], qbAngles, playerData, qbCats, color)

        if i == len(qb1s)-1:
            plt.savefig('spiderGraphs_qb1s.png', bbox_inches='tight')
    """

def createSpiderGraph(ax, angles, player_data, categories, color='blue'):
    #Function to create and fill spider graphs 

    #Plot data and fill with team color
    ax.plot(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, linewidth=2)
    ax.fill(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, alpha=0.2)
    
    #Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.tick_params(axis='x', which='major', pad=10)
    
    #Remove radial labels
    ax.set_yticklabels([])

    #Add player name and team
    ax.text(np.pi/2, 1.7, player_data[0]+", "+player_data[1], ha='center', va='center', size=14, color=color)
    
    #Use white grid
    ax.grid(color='white', linewidth=1.5)

    #Set axis limits
    ax.set(xlim=(0, 2*np.pi), ylim=(0, 1))

    return ax

def getPlayerData(data, player):
    #Function to select individual player data as an array from dataframes
    
    try:
        playerStats = np.array(data[data['Player'] == player])[0]
        
    except IndexError:
        print(player + "'s 2021 stats do not meet data selection requirements. Player will be skipped.")
        playerStats = np.array([])
        
    return playerStats 

def plotsByFantasyRanking(positionRankList, positionData, axes, positionAngles, positionCats, groupName):
    
    #Use color dict from https://teamcolorcodes.com/nfl-team-color-codes/#What_Are_the_HEX_Color_Codes_Used_by_NFL_Teams
    team_colors = {'ARI':'#97233f', 'ATL':'#a71930', 'BAL':'#241773', 'BUF':'#00338d', 'CAR':'#0085ca', 'CHI':'#0b162a', 'CIN':'#fb4f14', 'CLE':'#311d00', 'DAL':'#041e42', 'DEN':'#002244', 'DET':'#0076b6', 'GNB':'#203731', 'HOU':'#03202f', 'IND':'#002c5f', 'JAX':'#006778', 'KAN':'#e31837', 'LAC':'#002a5e', 'LAR':'#003594', 'MIA':'#008e97', 'MIN':'#4f2683', 'NWE':'#002244', 'NOR':'#d3bc8d', 'NYG':'#0b2265', 'NYJ':'#125740', 'LVR':'#000000', 'PHI':'#004c54', 'PIT':'#ffb612', 'SFO':'#aa0000', 'SEA':'#002244', 'TAM':'#d50a0a', 'TEN':'#0c2340', 'WAS':'#773141', '2TM':'black'}
    
    #Loop over player groups and plot stats
    for i,player in enumerate(positionRankList):
        
        if len(positionRankList) != len(axes):
            print("Must define set of axes for each player. Exiting...")
            break
        
        playerData = getPlayerData(positionData, player)
        
        #Check that a filled array is passed
        if not playerData.size:
            axes[i].set_xticklabels([])
            axes[i].set_yticklabels([])
            axes[i].text(np.pi/2, 1.7, player, ha='center', va='center', size=14, color='black')
            if i == len(positionRankList)-1:
                #plt.show()
                plt.savefig('spiderGraphs_'+groupName+'.png', bbox_inches='tight')
                #plt.figure().clear()
                #plt.close()
                #plt.cla()
                #plt.clf()
            continue

        #print(playerData)
        color = team_colors[playerData[1]]
        axes[i] = createSpiderGraph(axes[i], positionAngles, playerData, positionCats, color)

        if i == len(positionRankList)-1:
            plt.savefig('spiderGraphs_'+groupName+'.png', bbox_inches='tight')
            #plt.figure().clear()
            #plt.close()
            #plt.cla()
            #plt.clf()

def clearAxes(axes):
    for ax in axes:
        ax.clear()


main()