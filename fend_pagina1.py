import backend
import streamlit as st
from streamlit_chat import message
import plotly.express as px
import pandas as pd

def mostrar_pagina1():
    backend.descarga()
    st.title("Consultar Colectivos AMBA")
    st.write("Indica el número de colectivo o el número más la letra del ramal")

    if 'preguntas' not in st.session_state:
        st.session_state.preguntas = []
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = []

    def click():
        if st.session_state.user != '':
            pregunta = st.session_state.user
            respuesta = backend.consulta(pregunta)

            st.session_state.preguntas.append(pregunta)
            st.session_state.respuestas.append(respuesta)

            # Limpiar el input de usuario después de enviar la pregunta
            st.session_state.user = ''
            
            # Generar y mostrar el mapa
            if isinstance(respuesta, pd.DataFrame) and not respuesta.empty:
                # Renombrar columnas temporalmente para los tooltips
                respuesta = respuesta.rename(columns={
                    'route_short_name': 'Ramal',
                    'trip_headsign': 'Destino',
                    'time': 'Ultima actualización'
                })

                # Crear el scattermapbox
                fig = px.scatter_mapbox(respuesta,
                                        lat='latitude',
                                        lon='longitude',
                                        hover_name='Ramal',  # Usar el nuevo nombre
                                        hover_data={
                                            'Destino': True,  # Mostrar 'Destino'
                                            'Ultima actualización': True,  # Mostrar 'Ultima actualización'
                                            'latitude': False,  # Ocultar coordenadas en el tooltip
                                            'longitude': False
                                        },
                                        zoom=10,  # Nivel de zoom inicial
                                        height=600)

                # Personalizar el mapa
                fig.update_layout(mapbox_style="open-street-map")

                # Aumentar el tamaño de los marcadores
                fig.update_traces(marker=dict(size=12))  # Cambia el tamaño según sea necesario
                st.plotly_chart(fig)


    with st.form('my-form'):
        query = st.text_input('¿Qué colectivo quieres consultar?:', key='user', help='Pulsa Enviar para hacer la consulta')
        submit_button = st.form_submit_button('Enviar', on_click=click)

    # if st.session_state.preguntas:
    #     for i in range(len(st.session_state.respuestas)-1, -1, -1):
    #         message(st.session_state.respuestas[i], key=str(i))

    #     # Opción para continuar la conversación
    #     continuar_conversacion = st.checkbox('Quieres hacer otra consulta?')
    #     if not continuar_conversacion:
    #         st.session_state.preguntas = []
    #         st.session_state.respuestas = []
