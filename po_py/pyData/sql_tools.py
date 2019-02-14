"""Tools for database-related operation."""

from getpass import getpass
import sqlalchemy as sql


def connect(db='D01', dialect='mssql', dbapi='pyodbc',
            driver='ODBC+Driver+13+for+SQL+Server',
            port='1433', dbname='EUDevDB'):

    if db == 'D01':
        hostname = '10.0.10.199'
    elif db == 'P13':
        hostname = '10.0.10.197'

    username = input('Username: ')

    password = getpass(prompt='Password: ')

    return sql.create_engine(dialect+'+'+dbapi+'://'+username+':'+password+'@'
                             + hostname+':'+port+'/'+dbname+'?driver='+driver)
