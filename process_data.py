import csv

import pandas

player_list = open('player_list.txt', "r")
player_names = []

# KILLS, DEATHS, ASSISTS, CS + METAGAME pts
static_vals_top = [float(0.40), float(-0.15), float(0.20), float(0.02)]
static_vals_jgl = [float(0.40), float(-0.15), float(0.20), float(0.02)]
static_vals_mid = [float(0.40), float(-0.20), float(0.15), float(0.015)]
static_vals_adc = [float(0.40), float(-0.20), float(0.15), float(0.015)]
static_vals_sup = [float(0.40), float(-0.10), float(0.35), float(0.03)]
static_vals_meta = [float(0.10), float(0.20), float(0.50), float(0.50)]
static_win = float(2.00)

for player_info in player_list:
    player_name = player_info.split('|')[2].strip()
    player_names.append(player_name)

for player_name in player_names:
    input_csv_file_name = f"2023_Worlds_Swiss/data_raw/{player_name}.csv"
    output_csv_file_name = f"2023_Worlds_Swiss/data_processed/{player_name}.csv"

    # dataframe specific arrays
    df_kills = []
    df_deaths = []
    df_assists = []
    df_cs = []
    df_turrets = []
    df_dragons = []
    df_barons = []
    df_first_blood = []
    df_CS_pts = []
    df_KDA_pts = []
    df_TDFB_pts = []
    df_WIN_pts = []
    df_PTV = []

    raw_player_df = pandas.read_csv(input_csv_file_name)
    print(raw_player_df)
    player_role = raw_player_df.iloc[0].EgoPlayerRole
    static_vals = []

    if player_role == "Top":
        static_vals = static_vals_top
    elif player_role == "Jungle":
        static_vals = static_vals_jgl
    elif player_role == "Mid":
        static_vals = static_vals_mid
    elif player_role == "ADC":
        static_vals = static_vals_adc
    elif player_role == "Support":
        static_vals = static_vals_sup

    # iterate over number of games played
    # 0-4 ... ["GamePageID", "Tournament", "GameOutcome", "GameTime", "EgoPlayerRole",
    # 5-9... "EgoPlayerTeam", "OppoPlayerTeam", "PlayerKills", "PlayerDeaths", "PlayerAssists",
    # 10-14..."PlayerCS", "TeamTurrets", "TeamDrakes", "TeamBarons", "TeamFirstBlood",
    # 15... "GameLink"]
    num_total_matches = raw_player_df.shape[0]
    print("Total Matches: ", num_total_matches)
    for match in range(num_total_matches):
        print("[Player Name]", player_name, "[Match Number]", match)
        df_kills.append(raw_player_df.iloc[match].PlayerKills)
        df_deaths.append(raw_player_df.iloc[match].PlayerDeaths)
        df_assists.append(raw_player_df.iloc[match].PlayerAssists)
        df_cs.append(raw_player_df.iloc[match].PlayerCS)
        df_turrets.append(raw_player_df.iloc[match].TeamTurrets)
        df_dragons.append(raw_player_df.iloc[match].TeamDrakes)
        df_barons.append(raw_player_df.iloc[match].TeamBarons)
        df_first_blood.append(raw_player_df.iloc[match].TeamFirstBlood)

        K_pts = static_vals[0] * float(raw_player_df.iloc[match].PlayerKills)
        D_pts = static_vals[1] * float(raw_player_df.iloc[match].PlayerDeaths)
        A_pts = static_vals[2] * float(raw_player_df.iloc[match].PlayerAssists)

        T_pts = static_vals_meta[0] * float(raw_player_df.iloc[match].TeamTurrets)
        Dr_pts = static_vals_meta[1] * float(raw_player_df.iloc[match].TeamDrakes)
        B_pts = static_vals_meta[2] * float(raw_player_df.iloc[match].TeamBarons)

        # generate First Blood Points
        if raw_player_df.iloc[match].TeamFirstBlood:
            FB_pts = static_vals_meta[3]
        elif not raw_player_df.iloc[match].TeamFirstBlood:
            FB_pts = 0
        else:
            print("errrr Problem with First Blood?")
            exit()

        # generate Team Outcome Points
        if raw_player_df.iloc[match].GameOutcome == "Victory":
            WIN_pts = static_win
        elif raw_player_df.iloc[match].GameOutcome == "Defeat":
            WIN_pts = 0
        else:
            print("errrr Problem with Game Outcome?")
            exit()

        # Sum KDA, CS, TDFB points into PTV
        KDA_pts = K_pts + D_pts + A_pts
        CS_pts = static_vals[3] * float(raw_player_df.iloc[match].PlayerCS)
        TDFB_pts = T_pts + Dr_pts + B_pts + FB_pts
        PTV_pts = KDA_pts + CS_pts + TDFB_pts + WIN_pts

        df_KDA_pts.append(KDA_pts)
        df_CS_pts.append(CS_pts)
        df_TDFB_pts.append(TDFB_pts)
        df_WIN_pts.append(WIN_pts)

        df_PTV.append(PTV_pts)
    # end for loop

    processed_player_df = pandas.DataFrame(
        {
            "kills": df_kills,
            "assists": df_deaths,
            "deaths": df_assists,
            "cs": df_cs,
            "turrets": df_turrets,
            "dragons": df_dragons,
            "barons": df_barons,
            "first_blood": df_first_blood,
            "CS_pts": df_CS_pts,
            "KDA_pts": df_KDA_pts,
            "TDFB_pts": df_TDFB_pts,
            "WIN_pts": df_WIN_pts,
            "PTV": df_PTV
        }
    )
    print(processed_player_df)

    # open the PLAYER CSV file (see filepath variable at top of this file)
    with open(output_csv_file_name, 'w', newline='') as file:
        writer = csv.writer(file)

        # writer HEADERS to each csv file
        headers = ["kills", "assists", "deaths", "cs", "turrets",
                   "dragons", "barons", "first_blood", "CS_pts", "KDA_pts",
                   "TDFB_pts", "WIN_pts", "PTV"]
        writer.writerow(headers)

        # write DATA for each HEADER to csv file
        for i in range(0, num_total_matches):  # iterate number of games played for team
            row = list(processed_player_df.iloc[i])  # steal a row of data for team X for game i from the 'team_df' dataframe
            print(row)  # DEBUG print statement
            writer.writerow(row)  # write data to CSV file

    output_msg = f"Successfully processed data for player {player_name}"
    print(output_msg)