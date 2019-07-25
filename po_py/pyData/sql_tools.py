"""Tools for database-related operation."""

from getpass import getpass
import sqlalchemy as sql


def connect(db_name=None, dialect='mssql', dbapi='pyodbc',
            driver='ODBC+Driver+13+for+SQL+Server',
            port='1433'):
    """Creates engine for interaction with the database.

    Keyword arguments:
    ------------------
    db_name : str
        The "nickname" of the database
    dialect : str
    dbapi : str
    driver : str
    port : str
    """
    db_name = db_name.strip().lower()
    
    if db_name == '' :
        host = ''
        db = ''

    username = input('Username: ')

    password = getpass(prompt='Password: ')

    return sql.create_engine(dialect+'+'+dbapi+'://'+username+':'+password+'@'
                             +host+':'+port+'/'+db+'?driver='+driver)