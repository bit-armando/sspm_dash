import pandas as pd
import os

def convinar_dataframes(ages):
    """
    Combines multiple CSV files into a single Pandas DataFrame.

    Args:
        ages (list): A list of integers representing the ages of the individuals whose data is being combined.

    Returns:
        pandas.DataFrame: A DataFrame containing the combined data from all CSV files.

    Raises:
        FileNotFoundError: If any of the CSV files specified in `ages` cannot be found in the `./data/` directory.

    """
    path = './data/'
    archivos = os.listdir(path)
    data_frames = [pd.read_csv(path + str(age) + '.csv', encoding='utf-8') for age in ages if str(age)+'.csv' in archivos]
    df = pd.concat(data_frames)
    df['id_fecha'] = pd.to_datetime(df['id_fecha'], format='%d/%m/%Y %H:%M:%S')
    df['anio'] = df['id_fecha'].dt.year
    df['mes'] = df['id_fecha'].dt.month
    return df
    

def remover_null_delitos(df):
    """Remueve los valores nulos de la columna delito

    Args:
        df (DataFrame): Dataframe a remover los valores nulos

    Returns:
        DataFrame: Dataframe con los valores nulos removidos
    """
    lista = list(df['id_Grupo'].unique())
    for i in lista:
        if i != str:
            lista.remove(i)
    return lista


def rellenar_meses_faltantes(df, ages):
    for age in ages:
        for mes in range(1, 13):
            try:
                df[(df['anio'] == age) & (df['mes'] == mes)].iloc[0]
            except:
                fila = pd.DataFrame({'anio': [age], 'mes': [mes], 'id_Grupo': None, 'count': [0]})
                df = pd.concat([df, fila], ignore_index=True)
    df = df.sort_values(by=['anio', 'mes'])
    return df


def remplazar_meses(df):
    meses = {
        1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL', 5: 'MAYO', 6: 'JUNIO', 
        7: 'JULIO', 8: 'AGOSTO', 9: 'SEPTIEMBRE', 10: 'OCTUBRE', 
        11: 'NOVIEMBRE', 12: 'DICIEMBRE'
        }
    df['mes'] = df['mes'].replace(meses)
    df['anio'] = df['anio'].astype(int)
    return df

def incidencia_delictiva(df, columnas=['mes','anio']):
    """Agrupa los datos por mes y año y remplaza el anio con una cadena de acuerdo al mes

    Args:
        df (DataFrame): Dataframe a agrupar
        columnas (list, optional): Columnas a agrupar. Defaults to ['mes','anio'].

    Returns:
        DataFrame: Dataframe agrupado
    """
    df = df.groupby(columnas).size().reset_index(name='count')
    return df


