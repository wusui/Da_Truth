# Copyright (C) 2024 Warren Usui, MIT License
"""
Scraper to collect player lists for all teams (one csv file per team)
"""
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from utilities import get_fpage, login_f, get_league, \
                      clean_fantrax, save_fantrax
from get_data import get_avail_players
from reorg_excel import reorg_excel

get_avail_players()
peeps = f'newui/fantasy/teamInfo.go?leagueId={get_league()}'
driver = login_f()
get_fpage(driver, peeps)
soup = bs(driver.page_source, 'html.parser')
stable = soup.find_all('table', class_='fantTable')
teams = stable[0].find_all('td', style=True)
tlist = list(map(lambda a: a.text, teams))
print(tlist)
time.sleep(5)
for plyr in tlist:
    clean_fantrax()
    driver.close()
    time.sleep(5)
    driver = login_f()
    driver.get(
        f"https://www.fantrax.com/fantasy/league/{get_league()}/team/owners")
    print(plyr)
    time.sleep(5)
    linkv = driver.find_element(By.PARTIAL_LINK_TEXT, plyr)
    linkv.click()
    time.sleep(5)
    btns = driver.find_elements(By.XPATH, "//button")
    fnd_dwnld = list(filter(lambda a: a[1].text == 'get_app', enumerate(btns)))
    btns[fnd_dwnld[0][0]].click()
    time.sleep(5)
    outcsv = plyr.replace(" ", "_")
    save_fantrax(f'{outcsv}.csv')
    time.sleep(5)
driver.quit()
reorg_excel()
