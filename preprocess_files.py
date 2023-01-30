'''Filters vessels based on area.
   Then calculates vessel type ID based on
   marker thresholds. Input and output are .csv.'''

import os
import numpy as np
import pandas as pd

class FileExtError(Exception):
    '''Catches error for wrong file type.'''
    pass 

def extract_file_tup(file_path):
    '''Returns a tuple of the file name and extension.'''
    file_basename = os.path.basename(file_path)
    return os.path.splitext(file_basename)

def dir_input():
    '''Returns the path to a directory.'''
    print('Enter the directory path:')
    dir_path = input()
    return dir_path

def read_file(file_path):
    '''Reads a .csv file into a pandas dataframe and returns it.'''
    file_ext = extract_file_tup(file_path)[1]
    try:
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        else:
            raise FileExtError
    except FileNotFoundError:
        raise FileNotFoundError

def output_dataframe(file_path, df):
    '''Writes a pandas dataframe to a .csv file. New file name is
       original/input file name plus suffix _trimmed. Does not overwrite
       the original/input file.'''
    file_tup = extract_file_tup(file_path)
    file_ext = file_tup[1]
    outfile_path = file_tup[0] + '_trimmed' + file_ext
    if file_ext == '.csv':
        df.to_csv(outfile_path, header=True, index=False)
    else:
        raise FileExtError    

def do_trim(df):
    '''Removes items from the dataframe based on given criteria.
       Returns a copy of the original dataframe (with items removed).'''
    area_threshold = 600
    df_t = df.T
    for col in df_t.columns:
        vessel_area = df_t[col][0]
        print(vessel_area)
        if int(vessel_area) < area_threshold:
            print("pop " + str(col))
            df_t.pop(col)
            col = col-1
    return df_t

in_dir = dir_input()
for in_file in in_dir:
    df = read_file(in_file)
    df_t_trimmed = do_trim(df)
    df_trimmed = df_t_trimmed.T
    output_dataframe(in_file, df_trimmed)