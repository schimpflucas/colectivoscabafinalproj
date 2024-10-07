import requests
import pandas as pd
import datetime
import pandas as pd
import plotly.express as px
import streamlit as st
import re

@st.cache_data(ttl=300)
def obtener_datos():
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

    return df



def timestamp():
    df = obtener_datos()
    # Devolver solo el valor escalar de la Serie (primer valor)
    return df['time'].head(1).iloc[0]  # .iloc[0] devuelve solo el primer valor

def indicadores():
    df = obtener_datos()
    total_colectivos = df['agency_name'].count()
    empresas_dist = df['agency_name'].nunique()
    destinos_dist = df['trip_headsign'].nunique()
    lineas_dist = df['route_short_name'].nunique()
    indicadores = [total_colectivos,empresas_dist, destinos_dist, lineas_dist]
    return(indicadores)

def consulta(input_usuario):
    df = obtener_datos()
    
    try:
        # Comprobar si la entrada del usuario tiene letras
        if any(char.isalpha() for char in input_usuario):
            # Si hay letras, buscamos esa combinación exacta
            regex_pattern = f'^{input_usuario}$'  # Empieza y termina con input_usuario
        else:
            # Si solo hay números, buscamos esos números seguidos de letras
            regex_pattern = f'^{input_usuario}(?![0-9])([A-Za-z]*)$'  # Solo seguido de letras

        # Filtrar el DataFrame

        df_filtered = df[df['route_short_name'].str.contains(regex_pattern, regex=True)]

        # Convertir columnas a float
        df_filtered['latitude'] = df_filtered['latitude'].astype(float)
        df_filtered['longitude'] = df_filtered['longitude'].astype(float)

        # Retornar el DataFrame filtrado
        resultado = df_filtered

    except re.error as e:
        # Si hay un error en la expresión regular, imprimir el error y retornar None o un DataFrame vacío
        print(f"Error en la expresión regular: {e}")
        return None  # O puedes devolver pd.DataFrame() para un DataFrame vacío

    except KeyError as e:
        # Si no existe alguna de las columnas esperadas, manejar el error
        print(f"Columna faltante en el DataFrame: {e}")
        return None  # O pd.DataFrame() si prefieres

    except ValueError as e:
        # Si ocurre algún problema con la conversión de tipos
        print(f"Error en la conversión de datos: {e}")
        return None

    return resultado

def funcion_df_agency():
    df = obtener_datos()
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
    df = obtener_datos()
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
    df = obtener_datos()
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
    df = obtener_datos()
    # Obtener el conteo de los valores en la columna 'agency_name' y ordenarlos
    df_agency = df['agency_name'].value_counts().sort_values(ascending=False)

    # Convertir la serie en un DataFrame
    df_agency = df_agency.reset_index()

    # Renombrar las columnas
    df_agency.columns = ['Empresa', 'Colectivos']

    return(df_agency)


