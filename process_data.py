import pandas

player_list = open('player_list.txt', "r")
player_names = []

for player_info in player_list:
    player_name = player_info.split('|')[2].strip()
    player_names.append(player_name)

for player_name in player_names:
    csv_file_name = f"2023_Worlds_Swiss/data_raw/{player_name}.csv"

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
    df_PTV = []

    raw_player_df = pandas.read_csv(csv_file_name)

    # iterate over number of games played
    for match in range(raw_player_df.shape[0]):
        # processing based on page_game link
        pass

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
            "PTV": df_PTV
        }
    )
    print(processed_player_df)