# Copyright (C) 2024 Warren Usui, MIT License
"""
Run everything
"""
from get_avail_players import get_avail_players
from get_teams import get_teams
from reorg_excel import reorg_excel
from gen_yesterday_html import gen_yesterday_html

get_avail_players()
get_teams()
reorg_excel()
gen_yesterday_html()
