#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions to add impact cratering to drainage (Earth + Mars)
@author: gaia
"""


# This one is taken from (river_profile_functions.py)
def clean_profiles(df, extra=None):
    """
    Parameters
    ----------
    df : dataframe
        Input dataframe from QGIS using "Get Hydrology" tool with river profiles
    res : float
        Resolution of dataset/topography (in meters or map units)
    extra: string
        Explainer string for additional rasters in river points
    Returns
    -------
    df : cleaner dataframe

    """
    # Delete these automatic ones
    del df['DIST']; del df['DIST_SURF']
    # Change automatic QGIS names:
    # Core QGIS columns
    df = df.rename(columns = {"LINE_ID":"River", "ID":"Point", "X":"X_m", 
                                  "Y":"Y_m", "Z":"Elevation_m", 
                                  "DISTANCE":"Length_m", "OUTPUT_1":"Direction", 
                                  "FLOW":"Area_m2", "BASIN":"Basin", 
                                  "OUTPUT":"Slope",  "ORDER":"Strahler"}) 
    # Additional extracted columns (extra rasters deom QGIS)
    if extra=="e_p_a_au": #four extra columns with erosion, precip, and age + error
        df = df.rename(columns = {"erosionpbt":"Erosion_m", "pupstream":"P_rate_mmyr", 
                                  "geoage":"Terrain_ka", "geoageunc":"Error_ka"})
        #Remove rivers where nans > 10% of river length
        df = df.dropna(subset = ["Terrain_ka"]) #Delete terrains we don't want (nans)
        df = df.dropna(subset = ["Basin"]) #Delete where Basin = nan
        df = df[df.Erosion_m != 0]# delete erosion = 0
    # Shift column 'Basin' to first position + make integer
    df.insert(0, 'Basin', df.pop('Basin'))
    df['Basin'] = df['Basin'].astype(int)
    
    #Remove rivers that are >10%comprised of nans

    # Sort (does it need this? Leave anyway)
    df = df.sort_values(['Basin','River','Length_m'],ascending=True) #sort by basin and flow length

    # THE most important step for this process!:
    # Delete duplicat pixels, don't need whole tributary, just any single pixel
    df = df.drop_duplicates(subset=['X_m', 'Y_m'], keep='first')
    
    #Delete what you don't need for now:
    df = df.drop(columns=['Length_m', 'Direction', 'Slope', 'Strahler', 'P_rate_mmyr', 'Terrain_ka', 'Error_ka'])

    return df

def split_rivers(df, basin_ids):
    """
    Parameters
    ----------
    df : dataframe of rivers
    basin_ids : list with basin IDs to split into
    
    Returns
    -------
    dataframe with new column that labels two types of rivers (valley and canyon)

    """

    df['Type'] = 1
    df['Type'][~df['Basin'].isin(basin_ids)] = 'valley' # valleys (smol)
    df['Type'][df['Basin'].isin(basin_ids)] = 'canyon' # canyons (big)
    
    return df
