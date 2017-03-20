# -*- coding: utf-8 -*-
"""utility function

"""
import pandas as pd
import pandas.io.sql as pandas_sql
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sqlite3

STATIC_PATH = 'C:/Users/byang/Documents/bin/workspace/werewolf_assist/static/'
GAME_DB_PATH = 'C:/Users/byang/Documents/bin/workspace/werewolf_assist/games/game.db'


def gen_connection(file_path=None):
    """
    generate a connection object for different database types
    :param host: host of the db server
    :param user: username
    :param password: password
    :param db_name: database name
    :param db_type: only support mysql now
    :return: return connection object
    """
    if file_path is None:
        file_path = GAME_DB_PATH
    _conn = sqlite3.connect(file_path)
    return _conn


engine_ap = create_engine("{0}://".format('sqlite+pysqlite'), creator=gen_connection, pool_recycle=3600, pool_size=10)
db_session_lrs = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_ap))


def helper_fix_pandas_sql_str(sql_str):
    """
    # fix an issue withe query having % within
    # for instance query = '%%usd%%'
    :param sql_str:
    :return:
    usage:
        >>> sql_str = 'blah%%dfk%% somethingelse% again%something %blahblah'
        >>> helper_fix_pandas_sql_str(sql_str)
    """
    if '%' in sql_str:
        assert '|' not in sql_str, 'both % and | in query cannot handle'
        _temp_query = re.sub('%+', '|', sql_str)
        sql_str = _temp_query.replace('|', '%%')
    return sql_str


def db_select(db_session, sql_str, return_df=True, pd_native=True):
    """
    replace ExecuteQuery, ExecuteDFQuery in db.py
    :param db_session:
    :param pd_native: if set to true, it will use pandas read_sql function
    :param sql_str: sql string
    :param return_df: flag to return dataframe or not
    usage:
        >>> db_select(db_session_lrs, 'select * from role_def')

    """
    if pd_native:
        if '%' in sql_str:
            sql_str = helper_fix_pandas_sql_str(sql_str)
        _result = pandas_sql.read_sql(sql_str, con=db_session.bind)
    else:
        _result = db_session.execute(sql_str)
        if return_df:
            _result = pd.DataFrame(_result.fetchall(), columns=[x[0] for x in _result._cursor_description()])
        else:
            _result = _result.fetchall()
    db_session.remove()
    return _result

def db_insert_df(db_session, table_name, input_df, schema=None):
    """
    replace DataFrame2DB
    though this function no longer handles BBG2DBMapping,
    usage:
        >>> df = pd.read_csv(STATIC_PATH + 'role_def.csv')
        >>> db_insert_df(db_session_lrs, 'role_def', df)
    """
    if schema is None:
        input_df.to_sql(table_name, db_session.bind, if_exists='append', index=False)
    else:
        input_df.to_sql(table_name, db_session.bind, if_exists='append', index=False, schema=schema)
    db_session.commit()
    db_session.remove()