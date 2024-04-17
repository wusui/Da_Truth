# Copyright (C) 2024 Warren Usui, MIT License
"""
Extract player stats
"""
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
from utilities import get_fpage, login_f, get_config

def get_player_stats(driver, player):
    """
    Extract stats from yesterday for each player.  Uses PDT and yesterday
    starts at midnight Mountain time.
    """
    def comp_outs(ipval):
        if '.' in ipval:
            oparts = ipval.split('.')
            return int(oparts[0]) * 3 + int(oparts[1])
        return int(ipval) * 3
    def get_drows(row_inf):
        if row_inf[0] == 0:
            return False
        gdate = list(map(lambda a: a.text, row_inf[1]))[0]
        tcheck = datetime.now()
        if tcheck.hour < 23:
            tcheck -= timedelta(1)
        cdate = ' '.join([tcheck.strftime("%b"), str(tcheck.day)])
        if gdate == cdate:
            return True
        return False
    def gen_results(drows):
        datav = drows.find_all('td')
        rowv = list(map(lambda a: a.text, datav))
        if len(rowv) > 20:
            return {'Player': player, 'Wins': int(rowv[7]),
                          'Saves': int(rowv[9]), 'Outs': comp_outs(rowv[12]),
                          'Hits': int(rowv[13]), 'Earned_Runs': int(rowv[15]),
                          'BB': int(rowv[17]), 'Ks': int(rowv[18])}
        return {'Player': player, 'AB': int(rowv[4]), 'Runs': int(rowv[5]),
                     'Hits': int(rowv[5]), 'HR': int(rowv[9]),
                     'RBI': int(rowv[10]), 'SB': int(rowv[13])}
    def get_key_from_xlsx():
        tname = get_config('myteam').replace(' ', '_')
        pl_df = pd.read_excel(f'{tname}.xlsx', sheet_name='Batting')
        pl_val = pl_df.loc[pl_df['Player'] == player]
        if len(pl_val) == 0:
            pl_df = pd.read_excel(f'{tname}.xlsx', sheet_name='Pitching')
            pl_val = pl_df.loc[pl_df['Player'] == player]
        return str(pl_val['ID']).split('*')[1]
    iplayer = player
    if ' ' in player:
        iplayer = player.replace(' ', '-').lower()
    pkey = get_key_from_xlsx()
    page_str = '/'.join([f"/player/{pkey}/{get_config('league')}",
                         f"{iplayer}/{get_config('extrastuff')}"])
    time.sleep(1)
    get_fpage(driver, page_str)
    time.sleep(1)
    tables = driver.find_elements(By.XPATH, '//table')
    htmlinf = tables[1].get_attribute('outerHTML')
    soup = BeautifulSoup(htmlinf,'html.parser')
    drows = soup.find_all('tr')[0:6]
    if len(drows) == 0:
        return {}
    rw_list = list(filter(get_drows, enumerate(drows)))
    rw_list = list(map(lambda a: a[1], rw_list))
    return list(map(gen_results, rw_list))

if __name__ == "__main__":
    tdriver = login_f()
    print(get_player_stats(tdriver, 'Kyle Tucker'))
    print(get_player_stats(tdriver, 'Shelby Miller'))
    print(get_player_stats(tdriver, 'Kevin Gausman'))
