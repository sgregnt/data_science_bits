# -*- coding: utf-8 -*-

# Code snippets to:
# - read cvs file using pandas's read_csv method into a data frame
# - store a data frame as pickle file with ability to change naming convention.
# - split full data frame into subframes according to some fixed condition (e.g.,
#   split samples into cities according to geo locations)
# - store list of data frames into pickle files
# - store tiny sample of data frame to pickle file (to run experiments)

import pandas as pd
import os
import numpy as np 
     
def split_to_cities_filter_locations(df_full):
    
    locations = [(48.86,  2.35), (34.05, -118.24), (37.77, -122.43)]
    names = ['Paris', 'Los Angeles', 'San Francisco']
    
    r_square = 0.01
    
    dfs_full = []
    
    for geo, name in zip(locations, names):
        
        lat = geo[0]
        lng = geo[1]
        
        mask_geo = np.array(((df_full['dim_lat'] - lat)**2 + (df_full['dim_lng'] - lng) **2  < r_square))
        mask_name = np.array(df_full['dim_market'] == name)
        mask = np.logical_and(mask_geo, mask_name)
        dfs_full.append(df_full[mask])
    
    return dfs_full

def split_to_cities(df_full):
    
    names = ['Paris', 'Los Angeles', 'San Francisco']
    dfs_full = []
    
    for name in names:

        mask = np.array(df_full['dim_market'] == name)
        dfs_full.append(df_full[mask])
    
    return dfs_full

def store_df_full(df, name, suffix=''):    

    root = '/home/'
    data = 'data'                 
    
    df.to_pickle(os.path.join(os.path.join(root, data), 'df_%s_full_%s.pkl' % (name, suffix)))    
                  
def store_df_per_city_full(dfs_full, names, suffix=''):                   
    
    root = '/home/'
    data = 'data'  

    for df , name in zip(dfs_full, names):                   
        df.to_pickle(os.path.join(os.path.join(root, data), 'df_%s_full_%s.pkl' % (name, suffix)))                       
        
def store_df_per_city_tiny(dfs_full, names, suffix=''):    

    root = '/home/'
    data = 'data'  
               
    for df , name in zip(dfs_full, names):   
        df = df.sample(frac=0.1, replace=False, random_state=1)                
        df.to_pickle(os.path.join(os.path.join(root, data), 'df_%s_tiny_%s.pkl' % (name, suffix)))

if __name__ == '__main__' :    
        
    names = ['Paris', 'Los Angeles', 'San Francisco']
    
    df_all = pd.read_csv('/home/Downloads/data.tsv',  delimiter='\t',encoding='utf-8')
    store_df_full(df=df_all, name='all_cities', suffix='raw')
    
    dfs_full = split_to_cities_filter_locations(df_all)   
    store_df_per_city_full(dfs_full, names)

