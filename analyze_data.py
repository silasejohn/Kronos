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
player_list = open('player_list.txt', "r")

# for each player in the file... store their info
for player_info in player_list:
    team_id = player_info.split('|')[0].strip()
    team_name = player_info.split('|')[1].strip()
    player_name = player_info.split('|')[2].strip()
    player_id = player_info.split('|')[3].strip()
    player_role = player_info.split('|')[4].strip()

    player_tier = 0
    if team_name in tier_one_teams:
        player_tier = 1
    elif team_name in tier_two_teams:
        player_tier = 2
    else:
        player_tier = 3

    input_csv_file = f"2023_Worlds_Swiss/data_processed/{player_name}.csv"
    processed_player_df = pandas.read_csv(input_csv_file)

    total_pts = 0
    num_total_games = processed_player_df.shape[0]

    for match in range(num_total_games):
        total_pts = total_pts + float(processed_player_df.iloc[match].PTV)
        total_pts = round(total_pts, 2)

    standardized_total_pts = total_pts / num_total_games
    print(f"[{player_tier}] Player Name: {player_name} ... {standardized_total_pts}")

    if player_role == "Top":
        player_role_top[player_name] = standardized_total_pts
    elif player_role == "Jungle":
        player_role_jgl[player_name] = standardized_total_pts
    elif player_role == "Mid":
        player_role_mid[player_name] = standardized_total_pts
    elif player_role == "ADC":
        player_role_adc[player_name] = standardized_total_pts
    elif player_role == "Support":
        player_role_sup[player_name] = standardized_total_pts

def value_getter(item):
    return item[1]

print("Player Role Top: ", sorted(player_role_top.items(), key=value_getter))
print("player_role_jgl: ", player_role_jgl)
print("player_role_mid: ", player_role_mid)
print("player_role_adc: ", player_role_adc)
print("player_role_sup: ", player_role_sup)
