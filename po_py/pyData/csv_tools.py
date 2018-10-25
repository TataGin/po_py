"""Tools for managing files and data."""

import glob
import pandas as pd
import path_tools as pt
import input_tools as it
import pathlib as pl


def concat_csv(search_folder=None, output_folder=None, search_file='*.csv',
               output_file='Concat.csv', index_col=[0],
               join='outer', subfolders=False,
               fill_na=False, ffill=None):
    """Concatenates all csv files in a folder and optionnally its subfolders.

    Positional arguments:
    :search_folder str

    Keyword arguments:
    :search_folder str
    :output_folder str
    :search_file
    :output_file str
    :index_col list
    :output_folder str
    :join str
    :subfolders boolean
    :fillna boolean
    :ffill string
    """

    # If no search folder given, looks in current working directory
    if not search_folder:
        search_folder = pl.Path.cwd()

    # Output path = input path if not precised by user
    output_folder = it.if_none(output_folder, search_folder)

    # Add csv extension to input
    input_path = pt.create_path(search_folder, search_file, 'csv')
    output_path = pt.create_path(search_folder, search_file, 'csv')

    # Check if file with output name already exists
    pt.prompt_if_exists(output_file)

    # Adapt path to look in subfolders
    sub = _search_subfolders(subfolders)

    # List of all paths to matching files
    occurences = glob.glob(search_folder+sub+search_file, recursive=True)

    print('{0} matching files found'.format(len(occurences)+1))

    # Concatenate files with pandas
    for f in occurences:
        print('File # {} is being concatenated')
        df = pd.concat(pd.read_csv(f, index_col=index_col), sort=False)

    # Write result to CSV
    df.to_csv(os.path.join(output_folder, output_file))

    print('All files concatenated in {0}'
          .format(os.path.join(output_folder, output_file)))


def _fill_na(df, fill_na, ffill):

    if fill_na or ffill:
        df = df.fillna(value=fill_na, method=ffill)


def excel_to_csv(input_path, output_folder=None, skiprows=None):
    ''' Saves a .csv copy of all Excel file (.xls or .xlsx) in a folder.

    If no output path is given, saves the stacked file in the same
    folder as the input files.

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
