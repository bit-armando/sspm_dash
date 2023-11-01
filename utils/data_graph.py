import pandas as pd
import geopandas as gpd
import os

def data_maps():
    df = gpd.read_file('./distritos.geojson')
    df = df.set_index('TEXT')
    return df

def get_sectores():
    geo_df = gpd.read_file('./sectores.geojson')
    return geo_df

def data_calles():
    return pd.read_csv('./data_group/locations.csv')

def get_geodataframes():
    distritos = data_maps()
    sectores = gpd.read_file('./sectores.geojson')
    calles = data_calles()
    return [distritos, sectores, calles]
