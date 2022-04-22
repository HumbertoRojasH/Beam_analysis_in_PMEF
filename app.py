import streamlit as st
import streamlit.components.v1 as components
from functions import *

st.title("Análisis de Vigas Alveolares con la librería de PMEF")
st.markdown("#### Dimensionamiento de la Sección (m)")

col1, col2 = st.columns(2)
with col1:
    st.image("img/Perfil.jpg",width=320)
with col2:
    W = st.text_input("Ancho de la sección (b)","0.6")
    H = st.text_input("Altura de la sección (h)","1")
    t = st.text_input("Espesor del ala (e)","0.05")
    ta = st.text_input("Espesor del alma (a)","0.05")

st.markdown("#### Dimensionamiento Longitudinal de la Viga (m)")
type = st.selectbox("Seleccione la tipología de viga",["Castellated Beam","Cellular Beam"])

col1, col2 = st.columns(2)

with col2:
    L = st.text_input("Longitud de la viga (L)","10")
    n = st.text_input("Número de agujeros (n)","8")
    d = st.text_input("Radio del agujero (d)","0.7")

if type == "Castellated Beam":
    col1.image("img/Castellated.jpg",width=250)
if type == "Cellular Beam":
    col1.image("img/Cellular.png",width=250)

Generate_Model(W,H,t,ta,L,n,d,type)

st.markdown("#### Refinamiento de la Viga (m)")
col1, col2 = st.columns([1,4])
with col1:
    Min_size = st.text_input("Tamaño mínimo de la malla","0.3")
    Max_size = st.text_input("Tamaño máximo de la malla","0.4")

Generate_geo_file(t,ta,type,n,Min_size,Max_size)

import subprocess
import sys
subprocess.run([f"{sys.executable}", "mesh.py"])

with col2:
    p = open("object.html")
    components.html(p.read(), height=400)

st.markdown("#### Análisis con PMEF (kg,m,s)")
col1, col2 = st.columns(2)

Elas = col1.text_input("Módulo de elasticidad","2.1e10")
v = col1.text_input("Coeficiente de Poisson","0.2")
de = col1.text_input("Densidad","7850")
F = col2.text_input("Fuerza distribuida uniformemente en la cara superior del ala","-1e5")
fix = col2.selectbox("Tipo de empotramiento de la viga",["Start","End - Start"])
FS = col2.text_input("Factor de escala de lo dezplamientos","15")

Analysis_FEM(W,H,L,Elas,v,de,F,fix, FS)

st.components.v1.html('''
<!doctype html>
<html>
  <head>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width,height=device-height,initial-scale=1,maximum-scale=1,minimum-scale=1,user-scalable=no">
    <script src="https://unpkg.com/@babel/polyfill@7.0.0/dist/polyfill.js"></script>
  </head>
  <body>
    <div class="content"></div>
    <input type="button" value="Actualizar" onclick="location.reload()" 
style="font-family:Arial;font-size:8pt;width:150px;height:30px;
background:#777777;color:#fff444;cursor:pointer;position: absolute;bottom: 0%;"/>
    <script defer="defer" src="https://kitware.github.io/vtk-js/examples/GeometryViewer/GeometryViewer.js"></script>
  </body>
  </html>
    
    
''',height=600)

