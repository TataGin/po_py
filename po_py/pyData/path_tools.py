import os
import pathlib


def create_path(root, file, ext=None):
    """ Creates a full path from user input folder, file_name

        Potential improvements:
            - Add treatment if user does not enter raw string

        Keyword arguments:

    """

    path = pathlib.Path(root) / file

    if ext:
        if not ext.startswith('.'):
            ext = '.'+ext
        return path.with_suffix(ext)
    else:
        return path
