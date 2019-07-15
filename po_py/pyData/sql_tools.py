"""Tools for database-related operation."""

from getpass import getpass
import sqlalchemy as sql


def connect(db_name='D01', dialect='mssql', dbapi='pyodbc',
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

    if db_name == 'd01':
        host = '10.0.10.199'
        db = 'EUDevDB'

    elif db_name == 'p13':
        host = '10.0.10.197'
        db = 'FundamentalsDB'

    elif db_name == 'crypto':
        host = 'crypto-market-data-test.cwlmdysgd5t3.eu-west-1.rds.amazonaws.com'
        db = 'crypto_market_data'
        dialect = 'mysql'
        dbapi='pymysql'
        port='3306'
        driver = ''

    username = input('Username: ')

    password = getpass(prompt='Password: ')

    return sql.create_engine(dialect+'+'+dbapi+'://'+username+':'+password+'@'
                             +host+':'+port+'/'+db+'?driver='+driver)