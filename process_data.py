import csv

import pandas

player_list = open('player_list.txt', "r")
player_names = []

# KILLS, DEATHS, ASSISTS, CS + METAGAME pts
static_vals_top = [400, -150, 200, 20]
static_vals_jgl = [400, -150, 200, 20]
static_vals_mid = [400, -200, 150, 15]
static_vals_adc = [400, -200, 150, 15]
static_vals_sup = [400, -100, 350, 30]
static_vals_meta = [100, 200, 500, 500]
static_win = 2000

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

    df_K_pts = []
    df_D_pts = []
    df_A_pts = []

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
        df_kills.append(int(raw_player_df.iloc[match].PlayerKills))
        df_deaths.append(int(raw_player_df.iloc[match].PlayerDeaths))
        df_assists.append(int(raw_player_df.iloc[match].PlayerAssists))
        df_cs.append(int(raw_player_df.iloc[match].PlayerCS))
        df_turrets.append(int(raw_player_df.iloc[match].TeamTurrets))
        df_dragons.append(int(raw_player_df.iloc[match].TeamDrakes))
        df_barons.append(int(raw_player_df.iloc[match].TeamBarons))
        df_first_blood.append(bool(raw_player_df.iloc[match].TeamFirstBlood))

        K_pts = static_vals[0] * int(raw_player_df.iloc[match].PlayerKills)
        D_pts = static_vals[1] * int(raw_player_df.iloc[match].PlayerDeaths)
        A_pts = static_vals[2] * int(raw_player_df.iloc[match].PlayerAssists)

        df_K_pts.append(K_pts / 1000)
        df_D_pts.append(D_pts / 1000)
        df_A_pts.append(A_pts / 1000)

        T_pts = static_vals_meta[0] * int(raw_player_df.iloc[match].TeamTurrets)
        Dr_pts = static_vals_meta[1] * int(raw_player_df.iloc[match].TeamDrakes)
        B_pts = static_vals_meta[2] * int(raw_player_df.iloc[match].TeamBarons)

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
        KDA_pts_float = KDA_pts / 1000

        CS_pts = static_vals[3] * int(raw_player_df.iloc[match].PlayerCS)
        CS_pts_float = CS_pts / 1000

        TDFB_pts = T_pts + Dr_pts + B_pts + FB_pts
        TDFB_pts_float = TDFB_pts / 1000

        WIN_pts_float = WIN_pts / 1000

        PTV_pts = (KDA_pts + CS_pts + TDFB_pts + WIN_pts) / 1000

        df_KDA_pts.append(KDA_pts_float)
        df_CS_pts.append(CS_pts_float)
        df_TDFB_pts.append(TDFB_pts_float)
        df_WIN_pts.append(WIN_pts_float)

        df_PTV.append(PTV_pts)
    # end for loop

    processed_player_df = pandas.DataFrame(
        {
            "kills": df_kills,
            "deaths": df_deaths,
            "assists": df_assists,
            "cs": df_cs,
            "turrets": df_turrets,
            "dragons": df_dragons,
            "barons": df_barons,
            "first_blood": df_first_blood,
            "K_pts": df_K_pts,
            "D_pts": df_D_pts,
            "A_pts": df_A_pts,
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
                   "dragons", "barons", "first_blood", "K_pts", "D_pts", "A_pts", "CS_pts", "KDA_pts",
                   "TDFB_pts", "WIN_pts", "PTV"]
        writer.writerow(headers)

        # write DATA for each HEADER to csv file
        for i in range(0, num_total_matches):  # iterate number of games played for team
            row = list(processed_player_df.iloc[i])  # steal a row of data for team X for game i from the 'team_df' dataframe
            print(row)  # DEBUG print statement
            writer.writerow(row)  # write data to CSV file

    output_msg = f"Successfully processed data for player {player_name}"
    print(output_msg)