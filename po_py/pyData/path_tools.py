"""Tools for path-related operations."""

import re
import sys
import glob
import pathlib as pl
import input_tools as it


def create_path(folder, file, suffix=None):
    """Create pathlib Path from folder, file_name, and optionnal extension.

    Potential improvements:
    - Add treatment if user does not enter raw string

    Keyword arguments:
    :folder rstr
    :file str

    Positional arguments:
    :suffix str
    """
    path = pl.Path(folder) / file

    if suffix:
        # Add dot to extension if user did not do it,
        if not suffix.startswith('.'):
            suffix = '.'+suffix
        return path.with_suffix(suffix)
    else:
        return path


def prompt_if_exists(path):
    """Ask user for action of output file name already exists.

    Positional arguments:
    :path rstr or Path
    """
    # If user enters raw string, create the Path object
    path = _if_string(path)
    # If the file already exists, ask user for action
    if path.is_file():
        print('')
        choice = it.custom_question('File already exists. ' +
                                    'What should we do',
                                    {'Cancel': 'c',
                                     'Owerwrite': 'o',
                                     'Increment': 'i'})
        if choice in ['Increment', 'i']:
            return uniquify(path)
        # elif choice in ('change', 'c'):
        #    new_name = input('What new name?')
        if choice in ['Owerwrite', 'o']:
            return path
        else:
            sys.exit('Execution cancelled by YOU!!!')
    else:
        return path


def uniquify(path, sep='_'):
    """Increment file name if exists.

    Positional arguments:
    :path raw str or Path
    """
    path = _if_string(path)
    folder = path.parent
    name = path.stem
    suffix = ''.join(path.suffixes)
    s = re.search(re.escape(sep) + '[0-9]+$', name)
    if s:
        s = s.start() + 1
        return create_path(folder, name[:s] +
                           str(int(name[s:]) + 1).zfill(len(name)-s),
                           suffix)
    else:
        return create_path(folder, name + sep + '01', suffix)


def search(path, sub=False):
    """Get occurences of a file name within a directory and sub-directories.

    Positional arguments:
    :path str or path

    Keyword arguments:
    :sub boolean
    """
    path = _if_string(path)
    path = _search_subfolders(path, sub)
    return glob.glob(str(path), recursive=True)


def _search_subfolders(path, subfolders):
    if subfolders:
        folder = path.parent
        name = path.name
        return folder / '**' / name
    else:
        return path


def _if_string(path):
    """Transform string argument to Path object.

    Positinal arguments:
    :path str or Path
    """
    if type(path) == str:
        return pl.Path(path)
    else:
        return path
