# -*- coding: utf-8 -*-
"""role specific logic

"""
from util import db_select, db_session_lrs


def load_role():
    _sql = 'select * from role_def'
    _df = db_select(db_session_lrs, _sql)
    return _df
