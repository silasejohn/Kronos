import csv

import pandas

# setup lists for different roles
player_role_top = {}
player_role_jgl = {}
player_role_mid = {}
player_role_adc = {}
player_role_sup = {}

tier_one_teams = ["Gen.G eSports", "JD Gaming", "LNG Esports"]
tier_two_teams = ["T1", "Bilibili Gaming", "KT Rolster", "Weibo Gaming"]
tier_three_teams = ["NRG"]

# open player_list file for player_info
output_csv_file_name_overview = f"2023_Worlds_Swiss/data_analyzed/overview.csv"
output_file_1 = f"2023_Worlds_Swiss/data_analyzed/top.csv"
output_file_2 = f"2023_Worlds_Swiss/data_analyzed/jgl.csv"
output_file_3 = f"2023_Worlds_Swiss/data_analyzed/mid.csv"
output_file_4 = f"2023_Worlds_Swiss/data_analyzed/adc.csv"
output_file_5 = f"2023_Worlds_Swiss/data_analyzed/sup.csv"
output_csv_files = [output_csv_file_name_overview, output_file_1, output_file_2, output_file_3, output_file_4, output_file_5]

player_list = open('player_list.txt', "r")

df_player_tier = []
df_player_role = []
df_player_team_names = []
df_player_names = []
df_player_costs = []
df_player_games_played = []
df_player_total_pts = []
df_player_standardized_score = []

# for each player in the file... store their info
player_num = 0
for player_info in player_list:
    team_id = player_info.split('|')[0].strip()
    team_name = player_info.split('|')[1].strip()
    player_name = player_info.split('|')[2].strip()
    player_id = player_info.split('|')[3].strip()
    player_role = player_info.split('|')[4].strip()
    player_cost = player_info.split('|')[5].strip()

    df_player_team_names.append(team_name)
    df_player_names.append(player_name)
    df_player_role.append(player_role)
    df_player_costs.append(player_cost)

    player_tier = 0
    if team_name in tier_one_teams:
        player_tier = 1
    elif team_name in tier_two_teams:
        player_tier = 2
    else:
        player_tier = 3

    df_player_tier.append(player_tier)

    input_csv_file = f"2023_Worlds_Swiss/data_processed/{player_name}.csv"
    processed_player_df = pandas.read_csv(input_csv_file)

    total_pts = 0
    num_total_games = processed_player_df.shape[0]
    df_player_games_played.append(num_total_games)

    for match in range(num_total_games):
        total_pts = total_pts + float(processed_player_df.iloc[match].PTV)
        total_pts = round(total_pts, 2)

    df_player_total_pts.append(total_pts)

    standardized_total_pts = total_pts / num_total_games
    df_player_standardized_score.append(standardized_total_pts)

    print(f"[{player_tier}] Player Name: {player_name} ... {standardized_total_pts}")

    tiered_player_name = player_name + "_" + str(player_tier)
    if player_role == "Top":
        player_role_top[tiered_player_name] = standardized_total_pts
    elif player_role == "Jungle":
        player_role_jgl[tiered_player_name] = standardized_total_pts
    elif player_role == "Mid":
        player_role_mid[tiered_player_name] = standardized_total_pts
    elif player_role == "ADC":
        player_role_adc[tiered_player_name] = standardized_total_pts
    elif player_role == "Support":
        player_role_sup[tiered_player_name] = standardized_total_pts

    analyzed_player_df = 0
    analyzed_player_df = pandas.DataFrame(
        {
            "player_tier": df_player_tier,
            "player_role": df_player_role,
            "team_name": df_player_team_names,
            "player_name": df_player_names,
            "player_cost": df_player_costs,
            "games_played": df_player_games_played,
            "player_total_pts": df_player_total_pts,
            "player_standardized_score": df_player_standardized_score
        }
    )

    player_num = player_num + 1

# open the GENERAL CSV file
csv_counter = 0
for csv_file_name in output_csv_files:
    with open(csv_file_name, 'w', newline='') as file:
        writer = csv.writer(file)

        # writer HEADERS to each csv file
        headers = ["player_tier", "player_role", "team_name", "player_name", "player_cost", "games_played", "player_total_pts",
                   "player_standardized_score"]
        writer.writerow(headers)

        # write DATA for each HEADER to csv file
        for player_row in range(0, player_num):  # iterate number of games played for team
            csv_write = False
            if analyzed_player_df.iloc[player_row][1] == "Top" and (csv_counter == 0 or csv_counter == 1):
                csv_write = True
            elif analyzed_player_df.iloc[player_row][1] == "Jungle" and (csv_counter == 0 or csv_counter == 2):
                csv_write = True
            elif analyzed_player_df.iloc[player_row][1] == "Mid" and (csv_counter == 0 or csv_counter == 3):
                csv_write = True
            elif analyzed_player_df.iloc[player_row][1] == "ADC" and (csv_counter == 0 or csv_counter == 4):
                csv_write = True
            elif analyzed_player_df.iloc[player_row][1] == "Support" and (csv_counter == 0 or csv_counter == 5):
                csv_write = True
            else:
                csv_write = False
            if csv_write:
                row = list(analyzed_player_df.iloc[player_row])
                print(row)  # DEBUG print statement
                writer.writerow(row)  # write data to CSV file
    csv_counter = csv_counter + 1

def value_getter(item):
    return item[1]

print("Player Role Top: ", sorted(player_role_top.items(), key=value_getter))
print("player_role_jgl: ", sorted(player_role_jgl.items(), key=value_getter))
print("player_role_mid: ", sorted(player_role_mid.items(), key=value_getter))
print("player_role_adc: ", sorted(player_role_adc.items(), key=value_getter))
print("player_role_sup: ", sorted(player_role_sup.items(), key=value_getter))
