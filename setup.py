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
import numpy as np
import pandas as pd
import csv

# utilize chunking to break up large CSV files (might need later)
# chunk_size = 1000
# chunk_idx = 0
# for chunk in pd.read_csv(league_data_csv, chunksize=chunk_size):
#     print(chunk_idx)
#     chunk_idx = chunk_idx + 1
#     print(chunk)

league_data_csv = '2024_LOL_Esports_Data.csv'
relevant_metadata_headers = ["gameid", "datacompleteness", "league", "year", "split", "playoffs", "date", "game", "gamelength"]
relevant_player_headers = ["participantid", "position", "playername", "playerid", "teamname", "teamid", "result", "kills", "assists", "deaths", "total cs", "teamkills", "teamdeaths", "cspm", "damageshare", "earnedgoldshare"]
relevant_team_headers = ["participantid", "teamname", "teamid", "result", "teamkills", "assists", "teamdeaths", "dragons", "opp_dragons", "heralds", "opp_heralds", "barons", "opp_barons", "towers"]
relevant_headers = relevant_metadata_headers + relevant_player_headers + relevant_team_headers

# read in league data csv into a dataframe
league_data_df = pd.read_csv(league_data_csv)
num_total_rows = league_data_df.shape[0]
print(league_data_df.head())

# only keep headers with relevant data
relevant_league_data_df = league_data_df[relevant_headers]
print(relevant_league_data_df.head())


def craft_player_csv(initial_df, league, split, position):
    # selecting rows based on condition
    processed_df1 = initial_df.loc[np.logical_and(initial_df['league'] == league, initial_df['position'] == position)]
    processed_df2 = processed_df1.loc[processed_df1['split'] == split]
    output_csv_file_name = f"2024/data_raw/{league}/{split}/{position}.csv"
    write_to_csv(processed_df2, output_csv_file_name)


def write_to_csv(input_df, output_csv, csv_headers=0):
    with open(output_csv, 'w', newline='') as file:
        # determine rows in input_df
        df_num_rows = input_df.shape[0]

        # if no custom headers, set to dataframe headers
        if csv_headers == 0:
            csv_headers = list(input_df.columns)

        # write headers to CSV output file
        csv_writer = csv.writer(file)
        csv_writer.writerow(csv_headers)

        # write data to CSV output file
        for df_row_idx in range(0, df_num_rows):
            csv_row = list(input_df.iloc[df_row_idx])
            csv_writer.writerow(csv_row)


output_test_csv_file_name = f"testing/output1.csv"
write_to_csv(relevant_league_data_df, output_test_csv_file_name, csv_headers=relevant_headers)

craft_player_csv(relevant_league_data_df, "LEC", "Winter", "top")
craft_player_csv(relevant_league_data_df, "LEC", "Winter", "jng")
craft_player_csv(relevant_league_data_df, "LEC", "Winter", "mid")
craft_player_csv(relevant_league_data_df, "LEC", "Winter", "bot")
craft_player_csv(relevant_league_data_df, "LEC", "Winter", "sup")

