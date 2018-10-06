import os
import glob
import pandas as pd


def concat_csv(search_folder, output_folder=None, search_file='*',
               output_file='Concat.csv', index_col=[0],
               join='outer', subfolders=False,
               fill_na=False, ffill=None):
    ''' Concatenates all csv files in a folder and optionnally its subfolders

        Positional arguments:
        :search_folder str

        Keyword arguments:
        :output_file str
        :index_col list
        :output_folder None
        :join str
        :subfolders boolean
        :fillna boolean
        :ffill=None

    '''

    # Add csv extension to input
    search_file = _add_extension(search_file, 'csv')
    output_file = _add_extension(output_file, 'csv')

    # Output path = input path if not precised by user
    output_folder = _if_none(output_folder, search_folder)

    # Adapt path to look in subfolders
    sub = _search_subfolders(subfolders)

    # Check if file with output name already exists
    _prompt_if_exists(output_file)
    if file_exists(os.path.join(output_folder, output_file)):
        output_file = _prompt_replace(output_file)

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


def _add_extension(file, ext):
    ''' !!! See how to accept file both as a list or a string '''

    ext = _format_ext(ext)

    if _has_extension(file, ext):
        return file
    else:
        return file+ext.lower()


def _format_ext(ext):

    # Treat for user input '.fileext'
    if not ext.startswith('.'):
        return '.'+ext.lower()
    else:
        return ext.lower()


def _has_extension(file_path, ext):
    ''' Check if a file has a specific extension
        Could be more elegant

        !!! See how to accept file both as a list or a string

    '''

    ext = _format_ext(ext)

    # Check if file name finishes by extension
    if os.path.splitext(file_path) == ext:
        return True
    else:
        return False


def _if_none(x, y):

    if x:
        return x
    else:
        return y


def _search_subfolders(subfolders):
    ''' Returns substring for searching in subfolders

        Positional arguments:
        : subfolders boolean

    '''

    if subfolders:
        return '/**/'
    else:
        return '/'


def _prompt_replace(file_path):
    pass


def file_exists(path):
    """ Checks if the files already exists in the folder.

        Positional arguments:
        :path str

    """

    if file_exists(file_path):
        return os.path.isfile(file_path)


def _yes_no(question):
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or
              answer == "n" or answer == "no"):
        print("Input yes or no")
        answer = input(question + "(y/n):").lower().strip()
        print("")
    if answer[0] == "y":
        return True
    else:
        return False


def _increment_file_name(file_path):
    pass


def _fill_na(df, fill_na, ffill):

    if fill_na or ffill:
        df = df.fillna(value=fill_na, method=ffill)


def excel_to_csv(input_path, output_folder=None, skiprows=None):
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
