"""Tools for managing files and data."""

import pathlib as pl
import pandas as pd
import path_tools as pt
import input_tools as it


def concat_csv(work_folder=None, output_folder=None, search_file='*.csv',
               output_file='Concat.csv', index_col=[0],
               join='outer', subfolders=False,
               fill_na=False, ffill=None):
    """Concatenates all csv files in a folder and optionnally its subfolders.

    Positional arguments:
    :work_folder str

    Keyword arguments:
    :work_folder str
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
    # Manage user inputs for paths
    input_path, output_path = _prepare_paths(work_folder, output_folder)

    # List of all paths to matching files
    occurences = pt.search(input_path, subfolders)

    # Print the number of files found
    print('{0} matching files found'.format(len(occurences) + 1))

    # Function to treat changing columns names

    # Concatenate files with pandas
    for i, f in enumerate(occurences):
        print('File # {} is being concatenated'.format(i))
        df = pd.concat(pd.read_csv(f, index_col=index_col), sort=False)

        df = pd.concat([pd.read_csv(f, index_col=index_col).rename(
            str.lower, axis='columns').rename(
            str.strip, axis='columns')

            for f in glob.glob(input_path+'/**/*.csv',
                               recursive=True)], sort=False)

    # Write result to CSV
    df.to_csv(output_path)

    # Print completion confirmation
    print('All files concatenated in {0}. Good job!'.format(output_path))


def _prepare_paths(work_folder, output_folder):

    # If no search folder given, looks in current working directory
    work_folder = it.if_none(work_folder, pl.Path.cwd())

    # Output path = input path if not precised by user
    output_folder = it.if_none(output_folder, work_folder)

    # Add csv extension to input
    input_path = pt.create_path(work_folder, search_file, 'csv')
    output_path = pt.create_path(work_folder, search_file, 'csv')

    # Check if file with output name already exists
    output_path = pt.prompt_if_exists(output_path)

    return input_path, output_path


def _fill_na(df, fill_na, ffill):

    if fill_na or ffill:
        df = df.fillna(value=fill_na, method=ffill)


def concat_csv(files, low_strip=False, replace_cols=None):
    """Concatenate a bunch of files.

    Positional arguments:
    :files list

    Keyword arguments:
    :low_strip boolean
    :replace_cols dict
    """
    if replace_cols:
        # Function to replace columns
        pass
    elif low_strip:
        return _concat_csv_lower_strip()

    return _concat()


def _concat_csv_lower_strip(files):
    """Concatenate files, df columns lowered and stripped

    """
    df = pd.concat([pd.read_csv(f, index_col=index_col).rename(
        str.lower, axis='columns').rename(
        str.strip, axis='columns')



def excel_to_csv(input_path, output_folder=None, skiprows=None):
    """Save a .csv copy of all Excel file (.xls or .xlsx) in a folder.

    If no output path is given, saves the stacked file in the same
    folder as the input files.

    Postitional arguments:
    :input_path str

    Keyword arguments:
    :output_path - str
    :skiprows = list
    """
    if not output_path:
        output_path=input_path

    for file_name in os.listdir(input_path):

        file_name=os.fsdecode(file_name)
        if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
            data=pd.read_excel(input_path+file_name, skiprows=skiprows)
            file_name=file_name.split('.')[0]+'.csv'
            data.to_csv(output_path+file_name)
