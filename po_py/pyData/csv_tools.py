import os
import pandas as p
import glob
import pandas as pd
from pathlib import Path


def stack_csv(input_path, output_file='Concat.csv',
              index_col=[0], output_path=None, join='outer', sort=False):
    ''' Concatenates all csv files in a folder and optionnally its subfolders

        Positional arguments:
        :input_path str

    '''

    if not output_path:
        output_path = input_path

    df = pd.concat([pd.read_csv(f, index_col=index_col)
                    for f in glob.glob(input_path+'/**/*.csv', recursive=True)],
                   sort=False)

    df.to_csv(os.path.join(output_path, output_file))


def excel_to_csv(input_path, output_path=None, skiprows=None):
    ''' Saves a .csv copy of all Excel file (.xls or .xlsx) in a folder
        If no output path is given, saves the stacked file in the same folder as the input files

        Postitional arguments:
        :input_path str

        Keyword arguments:
        :output_path - str
        :skiprows = list

    '''

    input_path = end_path(input_path)
    if not output_path:
        output_path = input_path

    directory = os.fsencode(input_path)

    for file_name in os.listdir(input_path):

        file_name = os.fsdecode(file_name)
        if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
            data = pd.read_excel(input_path+file_name, skiprows=skiprows)
            file_name = file_name.split('.')[0]+'.csv'
            data.to_csv(output_path+file_name)
