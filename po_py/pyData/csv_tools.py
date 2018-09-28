import os
import glob
import pandas as pd


def concat_csv(input_path, output_file='Concat.csv',
               index_col=[0], output_path=None, join='outer',
               sort=False, subfolders=False, fill_na=False,
               ffill=None):
    ''' Concatenates all csv files in a folder and optionnally its subfolders

        Positional arguments:
        :input_path str

        Keyword arguments:
        :output_file str
        :index_col list
        :output_path None
        :join str
        :sort boolean
        :subfolders boolean
        :fillna boolean
        ffill=None

    '''

    sub = _search_subfolders(subfolders)

    output_path = _check_output_path(input_path, output_path)
    output_path = os.path.join(output_path, output_file)

    if file_exists(output_file, input_path, sub):

        df = pd.concat([pd.read_csv(f, index_col=index_col)
                        for f in glob.glob(input_path+sub+'/*.csv',
                                           recursive=True)], sort=False)

        df.to_csv(output_path)


def _search_subfolders(subfolders):
    if subfolders:
        return '/**'
    else:
        return ''


def file_exists(output_file, directory, sub):
    if output_file in glob.glob(directory+sub+'/**/output_file',
                                recursive=True):
        return True
    else:
        return False


def _check_output_path(input_path, output_path):

    if not output_path:
        output_path = input_path


def _fill_na(df, fill_na, ffill):

    if fill_na or ffill:
        df = df.fillna(value=fill_na, method=ffill)


def excel_to_csv(input_path, output_path=None, skiprows=None):
    ''' Saves a .csv copy of all Excel file (.xls or .xlsx) in a folder
        If no output path is given, saves the stacked file in the same
        folder as the input files

        Postitional arguments:
        :input_path str

        Keyword arguments:
        :output_path - str
        :skiprows = list

    '''

    if not output_path:
        output_path = input_path

    for file_name in os.listdir(input_path):

        file_name = os.fsdecode(file_name)
        if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
            data = pd.read_excel(input_path+file_name, skiprows=skiprows)
            file_name = file_name.split('.')[0]+'.csv'
            data.to_csv(output_path+file_name)
