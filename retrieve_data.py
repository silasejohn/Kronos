# -*- coding: utf-8 -*-
import csv
import os
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
DEBUG = False


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
    player_id = player_info.split('|')[0].strip()
    player_name = player_info.split('|')[1].strip()
    team_id = player_info.split('|')[2].strip()
    team_name = player_info.split('|')[3].strip()

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
        table = soup.find("table", attrs={"class": "table_list"})
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            i = [ele for ele in cols if ele]
            if i:
                print(i)
                match_list.append(i)

        # DEBUG: print match-list data to console
        if DEBUG:
            print(match_list)

        # open player-specific CSV... output relevant data
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)

            # writer headers to csv file
            headers = ["champName", "gameOutcome", "KDA", "gameTime", "gameDate", "matchup", "split"]
            writer.writerow(headers)

            # write match-data columns to csv file
            for i in range(0, len(match_list)):
                writer.writerow(match_list[i])

        print("Successfully scraped ", player_name)

    if DEBUG:
        break  # single iteration for testing purposes
