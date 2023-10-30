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

    # printing processed data from input file
    searching_msg = "Searching database for {arg1} [{arg2}] player {arg3} [{arg4}]...".format(arg1=team_name,
                                                                                              arg2=team_id,
                                                                                              arg3=player_name,
                                                                                              arg4=player_id)
    print(searching_msg)

    # generating custom player file path
    filepath = f"2023_Worlds_Swiss/data_raw/{player_name}.csv"

    # check if player has already been processed
    if os.path.exists(filepath):
        print("Already scraped. If you would like to re-scrape, please delete the file and try again.")
    else:
        # url for scraping data ... depends on input parameters
        match_list = []  # will store important scraped data for player
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
            match_value = [ele for ele in match_text_ele if ele]  # if not empty, then proceed
            if match_value:
                print(match_value)
                match_list.append(match_value)

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
                        match_list[-1].append(absolute_link_to_game_page)  # add full link to the last match_list

        # DEBUG: print match-list data to console
        if DEBUG:
            print(match_list)

        # open player-specific CSV... output relevant data
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)

            # writer headers to csv file
            headers = ["gameID", "champName", "gameOutcome", "KDA", "gameTime", "gameDate", "matchup", "split", "gameLink"]
            writer.writerow(headers)

            # write match-data columns to csv file
            for i in range(0, len(match_list)):
                writer.writerow(match_list[i])

        print("Successfully scraped ", player_name)

    if DEBUG:
        break  # single iteration for testing purposes
