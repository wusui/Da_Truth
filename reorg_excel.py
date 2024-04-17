# Copyright (C) 2024 Warren Usui, MIT License
"""
Copy all local csv files into one new excel file
"""
import os
import time
from datetime import datetime
from io import StringIO
import pandas as pd

def reorg_excel():
    """
    Move information into excel files
    """
    ofilen = f"gnus-{datetime.today().strftime('%Y-%m-%d')}.xlsx"
    dfa = pd.read_csv('available_players.csv')
    dfa.to_excel(ofilen, sheet_name='data')
    os.remove('available_players.csv')
    time.sleep(2)
    pllist = list(filter(lambda a: a.endswith('.csv'), os.listdir()))
    for team in pllist:
        if team.startswith('avail'):
            continue
        print(team)
        with open(team, 'r', encoding='utf-8') as tcsv:
            csv_text = tcsv.read()
        brk = csv_text.find('\n\n')
        bat_str = csv_text[:brk + 1]
        bat_str = '\n'.join(bat_str.split('\n')[1:])
        pit_str = csv_text[brk+2:]
        pit_str = '\n'.join(pit_str.split('\n')[1:])
        df1 = pd.read_csv(StringIO(bat_str))
        df2 = pd.read_csv(StringIO(pit_str))
        team_tab = team.split('.')[0]
        excelf = '.'.join([team_tab, "xlsx"])
        df1.to_excel(excelf, sheet_name='Batting', index=False)
        # pylint: disable=abstract-class-instantiated
        with pd.ExcelWriter(excelf, engine='openpyxl', mode='a') as writer:
            df2.to_excel(writer, sheet_name='Pitching', index=False)
        os.remove(team)
        time.sleep(2)

if __name__ == "__main__":
    reorg_excel()
