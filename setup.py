# using tournament data from Oracles Elixir

### DATA PARAMETERS ###
'''

METADATA STATS
[gameid] - unique alphanumerical identifier for game
[datacompleteness] - if data is complete or not ... set warning if NOT complete for future errors
[league] - specifies tournament or major league
>> DCup, LEC, LPL, LCK, LCS
[year] - specifies year of match
>> 2023, 2024
[split] - specifies split of match
>> NULL, Winter, Split 1, Spring
[playoffs] - boolean value specifying if the match is playoffs
[date] - specifies date and time of match
[game] - specifies the game number in a series
>> 1, 2, 3 ...
[gamelength] - time of game (M1M2S1S2)

PLAYER STATS
[participantid] - specifies the player
>> 1-6-top, 2-7-jng, 3-8-mid, 4-9-bot, 5-10-sup
[position] - position of player ... see above
[playername] [playerid] - name of player + ID of player
[teamname] [teamid] - name and ID of team
[result] - boolean value symbolizing win or loss (0 or 1)
[kills] [deaths] [assists] [total cs]- KDA per player
[teamkills] [teamdeaths] - use for carry and int potential relative to team
[cspm] [damageshare] [earnedgoldshare] - use for carry / int potential relative to team

TEAM STATS
[participantid] - specifies the team relative id
>> 100-Blue, 200-Red
[teamname] [teamid] - name and ID of team
[result] - boolean value symbolizing win or loss (0 or 1)
[assists] - assists per team
[teamkills] [teamdeaths] - use for carry and int potential relative to team
[dragons] [oppdragons] - for each team
[barons] [heralds] [opp_heralds] [opp_barons] - for each team
[towers] - for each team
'''

import pandas as pd

league_data_csv = '2024_LOL_Esports_Data.csv'
relevant_metadata_headers = ["gameid", "datacompleteness", "league", "year", "split", "playoffs", "date", "game", "gamelength"]
relevant_player_headers = ["participantid", "position", "playername", "playerid", "teamname", "teamid", "result", "kills", "assists", "deaths", "total cs", "teamkills", "teamdeaths", "cspm", "damageshare", "earnedgoldshare"]
relevant_team_headers = ["participantid", "teamname", "teamid", "result", "teamkills", "assists", "teamdeaths", "dragons", "opp_dragons", "heralds", "opp_heralds", "barons", "opp_barons", "towers"]
relevant_headers = relevant_metadata_headers + relevant_player_headers + relevant_team_headers

chunk_size = 1000
chunk_idx = 0

# for chunk in pd.read_csv(league_data_csv, chunksize=chunk_size):
#     print(chunk_idx)
#     chunk_idx = chunk_idx + 1
#     print(chunk)

league_data_df = pd.read_csv(league_data_csv)
print(league_data_df.head())


relevant_league_data_df = league_data_df[relevant_headers]
print(relevant_league_data_df.head())