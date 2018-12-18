import pandas as pd
from io import BytesIO

HOST = 'indices.markit.com'
USER_ID = 'WISDOM_TREE'
PWD = 'Fz5G95klKmDr'
CWD = '/IBOXX_CUSTOM_INDICES/b171101/components'
FILE_NAME = 'iboxx_b171101_eom_components_201806.csv'

ftp = FTP(HOST, user=USER_ID, passwd=PWD)


def ftp_download(ftp, file_name=None, source_cwd='/'):
    """ Downloads files from FTP server

    Positional arguments:
    :FTP class from ftplib librairy

    Keyword arguments:
    :file_name=None - str

    """

    # Ajouter si file_name=None tlecharger tous les fichiers du doss
    # Ajouter un chemin de destination optionel

    ftp.cwd(source_cwd)

    with open(file_name, 'wb') as localfile:
        ftp.retrbinary('RETR ' + file_name, localfile.write, 1024)


def ftp_to_df(ftp, file_name=None, cwd='/', sep=',', index_col=None):
    """ Downloads file from FTP server

    Positional arguments:
    :FTP class from ftplib librairy

    Keyword arguments:
    :file_name=None - str

    Returns:
    :DataFrame

    """

    ftp.cwd(cwd)

    r = BytesIO()

    ftp.retrbinary('RETR ' + file_name, r.write)

    r.seek(0)

    return pd.read_csv(r, sep, index_col=index_col)
