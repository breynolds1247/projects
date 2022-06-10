#Import scaping packages
import urllib3
from bs4 import BeautifulSoup

#Import data manipulation packages
import pandas as pd
import numpy as np

#Import data visualization packages
import matplotlib as mpl

#Toggle option to print dataframes to csv
printToCSV = True

#Access stats from pro-football-reference.com
url_passing = "https://www.pro-football-reference.com/years/2021/passing.htm"
url_receiving = "https://www.pro-football-reference.com/years/2021/receiving.htm"
url_rushing = "https://www.pro-football-reference.com/years/2021/rushing.htm"
url_kicking = "https://www.pro-football-reference.com/years/2021/kicking.htm"
url_fantasy = "https://www.pro-football-reference.com/years/2021/fantasy.htm"

http = urllib3.PoolManager(num_pools=5)

response_passing = http.request("GET", url_passing)
response_receiving = http.request("GET", url_receiving)
response_rushing = http.request("GET", url_rushing)
response_kicking = http.request("GET", url_kicking)
response_fantasy = http.request("GET", url_fantasy)

stats_page_passing = BeautifulSoup(response_passing.data, features="lxml")
stats_page_receiving = BeautifulSoup(response_receiving.data, features="lxml")
stats_page_rushing = BeautifulSoup(response_rushing.data, features="lxml")
stats_page_kicking = BeautifulSoup(response_kicking.data, features="lxml")
stats_page_fantasy = BeautifulSoup(response_fantasy.data, features="lxml")

#Get stat tables

#Get column headers (row [0])
column_headers_passing = stats_page_passing.findAll('tr')[0]
column_headers_passing = [i.getText() for i in column_headers_passing.findAll('th')]

column_headers_receiving = stats_page_receiving.findAll('tr')[0]
column_headers_receiving = [i.getText() for i in column_headers_receiving.findAll('th')]

column_headers_rushing = stats_page_rushing.findAll('tr')[1] #rushing table has extra heading line
column_headers_rushing = [i.getText() for i in column_headers_rushing.findAll('th')]

column_headers_kicking = stats_page_kicking.findAll('tr')[1] #kicking table has extra heading line
column_headers_kicking = [i.getText() for i in column_headers_kicking.findAll('th')]

column_headers_fantasy = stats_page_fantasy.findAll('tr')[1] #fantasy table has extra heading line
column_headers_fantasy = [i.getText() for i in column_headers_fantasy.findAll('th')]

#Get table rows (not headers, so row [1:])
rows_passing = stats_page_passing.findAll('tr')[1:]
rows_receiving = stats_page_receiving.findAll('tr')[1:]
rows_rushing = stats_page_rushing.findAll('tr')[2:] #rushing table has extra heading line
rows_kicking = stats_page_kicking.findAll('tr')[2:] #kicking table has extra heading line
rows_fantasy = stats_page_fantasy.findAll('tr')[2:] #fantasy table has extra heading line

#Loop over rows to fill lists with stats from each column in tables for position groups
passing_stats = []
receiving_stats = []
rushing_stats = []
kicking_stats = []
fantasy_stats = []

for i in range(len(rows_passing)):
    passing_stats.append([j.getText() for j in rows_passing[i].findAll('td')])
for i in range(len(rows_receiving)):
    receiving_stats.append([j.getText() for j in rows_receiving[i].findAll('td')])
for i in range(len(rows_rushing)):
    rushing_stats.append([j.getText() for j in rows_rushing[i].findAll('td')])
for i in range(len(rows_kicking)):
    kicking_stats.append([j.getText() for j in rows_kicking[i].findAll('td')])
for i in range(len(rows_fantasy)):
    fantasy_stats.append([j.getText() for j in rows_fantasy[i].findAll('td')])

#Create DataFrames
passing_data = pd.DataFrame(passing_stats, columns=column_headers_passing[1:]) #exclude 0th element because "Rk" column was not pulled from tables
receiving_data = pd.DataFrame(receiving_stats, columns=column_headers_receiving[1:]) #exclude 0th element because "Rk" column was not pulled from tables
rushing_data = pd.DataFrame(rushing_stats, columns=column_headers_rushing[1:]) #exclude 0th element because "Rk" column was not pulled from tables
kicking_data = pd.DataFrame(kicking_stats, columns=column_headers_kicking[1:]) #exclude 0th element because "Rk" column was not pulled from tables
fantasy_data = pd.DataFrame(fantasy_stats, columns=column_headers_fantasy[1:]) #exclude 0th element because "Rk" column was not pulled from tables

#Clean up data

#Rename duplicate column in passing stats table (change 2nd "Yds" to "Sack_Yds")
new_columns_passing = passing_data.columns.values
new_columns_passing[-6] = 'Sack_Yds'
passing_data.columns = new_columns_passing

#Rename duplicate column names in kicking stats table (change "FGA" and "FGM" for various distance ranges to be unique)
new_columns_kicking = kicking_data.columns.values
new_columns_kicking[6] = 'FGA0_19'
new_columns_kicking[7] = 'FGM0_19'
new_columns_kicking[8] = 'FGA20_29'
new_columns_kicking[9] = 'FGM20_29'
new_columns_kicking[10] = 'FGA30_39'
new_columns_kicking[11] = 'FGM30_39'
new_columns_kicking[12] = 'FGA40_49'
new_columns_kicking[13] = 'FGM40_49'
new_columns_kicking[14] = 'FGA50plus'
new_columns_kicking[15] = 'FGM50plus'
new_columns_kicking[18] = 'LngFG'
new_columns_kicking[30] = 'LngPnt'
kicking_data.columns = new_columns_kicking

#Rename duplicate column names in fantasy stats table (differentiate between passing/receiving/rushing yards/attempts/TDs)
new_columns_fantasy = fantasy_data.columns.values
new_columns_fantasy[7] = 'PassAtt'
new_columns_fantasy[8] = 'PassYds'
new_columns_fantasy[9] = 'PassTD'
new_columns_fantasy[11] = 'RushAtt'
new_columns_fantasy[12] = 'RushYds'
new_columns_fantasy[14] = 'RushTD'
new_columns_fantasy[17] = 'RecYds'
new_columns_fantasy[19] = 'RecTD'
new_columns_fantasy[22] = 'TotalTD'
fantasy_data.columns = new_columns_fantasy

#Remove extra characters from player names ("*" and "+" were used to denote Pro Bowl and All-Pro selections)
passing_data['Player'] = passing_data['Player'].str.replace('*','')
passing_data['Player'] = passing_data['Player'].str.replace('+','')
passing_data['Player'] = passing_data['Player'].str.strip()
receiving_data['Player'] = receiving_data['Player'].str.replace('*','')
receiving_data['Player'] = receiving_data['Player'].str.replace('+','')
receiving_data['Player'] = receiving_data['Player'].str.strip()
rushing_data['Player'] = rushing_data['Player'].str.replace('*','')
rushing_data['Player'] = rushing_data['Player'].str.replace('+','')
rushing_data['Player'] = rushing_data['Player'].str.strip()
kicking_data['Player'] = kicking_data['Player'].str.replace('*','')
kicking_data['Player'] = kicking_data['Player'].str.replace('+','')
kicking_data['Player'] = kicking_data['Player'].str.strip()
fantasy_data['Player'] = fantasy_data['Player'].str.replace('*','')
fantasy_data['Player'] = fantasy_data['Player'].str.replace('+','')
fantasy_data['Player'] = fantasy_data['Player'].str.strip()
#Remove "%" signs from percentage metrics
receiving_data['Ctch%'] = receiving_data['Ctch%'].str.replace('%','')
kicking_data['FG%'] = kicking_data['FG%'].str.replace('%','')
kicking_data['XP%'] = kicking_data['XP%'].str.replace('%','')
kicking_data['TB%'] = kicking_data['TB%'].str.replace('%','')

#Fill blank cells with zeros
##Note: be careful with this if calculating any ratios or percentils, as zeros might not play nicely and/or incorrectly skew results 
###Likely only using counting stats for what I have planned so no problem, but could replace blanks with np.NaN instead
passing_data = passing_data.replace(r'^\s*$', 0, regex=True)
receiving_data = receiving_data.replace(r'^\s*$', 0, regex=True)
rushing_data = rushing_data.replace(r'^\s*$', 0, regex=True)
kicking_data = kicking_data.replace(r'^\s*$', 0, regex=True)
fantasy_data = fantasy_data.replace(r'^\s*$', 0, regex=True)

#Remove blank rows
##IMPORTANT: Must come after blank cells are filled or else entire rows of content may be removed
passing_data['Player'] = passing_data['Player'].replace(r'^\s*$', np.NaN, regex=True)
receiving_data['Player'] = receiving_data['Player'].replace(r'^\s*$', np.NaN, regex=True)
rushing_data['Player'] = rushing_data['Player'].replace(r'^\s*$', np.NaN, regex=True)
kicking_data['Player'] = kicking_data['Player'].replace(r'^\s*$', np.NaN, regex=True)
fantasy_data['Player'] = fantasy_data['Player'].replace(r'^\s*$', np.NaN, regex=True)
passing_data.dropna(subset = ['Player'], inplace=True)
receiving_data.dropna(subset = ['Player'], inplace=True)
rushing_data.dropna(subset = ['Player'], inplace=True)
kicking_data.dropna(subset = ['Player'], inplace=True)
fantasy_data.dropna(subset = ['Player'], inplace=True)

#If we check the data types in each DataFrame (e.g. passing_data.dtypes), we see that numerical values are incorrectly stored as "object" type variables
#Let's convert them to numerical values
numericCats_passing = ['Age', 'G', 'GS', 'Cmp', 'Att', 'Cmp%', 'Yds', 'TD', 'TD%', 'Int', 'Int%', '1D', 'Lng', 'Y/A', 'AY/A', 'Y/C', 'Y/G', 'Rate', 'QBR', 'Sk', 'Sack_Yds', 'Sk%', 'NY/A', 'ANY/A', '4QC', 'GWD']
numericCats_receiving = ['Age', 'G', 'GS', 'Tgt', 'Rec', 'Ctch%', 'Yds', 'Y/R', 'TD', '1D', 'Lng', 'Y/Tgt', 'R/G', 'Y/G', 'Fmb']
numericCats_rushing = ['Age', 'G', 'GS', 'Att', 'Yds', 'TD', '1D', 'Lng', 'Y/A', 'Y/G', 'Fmb']
numericCats_kicking = ['Age', 'G', 'GS', 'FGA0_19', 'FGM0_19', 'FGA20_29', 'FGM20_29', 'FGA30_39', 'FGM30_39', 'FGA40_49', 'FGM40_49', 'FGA50plus', 'FGM50plus', 'FGA', 'FGM', 'LngFG', 'FG%', 'XPA', 'XPM', 'XP%', 'KO', 'KOYds', 'TB', 'TB%', 'KOAvg', 'Pnt', 'Yds', 'LngPnt', 'Blck', 'Y/P']
numericCats_fantasy = ['Age', 'G', 'GS', 'Cmp', 'PassAtt', 'PassYds', 'PassTD', 'Int', 'RushAtt', 'RushYds', 'Y/A', 'RushTD', 'Tgt', 'Rec', 'RecYds', 'Y/R', 'RecTD', 'Fmb', 'FL', 'TotalTD', '2PM', '2PP', 'FantPt', 'PPR', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank']

for i in numericCats_passing:
    passing_data[i] = pd.to_numeric(passing_data[i])
for i in numericCats_receiving:
    receiving_data[i] = pd.to_numeric(receiving_data[i])
for i in numericCats_rushing:
    rushing_data[i] = pd.to_numeric(rushing_data[i])
for i in numericCats_kicking:
    kicking_data[i] = pd.to_numeric(kicking_data[i])
for i in numericCats_fantasy:
    fantasy_data[i] = pd.to_numeric(fantasy_data[i])

if printToCSV:
    passing_data.to_csv(r'NFLPassingData2021.csv', index = False, header = True)
    receiving_data.to_csv(r'NFLReceivingData2021.csv', index = False, header = True)
    rushing_data.to_csv(r'NFLRushingData2021.csv', index = False, header = True)
    kicking_data.to_csv(r'NFLKickingData2021.csv', index = False, header = True)
    fantasy_data.to_csv(r'NFLFantasyData2021.csv', index = False, header = True)

#Test prints
#print(passing_data.head())
#print(receiving_data.head())
#print(rushing_data.head())
#print(kicking_data.head())
#print(fantasy_data.head())
#print(passing_data.dtypes)
#print(receiving_data.dtypes)
#print(rushing_data.dtypes)
#print(kicking_data.dtypes)
#print(fantasy_data.dtypes)