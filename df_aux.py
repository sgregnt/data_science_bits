import pandas as pd
import numpy as np
from dateutil import parser
import os

# Code snippets to:
# - run a GroupBy wrapper (see page 162 in Python Data Science Handbook.)
# - run an apply wrapper on data frame column, with converting a date (e.g., 2015-01-01) into ordinary data.
# - use index object of data frame to get data frame length (see page 99 in Python Data Science Handbook.)
# - save and load "formula" (treated as numpy object) following adopted name convention

def df_unique_unit(df, func):

    df = df.groupby('id_listing_anon').aggregate(func)

    return df

def df_unique_date(df, func):
    
    start = parser.parse('2015-01-01').toordinal()
    df['ds_night'] = df.ds_night.apply(lambda x: (parser.parse(x).toordinal() - start) % 365)
    df = df.groupby('ds_night').aggregate(func)  

    return df

def df_group_accupancy_by_column(df, col, func):

    df = df.groupby(col).aggregate(func)  
    n = len(df.index)
    
    return df.index, df['dim_is_requested']

def save_formula(formula, name='all_cities', size='full', suffix='raw'):    
    
    root = '/home/'
    data = 'data'
               
    np.save(os.path.join(os.path.join(root, data),  'formula_%s_%s_%s' % (name, size, suffix)), formula)

def load_formula(name='all_cities', size='full', suffix='raw'):    
    
    root = '/home/'
    data = 'data'
               
    formula = np.load(os.path.join(os.path.join(root, data),  'formula_%s_%s_%s.npy' % (name, size, suffix)))
    return str(formula)
