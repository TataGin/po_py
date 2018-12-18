"""Tools for database-related operation."""


def connect(id_, pwd, dsn='ResearchDB'):

    return sql.create_engine('mssql+pyodbc://'+id_+':'+pwd+'@'+dsn)


con = connect('florian.ginez', 'Pass')
