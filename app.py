# Importar librerías
import pandas as pd
import plotly.express as px
from shiny.express import input, render, ui
from shinywidgets import render_plotly, render_widget
import re
import matplotlib.pyplot as plt
import seaborn as sns
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
import base64
from sklearn.preprocessing import MinMaxScaler, LabelEncoder


#tips = px.data.tips()

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSaGCj_jLRHniAxOGU18VGKKRQdWuy8TVjjif7t3rW51g9A3usvKRHAwQunoyWoXkX89LVFig83zzs7/pub?output=csv")

# Convertir la columna 'Disponibilidad' a tipo string
df['Disponibilidad'] = df['Disponibilidad'].astype(str)
# Limpiar la columna de disponibilidad eliminando cualquier variación de "disponible"
df['Disponibilidad'] = df['Disponibilidad'].str.replace(r'\bdisponible(s?)\b', '', regex=True).str.strip()
# Cambiar "agotado" por 0
df['Disponibilidad'] = df['Disponibilidad'].str.replace('Agotado', '0')
# Reemplazar cualquier valor no numérico con 0
df['Disponibilidad'] = pd.to_numeric(df['Disponibilidad'], errors='coerce')
# Convertir la columna de disponibilidad a entero
df['Disponibilidad'] = df['Disponibilidad'].fillna(0).astype(int)
# Crear un objeto MinMaxScaler
scaler = MinMaxScaler()
# Normalizar la columna 'Disponibilidad'
df['Disponibilidad_Normalizada'] = scaler.fit_transform(df[['Disponibilidad']])

# Limpiar la columna de precios y convertirla a numérica
df['Precio'] = df['Precio'].replace({'[$,]': ''}, regex=True)  # Eliminar símbolos como '$' o ',' si los hay
df['Precio'] = df['Precio'].apply(lambda x: re.sub(r'[^0-9.]', '', x))  # Mantener solo números y puntos
df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')  # Convertir a tipo numérico
df['Precio'] = df['Precio'].fillna(0).astype(int)  # Rellenar NaN con 0 y convertir a entero
# Crear un objeto MinMaxScaler
scaler_precio = MinMaxScaler()
# Normalizar la columna 'Precio'
df['Precio_Normalizado'] = scaler_precio.fit_transform(df[['Precio']])
le_nombre = LabelEncoder()
# Codificar la variable 'Categoría' utilizando valores desde 1 en adelante
df.loc[:, 'Nombre_Código'] = le_nombre.fit_transform(df['Nombre']) + 1

# Normalizar la columna 'Categoría_Código' utilizando MinMaxScaler desde 1 en adelante
scaler_Categoría_Código = MinMaxScaler()
df['Nombre_Normalizado'] = scaler_Categoría_Código.fit_transform(df[['Nombre_Código']])

# Obtener las variables dummy para la columna 'Categoría'
df_encoded = pd.get_dummies(df['Categoría'], prefix='Categoría')
# Concatenar las variables dummy al DataFrame original
df2 = pd.concat([df, df_encoded], axis=1)

categorias = df2['Categoría'].dropna().unique().tolist()

with ui.sidebar():
    ui.input_selectize("Categoría", "Select variable", choices=categorias)
    # Crear la interfaz de usuario (UI)
ui.nav_spacer()


with ui.nav_panel("Plot"):
    
    @render.data_frame
    def table4():
        #return df[[input.Categoría()]]
        filtro = df2[df2['Categoría'].str.contains(input.Categoría())]
        return filtro

    @render_plotly
    def plot():
        p = px.histogram(df2[df2['Categoría'].str.contains(input.Categoría())], x = 'Nombre')
        p.update_layout(height=225)
        return p
        
with ui.nav_panel("Table"):
    @render_plotly
    def plot2():
        p = px.histogram(df2, x = 'Categoría')
        p.update_layout(height=225)
        return p
    
    @render.data_frame
    def table2():
        #return df[[input.Categoría()]]
        return df2

