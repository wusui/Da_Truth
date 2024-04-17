# Copyright (C) 2024 Warren Usui, MIT License
"""
Scraper to collect available players
"""
import time
from selenium.webdriver.common.by import By
from utilities import get_fpage, login_f, get_config, \
                      clean_fantrax, save_fantrax

def get_avail_players():
    """
    Extract available player information and save to a csv file
    """
    clean_fantrax()
    driver = login_f()
    page_str = f"fantasy/league/{get_config('league')}/players;" + \
                "pageNumber=1;maxResultsPerPage=500"
    get_fpage(driver, page_str)
    btns = driver.find_elements(By.XPATH, "//button")
    fnd_dwnld = list(filter(lambda a: a[1].text == 'get_app', enumerate(btns)))
    btns[fnd_dwnld[0][0]].click()
    time.sleep(2)
    save_fantrax('available_players.csv')
    driver.quit()

if __name__ == "__main__":
    get_avail_players()
