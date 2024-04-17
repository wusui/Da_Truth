# Copyright (C) 2024 Warren Usui, MIT License
"""
Generate html page showing my team's results from yesterday
"""
from itertools import chain
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from selenium import webdriver
from utilities import login_f, get_config
from get_player_stats import get_player_stats

def get_my_team():
    """
    Extract stats from players on my team
    """
    def gmt_inner(driver):
        def gplayer_stats(player):
            return get_player_stats(driver, player)
        def gdata(sheet_text):
            myteam = get_config('myteam').replace(' ', '_')
            dfbp = pd.read_excel(f'{myteam}.xlsx',
                            sheet_name=sheet_text)['Player'].tolist()
            bpdata = list(map(gplayer_stats, dfbp))
            return list(chain.from_iterable(bpdata))
        return [gdata('Batting'), gdata('Pitching')]
    return gmt_inner(login_f())

def gen_yesterday_html():
    """
    Construct html file
    """
    outdata = get_my_team()
    batdata = pd.DataFrame(outdata[0]).to_html(index=False)
    pitdata = pd.DataFrame(outdata[1]).to_html(index=False)
    environment = Environment(loader=FileSystemLoader("templates\\"))
    template = environment.get_template("dayscores.txt")
    content = template.render(
        batdata=batdata, pitdata=pitdata, jtitle=get_config('myteam')
    )
    with open('yesterday_my_team.html', mode="w",
                        encoding="utf-8") as message:
        message.write(content)
    driver = webdriver.Chrome()
    driver.get(f"file:///{get_config('mydir')}/yesterday_my_team.html")
    input()

if __name__ == "__main__":
    gen_yesterday_html()
