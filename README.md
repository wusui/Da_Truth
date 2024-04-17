# Fantrax Data Scraper

Collect Roto League data 

## Use

- get_data.py collects all non-rostered players into available_players.csv
- get_teams.py creates a csv file for each team in the league
- reorg_excel.py rewrites all the csv files collected into excel files
- gen_yesterday_html.py displays yesterday's stats for your team
- get_player_stats.py collects player's stats for yesterday (called from gen_yesterday_html.py
- utilities.py contains functions used by the preceding files
- fantrax.py small run once executable to make all the above calls.

Yesterday is defined to be yesterday or today if after 11 PM.  Time zone
is assumed to be PDT.

## ini File

gnus.ini contains the following fields in the DEFAULT section:
- username
- passwd
- league: The league id (16 lower case and numeric characters)
- downloaddir: Folder where downloads get sent on your system
- extrastuff: Additional text found in some fantrax file links
- myteam: My fantasy team name
- mydir: Home directory of the files here

## Easiest Usecase

Run python fantrax.py

## General Description

Selenium is used to provide webpage access, and the download button made
available by Fantrax is used to download the data.  Csv files are
rather clunkily copied locally.

Get_player_stats.py makes use of a jinja2 template named dayscores.txt that
is stored in a directory named templates.

This ain't very efficient, but even obsessive people have no need
to run this more than once a day.

This software is licensed under the MIT license.

