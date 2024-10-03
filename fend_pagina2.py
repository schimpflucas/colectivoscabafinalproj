import backend
import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_pagina2():
    
    st.title("Estadisticas Colectivos AMBA")
    st.write("Top 10 Empresas, Destinos y Lineas con mas colectivos")

    time = backend.timestamp()

    st.write(f"Horario: {time}")

    indicadores = backend.indicadores()
    st.write(f"Total Colectivos: {indicadores[0]}")
    st.write(f"Empresas Distintas: {indicadores[1]}")
    st.write(f"Destinos Distintos: {indicadores[2]}")
    st.write(f"Lineas Distintas: {indicadores[3]}")
    
    # Carga de los dataframes
    df1 = backend.funcion_df_agency()

    df2 = backend.funcion_df_destino()

    df3 = backend.funcion_df_linea()

    # Colocar la primer tabla
    st.subheader('Empresas')
    st.dataframe(df1)

    # Colocar la segunda tabla
    st.subheader('Destinos')
    st.dataframe(df2)

    # Colocar la tercera tabla en la parte inferior
    st.subheader('Lineas')
    st.dataframe(df3)


    df4 = backend.funcion_df_treemap()

    # Generar el treemap
    fig = px.treemap(df4, 
                    path=['Empresa'],  # La jerarquía del treemap
                    values='Colectivos',  # El valor que determina el tamaño de las cajas
                    title='Treemap de Colectivos por Empresa',
                    hover_name='Empresa',
                    hover_data={
                                    'Colectivos': True,  # Mostrar 'Destino'
                                },)

    # Mostrar el treemap
    st.plotly_chart(fig)
