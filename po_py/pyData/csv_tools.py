import os
import glob
import pandas as pd


def concat_csv(input_path, output_path=None, input_file='*',
               output_file='Concat.csv', index_col=[0],
               join='outer', subfolders=False,
               fill_na=False, ffill=None):


    ''' Concatenates all csv files in a folder and optionnally its subfolders

        Positional arguments:
        :input_path str

        Keyword arguments:
        :output_file str
        :index_col list
        :output_path None
        :join str
        :subfolders boolean
        :fillna boolean
        :ffill=None

    '''


    #Adapt path to look in subfolders
    sub = _search_subfolders(subfolders)

    #Add csv extension to input
    input_file = _has_csv_extension(input_file)

    #Output path = input path if not precised by user
    output_path = _check_output_path(input_path, output_path)

    #Check if file with output name already exists
    if file_exists(output_file, input_path, sub):
        if not _yes_no('Output file already exists. Overwrite? [Y/N]')
            output_file = _increment_file_name(output_file)

    #List of all paths to matching files
    occurences = glob.glob(input_path+sub+input_file, recursive=True)

    print('{0} matching files found'.format(len(occurences)))

    #Concatenate files with pandas
    df = pd.concat([pd.read_csv(f, index_col=index_col)
                        for f in occurences], sort=False)

    #Write result to CSV
    df.to_csv(os.path.join(output_path, output_file))

    print('All files concatenated in {0}'/
            .format(os.path.join(output_path, output_file)))


def _yes_no(question):
    answer = input(question + "(y/n): ").lower().strip()
    print("")
    while not(answer == "y" or answer == "yes" or \
    answer == "n" or answer == "no"):
        print("Input yes or no")
        answer = input(question + "(y/n):").lower().strip()
        print("")
    if answer[0] == "y":
        return True
    else:
        return False


def _search_subfolders(subfolders):
    if subfolders:
        return '/**/'
    else:
        return '/'

def _has_csv_extension():
    if not input_file.endswith('.csv')
        return input_file+'.csv'


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
