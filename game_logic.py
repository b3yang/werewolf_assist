# -*- coding: utf-8 -*-
"""game specific logic

"""
import pandas as pd

from util import db_insert_df, db_session_lrs, db_select


def init_game_auto(n_player):
    pass


def get_game_def():
    _sql = 'select * from game_def where save_time = (select max(save_time) from game_def)'
    _df = db_select(db_session_lrs, _sql)
    return _df

def save_game_def(player_config):
    _df = pd.DataFrame({'n_player': [len(player_config)]})
    db_insert_df(db_session_lrs, 'game_def', _df)

def save_game_player_def(player_config):

    pass

def init_game(player_config, re_init=False):
    # write game into sqlite db
    if re_init:
        save_game_def(player_config)


