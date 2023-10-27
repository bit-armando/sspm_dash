import pandas as pd
import geopandas as gpd
import os


def data_maps():
    df = gpd.read_file('./distritos.geojson')
    df = df.set_index('TEXT')
    return df

def data_calles():
    return pd.read_csv('./data_group/locations.csv')
    