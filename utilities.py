# Copyright (C) 2024 Warren Usui, MIT License
"""
General routines
"""
import os
import time
import configparser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_fpage(driver, page):
    """
    Go to webpage specified by page parameter
    """
    driver.get(f"https://www.fantrax.com/{page}")
    WebDriverWait(driver,1000).until(EC.presence_of_all_elements_located(
                    (By.XPATH,"(//iframe)")))

def login_f():
    """
    Login to the fantrax website.  Return a selenium driver to be used by
    other calls
    """
    driver = webdriver.Chrome()
    get_fpage(driver, "login")
    slist = list(filter(lambda a: 'mat-input-' in a.get_attribute('id'),
                        driver.find_elements(By.XPATH, '//*[@id]')))
    confg = configparser.ConfigParser()
    confg.read('gnus.ini')
    slist[0].send_keys(confg['DEFAULT']['username'])
    slist[1].send_keys(confg['DEFAULT']['password'])
    blist = list(filter(lambda a: 'Login' in a.text,
                        driver.find_elements(By.XPATH, "//button")))
    blist[0].click()
    time.sleep(2)
    return driver

def get_config(param):
    """
    Return configuration parameter
    """
    confg = configparser.ConfigParser()
    confg.read('gnus.ini')
    return confg['DEFAULT'][param]

def get_fantrax():
    """
    Find all downloaded fantrax files
    """
    dloads = get_config('downloaddir')
    ffiles = os.listdir(dloads)
    fnames = list(filter(lambda a: a.find('Fantrax') >= 0, ffiles))
    if not fnames:
        return []
    return list(map(lambda a: '\\'.join([dloads, a]), fnames))

def clean_fantrax():
    """
    Clean download directory
    """
    filens = get_fantrax()
    list(map(os.remove, filens))

def save_fantrax(new_name):
    """
    Save downloaded fantrax file in local file (new_name).
    """
    filens = get_fantrax()
    os.replace(filens[0], new_name)
