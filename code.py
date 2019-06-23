# --------------
import pandas as pd 
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# Load the dataset and create column `year` which stores the year in which match was played
df = pd.read_csv(path)
df['year'] = df['date'].apply(lambda x:pd.to_datetime(x, format="%Y-%m-%d").year)
# Plot the wins gained by teams across all seasons
win = df[['match_code', 'winner']].drop_duplicates().groupby(['winner']).count()
win.sort_values('match_code', ascending=False).plot(kind='bar', figsize=[15,10])
plt.xlabel('Teams')
plt.ylabel('Win Count')
plt.title('Bar plot for Win Count')
plt.legend().remove()
plt.show()
# Plot Number of matches played by each team through all seasons
total_matches = df[['match_code', 'team1', 'team2']].drop_duplicates()
total_matches = pd.concat([total_matches['team1'], total_matches['team2']])
total_matches.value_counts().plot(kind='bar', figsize=[14,8])
plt.xlabel('Teams')
plt.ylabel('Matchs played')
plt.title('Total Match Played Count')
plt.show()
# Top bowlers through all seasons
wicket = df[(df.player_out.notnull()) & (df.wicket_kind!='run_out')][['bowler']]
print(wicket['bowler'].value_counts())
# How did the different pitches behave? What was the average score for each stadium?
venue_avg_score = df.groupby(['venue', 'match_code', 'inning'])['total'].sum()
venue_avg_score.reset_index(level=['match_code', 'inning'], drop=True, inplace=True)
venue_avg_score = venue_avg_score.reset_index()
print(venue_avg_score.groupby('venue').mean())
# Types of Dismissal and how often they occur
wicket_type = df[df.wicket_kind.notnull()][['wicket_kind']]
print(wicket_type['wicket_kind'].value_counts())
# Plot no. of boundaries across IPL seasons
four = df[df.runs==4].groupby('year').size().reset_index().rename(columns={0:4})
six = df[df.runs==6].groupby('year').size().reset_index().rename(columns={0:6})
boundry = pd.merge(left=four, right=six, how='outer', on='year').set_index('year')
boundry.plot(kind='bar', figsize=[8,6])
plt.xlabel('Seasons')
plt.ylabel('Boundaries count')
plt.title('Boundaries across IPL seasons')
plt.show()
# Average statistics across all seasons
no_of_matches = df.groupby(['year'])['match_code'].nunique()
avg_runspermatch = df.groupby(['year', 'match_code'])['total'].sum()
avg_runspermatch.reset_index('match_code', drop=True, inplace=True)
avg_runspermatch = avg_runspermatch.reset_index()
avg_runspermatch = avg_runspermatch.groupby('year')['total'].mean()
avg_bowlspermatch = df.groupby(['year', 'match_code']).size()
avg_bowlspermatch.reset_index('match_code', drop=True, inplace=True)
avg_bowlspermatch = avg_bowlspermatch.reset_index()
avg_bowlspermatch = avg_bowlspermatch.groupby('year').mean()
avg_stats = pd.concat([no_of_matches, avg_runspermatch, avg_bowlspermatch], axis=1)
avg_stats.rename(columns={'match_code':'Match Count', 'total':'Avg Runs/Match', 0:'Avg Bowls/Match'}, inplace=True)
avg_stats['Avg Runs/Ball'] = avg_stats['Avg Runs/Match']/avg_stats['Avg Bowls/Match']
print(avg_stats)


