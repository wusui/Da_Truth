# Fantrax Data Scraper

Collect Roto League data into local csv files

## Use

- get_data.py collects all non-rostered players into available_players.csv
- get_teams.py creates a csv file for each team in the league.

## ini File

gnus.ini contains the following fields in the DEFAULT section:
- username
- passwd
- league: The league id (16 lower case and numeric characters)
- downloaddir: Folder where downloads get sent on your system

## General Description

Selenium is used to provide webpage access, and the download button made
available by Fantrax is used to download the data.  Csv files are
rather clunkily copied locally.

This ain't very efficient, but even obsessive people have no need
to run this more than once a day.

This software is licensed under the MIT license.

