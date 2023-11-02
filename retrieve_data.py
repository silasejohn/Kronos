# -*- coding: utf-8 -*-
import csv
import os
import re
import urllib

from bs4 import BeautifulSoup
import urllib.request as request


# // data scraping parameters //

# 'split-Summer', 'split-ALL/
SPLIT = "split-ALL/"
# 'tournament-ALL', 'tournament-Worlds%20Main%20Event%202023'
TOURNAMENT = "tournament-Worlds%20Main%20Event%202023"
# 'season-S13', 'season-ALL'
SEASON = "season-ALL"
# 'True', 'False'
DEBUG = True
MAIN_WEBSITE = "https://gol.gg"
enable_rescrape = True

# gol.gg implements server-side protection on normal urllib (classified as a boT??)
# anyway, this deprecated method slices through that...
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


# opening files, url_opener
player_list = open('player_list.txt', "r")
opener = AppURLopener()

"""
> Iterates through player_list.txt to identify persons of interest (for data scraping)
> Generating URLs + pulling response data + formatting for data processing / consumption
"""
for player_info in player_list:

    # reading, processing player info from file
    team_id = player_info.split('|')[0].strip()
    team_name = player_info.split('|')[1].strip()
    player_name = player_info.split('|')[2].strip()
    player_id = player_info.split('|')[3].strip()
    player_role = player_info.split('|')[4].strip()
    player_match_index = -1
    team_match_index = -1



    # printing processed data from input file
    searching_msg = "Searching database for {arg1} [{arg2}] player {arg3} [{arg4}]...".format(arg1=team_name,
                                                                                              arg2=team_id,
                                                                                              arg3=player_name,
                                                                                              arg4=player_id)
    print(searching_msg)

    # generating custom player file path
    filepath = f"2023_Worlds_Swiss/data_raw/{player_name}.csv"

    # check if player has already been processed
    if os.path.exists(filepath) and not enable_rescrape:
        print("Already scraped. If you would like to re-scrape, please delete the file and try again.")
    else:
        # url for scraping data ... depends on input parameters
        match_list = []  # will store important scraped data for player
        game_links = []  # link to all the URLs of games player has played
        url = f"https://gol.gg/players/player-matchlist/{player_id}/{SEASON}/{SPLIT}/{TOURNAMENT}/"

        # retrieve http web response into soup
        response = opener.open(url)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")

        # test and debug immediate file output
        if DEBUG:
            str_output = str(soup)
            with open('output.txt', 'w') as f:
                f.write(str_output)

        # scour player meta_data in soup
        name = soup.find("h1")
        print("Name: " + name.text)

        # score player match-specific data + append to a list
        match_table = soup.find("table", attrs={"class": "table_list"})  # symbolizes match list table
        list_of_matches = match_table.find_all('tr')  # symbolizes a table row - or a single match
        for match in list_of_matches:  # iterate through all the match games
            # obtaining metadata on state of match
            match_data = match.find_all('td')  # find all the html match data in a match-row
            match_text_ele = [html_elements.text.strip() for html_elements in match_data]  # strip title_text from html elements
            match_metadata = [ele for ele in match_text_ele if ele]  # if not empty, then proceed
            # Metadata contains... player champ, game status, player KDA, game time, date, matchup, tournament
            if match_metadata:
                relevant_match_metadata = []
                relevant_match_metadata.append(match_metadata[6])  # tournament
                relevant_match_metadata.append(match_metadata[1])  # game status
                relevant_match_metadata.append(match_metadata[3])  # game time
                print(relevant_match_metadata)
                match_list.append(relevant_match_metadata)

            # obtaining hyperlink + gameID to match-specific page
            for html_elements in match_data:
                # find all elements with a href element with hyperlink to games (regex-driven)
                all_link_info = str(html_elements.find_all("a", attrs={"href": re.compile(r"\.\.\/game.*")}))
                if len(all_link_info) > 2:  # do not sense the '[]' options
                    temp1 = all_link_info.split('title')[0].strip()  # gets the first part of href
                    temp2 = temp1.split('href=')[1].strip()  # gets second part of href
                    temp3 = temp2.replace("\"", "")  # formatting
                    relative_link_to_game_page = temp3.replace("..", "")  # formatting
                    temp4 = temp3.split("stats/")[1].strip()
                    game_ID = temp4.split("/page-game")[0].strip()
                    match_list[-1].insert(0, game_ID)
                    if relative_link_to_game_page:
                        absolute_link_to_game_page = f"{MAIN_WEBSITE}{relative_link_to_game_page}"
                        # match_list[-1].append(absolute_link_to_game_page)  # add full link to the last match_list
                        game_links.append(absolute_link_to_game_page)

        relative_game_index = 0
        for game_url in game_links:

            # retrieve http web response into soup
            opener = AppURLopener()
            response = opener.open(game_url)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            # print("Game_url is: ", game_url)

            # identify player_match_index on website for game page
            teams_competing_html = soup.find_all("a", attrs={"href": re.compile(r"../teams/team-stats/.*")})
            teams_competing = [html_element.text.strip() for html_element in teams_competing_html]
            # print(teams_competing)

            if team_name == teams_competing[0]:
                match_list[relative_game_index].append(teams_competing[0])
                match_list[relative_game_index].append(teams_competing[1])
                team_match_index = 0
                if player_role == "Top":
                    player_match_index = 0
                elif player_role == "Jungle":
                    player_match_index = 1
                elif player_role == "Mid":
                    player_match_index = 2
                elif player_role == "ADC":
                    player_match_index = 3
                elif player_role == "Support":
                    player_match_index = 4
                else:
                    print("problem?? ")
                    exit()
            elif team_name == teams_competing[1]:
                match_list[relative_game_index].append(teams_competing[1])
                match_list[relative_game_index].append(teams_competing[0])
                team_match_index = 1
                if player_role == "Top":
                    player_match_index = 5
                elif player_role == "Jungle":
                    player_match_index = 6
                elif player_role == "Mid":
                    player_match_index = 7
                elif player_role == "ADC":
                    player_match_index = 8
                elif player_role == "Support":
                    player_match_index = 9
                else:
                    print("problem?? ")
                    exit()

            # Item Of Interest: K / D / A
            # Order: Team 1 (Top, Jungle, Mid, ADC, Supp) ... Team 2 (Top, Jungle, Mid, ADC, Supp) ... idx[0:9]
            player_KDAs_raw = soup.find_all("td", attrs={"style": "text-align:center"})  # catches all html elements w/ KDA
            player_KDAs = [html_element.text.strip() for html_element in player_KDAs_raw]
            player_KDA = player_KDAs[player_match_index]

            kills = player_KDA.split('/')[0].strip()
            deaths = player_KDA.split('/')[1].strip()
            assists = player_KDA.split('/')[2].strip()

            match_list[relative_game_index].append(kills)
            match_list[relative_game_index].append(deaths)
            match_list[relative_game_index].append(assists)

            # ITEM Of Interest: CS
            player_CS_raw = soup.find_all("td", attrs={"style": "text-align:center;"})  # catches all html elements w/ cs
            player_CSs = [html_element.text.strip() for html_element in player_CS_raw]
            player_CS = player_CSs[player_match_index]

            match_list[relative_game_index].append(player_CS)

            # Item Of Interest: (need team name) Turr, Drag, Barons, First Blood
            # <div class="row" style="min-height:64px">
            game_meta_info_list = []

            # contains meta info on BOTH teams
            game_meta_info = soup.find_all("div", attrs={"class": "row", "style":"min-height:64px"})
            team_meta_info = game_meta_info[team_match_index]  # team_match_index

            # 6 options: team kills, towers, dragons, barons, team gold, [empty]
            team_meta_elements = team_meta_info.find_all("div", attrs={"class":"col-2"})

            # determines whether a team (for the current player) has first blood or not
            isFirstBlood = False
            first_blood_element = team_meta_elements[0].find("img", attrs={"alt" : "First Blood"})
            if first_blood_element is not None:
                isFirstBlood = True

            meta_text_ele = [html_element.text.strip() for html_element in
                              team_meta_elements]  # strip title_text from html elements
            metagame_values = [ele for ele in meta_text_ele if ele]  # if not empty, then proceed

            metagame_team_kills = metagame_values[0]
            metagame_towers = metagame_values[1]
            metagame_dragons = metagame_values[2]
            metagame_barons = metagame_values[3]
            metagame_team_gold = metagame_values[4]
            metagame_first_blood = isFirstBlood

            match_list[relative_game_index].append(metagame_towers)
            match_list[relative_game_index].append(metagame_dragons)
            match_list[relative_game_index].append(metagame_barons)
            match_list[relative_game_index].append(metagame_first_blood)

            relative_game_index = relative_game_index + 1

        # DEBUG: print match-list data to console
        if DEBUG:
            print(match_list)   # ORDER: GamePageID, Tournament, GameOutcome, GameTime, EgoPlayerTeam, OppoPlayerTeam
                                # PlayerKills, PlayerDeaths, PlayerAssists, PlayerCS,
                                # TeamTurrets, TeamDrakes, TeamBarons, TeamFirstBlood
            print(game_links)   # hyperlinks to all games player has played

        # open player-specific CSV... output relevant data
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)

            # writer headers to csv file
            headers = ["GamePageID", "Tournament", "GameOutcome", "GameTime", "EgoPlayerTeam", "OppoPlayerTeam",
                       "PlayerKills", "PlayerDeaths", "PlayerAssists", "PlayerCS", "TeamTurrets", "TeamDrakes",
                       "TeamBarons", "TeamFirstBlood"]
            writer.writerow(headers)

            # write match-data columns to csv file
            for i in range(0, len(match_list)):
                match_list[i].append(game_links[i])  # add the hyperlink to game page
                writer.writerow(match_list[i])

        print("Successfully scraped", player_name)

    if DEBUG:
        break  # single iteration for testing purposes
