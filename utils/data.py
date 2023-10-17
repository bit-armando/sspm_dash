import pandas as pd
import os


def convinar_dataframes(path):
    archivos = os.listdir(path)
    data_frames = []
    for archivo in archivos:
        data_frames.append(pd.read_csv(path + archivo, encoding='utf-8'))
    return pd.concat(data_frames)

def add_mount(df):
    """Agrega las columnas de mes y año a un dataframe

    Args:
        df (DataFrame): Dataframe a agregar las columnas

    Returns:
        DataFrame: Dataframe con las columnas agregadas
    """
    df['id_fecha'] = pd.to_datetime(df['id_fecha'], format='%d/%m/%Y %H:%M:%S')
    df['mes'] = df['id_fecha'].dt.month
    df['anio'] = df['id_fecha'].dt.year
    return df

def incidencia_delictiva(df):
    """Agrupa los datos por mes y año y remplaza el anio con una cadena de acuerdo al mes

    Args:
        df (DataFrame): Dataframe a agrupar

    Returns:
        DataFrame: Dataframe agrupado
    """
    meses = {
        1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL', 5: 'MAYO', 6: 'JUNIO', 
        7: 'JULIO', 8: 'AGOSTO', 9: 'SEPTIEMBRE', 10: 'OCTUBRE', 
        11: 'NOVIEMBRE', 12: 'DICIEMBRE'
        }
    
    df_group = add_mount(df)
    df_group = df.groupby(['mes','anio']).size().reset_index(name='count')
    df_group['mes'] = df_group['mes'].replace(meses)
    return df_group