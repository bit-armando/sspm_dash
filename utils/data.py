import pandas as pd
import sqlite3
import geopandas as gpd
import random

def convertir_fecha(df):
    df['id_fecha'] = pd.to_datetime(df['id_fecha'], format='%Y-%m-%d')
    df['anio'] = df['id_fecha'].dt.year
    df['mes'] = df['id_fecha'].dt.month
    return df

def get_data_incidentes():
    connection = sqlite3.connect('Estadisticas.db')
    query = 'SELECT * FROM Incidentes'
    incidentes_df = pd.read_sql(query, connection)
    connection.close()
    
    incidentes_df = convertir_fecha(incidentes_df)
    return incidentes_df


def limpiar_data_incidentes(df):
    columnas_incidentes = ['id_Parte', 'id_DSem2', 'arcview', 'id_Hechos', 'negocio', 'id_Horario', 'folio_ceri', 'id_ident', 'id_DetNum', 'pesos', 'dolares', 'vehiculo', 'parte']
    df.drop(columns=columnas_incidentes, inplace=True)

    df['id_fecha'] = pd.to_datetime(df['id_fecha'], format='%d/%m/%Y %H:%M:%S', dayfirst=True)
    df['zp'] = df['zp'].astype(float)
    return df

def random_point(distrito, sector, colonia):
    if distrito:
        if sector:
            if colonia:
                calle_aleatoria = random.choice(colonia)
                centro_aletorio = calle_aleatoria.centroid
            else:
                calle_aleatoria = random.choice(sector)
                centro_aletorio = calle_aleatoria.centroid
        else:
            calle_aleatoria = random.choice(distrito)
            centro_aletorio = calle_aleatoria.centroid
    
    else:
        centro_aletorio = None
    
    return centro_aletorio

def get_points_from_incidentes(df):
    colonias = gpd.read_file('colonias.geojson')
    distritos = gpd.read_file('distritos.geojson')
    vialidades = gpd.read_file('vialidades.geojson')
    sectores = gpd.read_file('sectores.geojson')
    
    df_xy = pd.DataFrame(columns=['zp', 'descripcion', 'id_fecha', 'id_Grupo', 'id_Asunto', 'id_Hora', 'colonia', 'id_Lugar', 'calle2', 'x', 'y'])
    df_not_found = pd.DataFrame(columns=['zp', 'descripcion', 'id_fecha', 'id_Grupo', 'id_Asunto', 'id_Hora', 'colonia', 'id_Lugar', 'calle2'])
    
    for item in range(len(df)):
        serie = df.loc[item]
        
        mask = vialidades['NOMBRE'].isin([serie.iloc[7], serie.iloc[8]])
        calles = vialidades[mask]
        mask = sectores['Sector'].isin([serie.iloc[0]])
        poligon_sector = sectores[mask]
        poligon_colonia = colonias[colonias['NOMBRE'] == serie.iloc[6]].geometry
        poligon_distrito = distritos[distritos['TEXT'] == serie.iloc[1]].geometry


        data_sector = []
        data_colonia = []
        data_distrito = []
        
        for line in calles['geometry']:
            contains_distrito = poligon_distrito.contains(line)
            
            if contains_distrito.any():
                data_distrito.append(line)
                contains_sector = poligon_sector.contains(line)
                
                if contains_sector.any():
                    data_sector.append(line)
                    contains_colonia = poligon_colonia.contains(line)
                    if contains_colonia.any():
                        data_sector.append(line)
                        
                        contains_colonia = poligon_colonia.contains(line)
                        if contains_colonia.any():
                            data_colonia.append(line)
                
                else:
                    contains_colonia = poligon_colonia.contains(line)
                    if contains_colonia.any():
                        data_colonia.append(line)
        
        point = random_point(data_distrito, data_sector, data_colonia)
        
        try:
            random_x, random_y = point.xy
        except:
            pass
        
        fila = {}
        if point:
            fila['zp'] = serie.iloc[0]
            fila['descripcion'] = serie.iloc[1]
            fila['id_fecha'] = serie.iloc[2]
            fila['id_Grupo'] = serie.iloc[3]
            fila['id_Asunto'] = serie.iloc[4]
            fila['id_Hora'] = serie.iloc[5]
            fila['colonia'] = serie.iloc[6]
            fila['id_Lugar'] = serie.iloc[7]
            fila['calle2'] = serie.iloc[8]
            fila['x'] = random_x
            fila['y'] = random_y
            
            fila = pd.DataFrame(fila, index=[0])
            df_xy = pd.concat([df_xy, fila], ignore_index=True)
        
        else:
            fila['zp'] = serie.iloc[0]
            fila['descripcion'] = serie.iloc[1]
            fila['id_fecha'] = serie.iloc[2]
            fila['id_Grupo'] = serie.iloc[3]
            fila['id_Asunto'] = serie.iloc[4]
            fila['id_Hora'] = serie.iloc[5]
            fila['colonia'] = serie.iloc[6]
            fila['id_Lugar'] = serie.iloc[7]
            fila['calle2'] = serie.iloc[8]
            
            fila = pd.DataFrame(fila, index=[0])
            df_not_found = pd.concat([df_not_found, fila], ignore_index=True)
            
    delitos = ['PRIVACION DE LA LIBERTAD', 'DET. ORDEN PENDIENTE',
       'ROBO A NEGOCIO', 'ROBO A CASA HABITACION', 'ROBO OTROS',
       'LESIONES ARMA BLANCA', 'HOMICIDIO C OTROS OBJETOS',
       'LESIONES ARMA DE FUEGO', 'PORTAR OBJETOS PELIG.',
       'HOMICIDIO C ARMA BLANCA', 'ABUSO SEXUAL', 'ARMAS DECOMISADAS',
       'ABUSO CONFIANZA', 'INTENTO DE ROBO', 'HOMICIDIO C ARMA DE FUEGO',
       'LESIONES OTROS', 'ASALTO ARMA DE FUEGO', 'OSAMENTA',
       'ASALTO ARMA BLANCA', 'SECUESTRO', 'INTENTO DE ASALTO',
       'EXTORSION', 'ASALTO OTROS', 'CARTUCHOS DECOMISADOS',
       'TENTATIVA DE HOMICIDIO', 'VIOLACION', 'ASALTO A BANCO']

    colores_hex = [
        "#012443",  # Rojo
        "#B61919",  # Verde
        "#A278B5",  # Azul
        "#5F1854",  # Amarillo
        "#8B104E",  # Magenta
        "#00FFFF",  # Cian
        "#FFA500",  # Naranja
        "#800080",  # Púrpura
        "#008000",  # Verde lima
        "#800000",  # Marrón
        "#008080",  # Verde azulado
        "#000080",  # Azul marino
        "#FFC0CB",  # Rosa
        "#A0522D",  # Marrón claro
        "#00FF7F",  # Verde primavera
        "#F0E68C",  # Amarillo claro
        "#2E8B57",  # Verde mar
        "#87CEEB",  # Azul cielo
        "#FFD700",  # Oro
        "#ADFF2F",  # Verde amarillo
        "#8A2BE2",  # Azul violeta
        "#9932CC",  # Púrpura oscuro
        "#F5DEB3",  # Trigo
        "#32CD32",  # Verde lima brillante
        "#FFE4C4",  # Melocotón
        "#DA70D6",  # Lila
        "#40E0D0"   # Turquesa
    ]
    
    df_xy['color'] = None    
    delito_a_color = dict(zip(delitos, colores_hex))

    # Ahora puedes buscar el color correspondiente a cada delito
    for item in range(len(df_xy)):
        delito = df_xy.loc[item, 'id_Grupo']
        if delito in delito_a_color:
            df_xy.loc[item, 'color'] = delito_a_color[delito]
            
    df_xy.to_csv('data_group/locations.csv', index=False)
    df_not_found.to_csv('data_group/locations_not_founf.csv', index=False)
    

def remover_null_delitos(df):
    """Remueve los valores nulos de la columna delito

    Args:
        df (DataFrame): Dataframe a remover los valores nulos

    Returns:
        DataFrame: Dataframe con los valores nulos removidos
    """
    lista = list(df['id_Grupo'].unique())
    for i in lista:
        if i == None:
            print(type(i))
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


def agregar_divisiones(df, ages):
    diviciones = ['ORIENTE', 'PONIENTE', 'CENTRO', 'RIVERAS', 'VALLE', 'SUR',
       'UNIVERSIDAD', 'POLICIA COMERCIAL', 'UNEVID', 'GOE', 'CANINA',
       'COM. ESPECIALES', 'OPERATIVO BLOCK', 'INTELIGENCIA', 'ALCAIDIA']
    
    grupo_df = df.groupby(['anio', 'mes', 'descripcion']).size().reset_index(name='counts')
    
    for age in ages:
        a = grupo_df[grupo_df['anio'] == age]
        for i in diviciones:
            if i not in a['descripcion'].unique():
                data = pd.DataFrame({'anio': age, 'mes': 5, 'descripcion': i, 'counts': 0}, index=[0])
                grupo_df = pd.concat([grupo_df, data], ignore_index=True)
                
    return grupo_df.sort_values(by=['anio', 'descripcion'])