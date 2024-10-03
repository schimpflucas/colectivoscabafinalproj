import requests
import pandas as pd
import datetime
import pandas as pd
import plotly.express as px
import streamlit as st

def descarga():

    # Acceder a los secretos
    client_id = st.secrets["client_id"]
    client_secret = st.secrets["client_secret"]
    
    # Construir la URL usando los secretos
    url = f"https://apitransporte.buenosaires.gob.ar/colectivos/vehiclePositionsSimple?client_id={client_id}&client_secret={client_secret}"
    
    # Realizar la solicitud GET
    response = requests.get(url)
    data_json = response.json()
    
    #creación dataframe
    
    df = pd.DataFrame(data_json)
    
    #eliminación duplicados
    
    df = df.drop_duplicates(subset='id')
    
    #eliminación nulos
    
    df = df.dropna()
    
    # Reemplazar 'Ã‘' por 'N' en toda la columna 'agency_name'
    df['agency_name'] = df['agency_name'].str.replace('Ã‘', 'N')
    
    #conversion speed de m/s a km/h
    
    df['speed'] = (df['speed']*(3.6))
    
    #Conversion timestamp a datetime
    
    df['time'] = pd.to_datetime(df['timestamp'], unit='s')
    # Restar 3 horas a cada valor en la columna 'time'
    df['time'] = df['time'] - pd.Timedelta(hours=3)
    
    #generacion primary key:
    
    df['id_timestamp'] = df['id'].astype(str) + '-' + df['timestamp'].astype(str)
    return(df)

df = descarga()

def timestamp():
    # Devolver solo el valor escalar de la Serie (primer valor)
    return df['time'].head(1).iloc[0]  # .iloc[0] devuelve solo el primer valor


def consulta(input_usuario):

    # Comprobar si la entrada del usuario tiene letras
    if any(char.isalpha() for char in input_usuario):
        # Si hay letras, buscamos esa combinación exacta
        regex_pattern = f'^{input_usuario}$'  # Empieza y termina con input_usuario
    else:
        # Si solo hay números, buscamos esos números seguidos de letras
        regex_pattern = f'^{input_usuario}(?![0-9])([A-Za-z]*)$'  # Solo seguido de letras

    # Filtrar el DataFrame
    df_filtered = df[df['route_short_name'].str.contains(regex_pattern, regex=True)]

    # Suponiendo que tu DataFrame se llama 'df_filtered'
    df_filtered['latitude'] = df_filtered['latitude'].astype(float)
    df_filtered['longitude'] = df_filtered['longitude'].astype(float)


    # Mostrar el gráfico
    resultado = df_filtered


    return resultado

def funcion_df_agency():
    # Obtener el conteo de los valores en la columna 'agency_name' y ordenarlos
    df_agency = df['agency_name'].value_counts().sort_values(ascending=False)

    # Convertir la serie en un DataFrame
    df_agency = df_agency.reset_index()

    # Renombrar las columnas
    df_agency.columns = ['Empresa', 'Colectivos']

    # Seleccion top 10
    df_agency_10 = df_agency.head(10)

    return(df_agency_10)

def funcion_df_destino():
    # Obtener el conteo de los valores en la columna 'agency_name' y ordenarlos
    df_destino = df['trip_headsign'].value_counts().sort_values(ascending=False)

    # Convertir la serie en un DataFrame
    df_destino = df_destino.reset_index()

    # Renombrar las columnas
    df_destino.columns = ['Destino', 'Colectivos']

    # Seleccion top 10
    df_destino_10 = df_destino.head(10)

    return(df_destino_10)

def funcion_df_linea():
    # Obtener el conteo de los valores en la columna 'agency_name' y ordenarlos
    df_linea = df['route_short_name'].value_counts().sort_values(ascending=False)

    # Convertir la serie en un DataFrame
    df_linea = df_linea.reset_index()

    # Renombrar las columnas
    df_linea.columns = ['Linea', 'Colectivos']

    # Seleccion top 10
    df_linea_10 = df_linea.head(10)

    return(df_linea_10)

def funcion_df_treemap():
    # Obtener el conteo de los valores en la columna 'agency_name' y ordenarlos
    df_agency = df['agency_name'].value_counts().sort_values(ascending=False)

    # Convertir la serie en un DataFrame
    df_agency = df_agency.reset_index()

    # Renombrar las columnas
    df_agency.columns = ['Empresa', 'Colectivos']

    return(df_agency)


