# -*- coding: utf-8 -*-
"""game specific logic

"""
import pandas as pd

from role import get_role_def, get_role_default_dict
from util import db_insert_df, db_session_lrs, db_select


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


def init_game_auto(config_type, n_player):
    """

    :param config_type:
    :param n_player:
    usage:
        >>> config_type = 'standard1'
        >>> n_player = 9
    """
    _role_dict = get_role_default_dict(config_type, n_player)

