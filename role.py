# -*- coding: utf-8 -*-
"""role specific logic

"""
from util import db_select, db_session_lrs, STATIC_PATH, db_insert_df
import pandas as pd


def get_role_def():
    _sql = 'select * from role_def'
    _df = db_select(db_session_lrs, _sql)
    return _df


def get_role_default(config_type, n_player):
    """

    :param config_type:
    :param n_player:
    :return:
    usage:
        >>> config_type = 'standard1'
        >>> n_player = 9
        >>> get_role_default(config_type, n_player)
    """
    _sql = 'select * from default_role where config_type = \'{}\' and n_player = {}'.format(config_type, n_player)
    _result = db_select(db_session_lrs, _sql)
    return _result


def get_role_default_dict(config_type, n_player):
    _default_df = get_role_default(config_type, n_player)
    _result_dict = dict(zip(_default_df['role'], _default_df['n_player_in_role']))
    return _result_dict


@DeprecationWarning
def save_default_config():
    _df = pd.read_csv('{}{}'.format(STATIC_PATH, 'default_role.csv'))
    db_insert_df(db_session_lrs, 'default_role', _df)
