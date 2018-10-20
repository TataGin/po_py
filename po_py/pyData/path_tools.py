import os
import pathlib


def create_path(root, file, suffix=None):
    """ Creates a full path from user input folder, file_name

        Potential improvements:
            - Add treatment if user does not enter raw string

        Keyword arguments:
        :root string
        :file string

        Positional arguments:
        :suffix string

    """

    path = pathlib.Path(root) / file

    if suffix:
        if not suffix.startswith('.'):
            suffix = '.'+suffix
        return path.with_suffix(suffix)
    else:
        return path
