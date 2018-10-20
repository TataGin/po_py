import csv_tools as csv
import path_tools as pt
import os
import pathlib

path = r'C:\Users\F.Ginez\Google Drive'
file = 'b.csv'
ext = ''

path = pt.create_path(path, file, ext)

path.name
