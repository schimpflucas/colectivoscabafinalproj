# app.py
import streamlit as st
from fend_pagina1 import mostrar_pagina1
from fend_pagina2 import mostrar_pagina2

@st.cache_data(ttl=300)

st.sidebar.title("Navegación")
pagina = st.sidebar.selectbox("Selecciona una página", ("Mapa de Consulta", "Estadisticas"))

if pagina == "Mapa de Consulta":
    mostrar_pagina1()
elif pagina == "Estadisticas":
    mostrar_pagina2()
