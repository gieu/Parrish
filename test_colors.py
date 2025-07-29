"""
Script de prueba para verificar los colores personalizados de Parrish
Ejecute este archivo para probar los elementos de la interfaz con los nuevos colores
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# Configuración de colores y estilos (copia del app.py)
# --------------------------------------------------
def apply_custom_styles():
    """Aplica los colores de marca Parrish al tema de Streamlit"""
    st.markdown("""
    <style>
    /* Colores de marca Parrish */
    :root {
        --verde-parrish: #049735;
        --verde-oscuro: #00541f;
        --amarillo-parrish: #f7c500;
        --verde-claro: #6dab3c;
        --morado-parrish: #7f469c;
    }
    
    /* Sidebar personalizado */
    .css-1d391kg {
        background-color: var(--verde-oscuro) !important;
    }
    
    /* Títulos principales */
    h1 {
        color: var(--verde-parrish) !important;
        font-weight: bold !important;
    }
    
    h2 {
        color: var(--verde-oscuro) !important;
        font-weight: bold !important;
    }
    
    h3 {
        color: var(--verde-claro) !important;
    }
    
    /* Botones principales */
    .stButton > button {
        background-color: var(--verde-parrish) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background-color: var(--verde-oscuro) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(4, 151, 53, 0.3) !important;
    }
    
    /* Métricas */
    div[data-testid="metric-container"] {
        background-color: rgba(4, 151, 53, 0.05) !important;
        border: 1px solid var(--verde-claro) !important;
        padding: 15px !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(4, 151, 53, 0.1) !important;
    }
    
    div[data-testid="metric-container"] > div {
        color: var(--verde-oscuro) !important;
    }
    
    /* Mensajes de éxito */
    .stSuccess {
        background-color: rgba(109, 171, 60, 0.1) !important;
        border-left: 4px solid var(--verde-claro) !important;
        border-radius: 8px !important;
    }
    
    /* Mensajes de información */
    .stInfo {
        background-color: rgba(247, 197, 0, 0.1) !important;
        border-left: 4px solid var(--amarillo-parrish) !important;
        border-radius: 8px !important;
    }
    
    /* Mensajes de advertencia */
    .stWarning {
        background-color: rgba(127, 70, 156, 0.1) !important;
        border-left: 4px solid var(--morado-parrish) !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_parrish_colors():
    """Retorna los colores de marca Parrish para uso en gráficos"""
    return {
        'primary': '#049735',      # Verde Parrish
        'secondary': '#00541f',    # Verde oscuro
        'accent': '#f7c500',       # Amarillo Parrish
        'success': '#6dab3c',      # Verde claro
        'info': '#7f469c',         # Morado Parrish
        'palette': ['#049735', '#6dab3c', '#f7c500', '#7f469c', '#00541f']
    }

def configure_plotly_theme():
    """Configura el tema de plotly con los colores de marca"""
    colors = get_parrish_colors()
    
    # Configurar template personalizado
    import plotly.io as pio
    pio.templates["parrish"] = go.layout.Template(
        layout=go.Layout(
            colorway=colors['palette'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=colors['secondary'], size=12),
            title=dict(font=dict(color=colors['primary'], size=16, family="Arial Black")),
            xaxis=dict(
                gridcolor='rgba(109, 171, 60, 0.3)',
                linecolor=colors['success'],
                tickfont=dict(color=colors['secondary'])
            ),
            yaxis=dict(
                gridcolor='rgba(109, 171, 60, 0.3)',
                linecolor=colors['success'],
                tickfont=dict(color=colors['secondary'])
            )
        )
    )
    pio.templates.default = "parrish"

# --------------------------------------------------
# Configuración de la página
# --------------------------------------------------
st.set_page_config(
    page_title="Test de Colores Parrish",
    page_icon="🎨",
    layout="wide"
)

# Aplicar estilos
apply_custom_styles()
configure_plotly_theme()

# --------------------------------------------------
# Contenido de prueba
# --------------------------------------------------
st.title("🎨 Test de Colores Parrish")
st.markdown("Esta página muestra cómo se ven los diferentes elementos con los colores de marca.")

# Sidebar
st.sidebar.title("🧭 Navegación")
st.sidebar.radio("Seleccione:", ["Opción 1", "Opción 2"])
st.sidebar.info("Este es un mensaje de información en el sidebar")

# Headers
st.header("Este es un Header Principal")
st.subheader("Este es un Subheader")

# Mensajes
col1, col2, col3 = st.columns(3)
with col1:
    st.success("✅ Mensaje de éxito")
with col2:
    st.info("ℹ️ Mensaje de información")
with col3:
    st.warning("⚠️ Mensaje de advertencia")

# Métricas
st.subheader("📊 Métricas")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Estudiantes", "150", "5")
with col2:
    st.metric("Promedio", "85.5", "2.1")
with col3:
    st.metric("Éxito", "78%", "3%")
with col4:
    st.metric("Satisfacción", "92%", "-1%")

# Botones
st.subheader("🔘 Botones")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Botón Principal")
with col2:
    st.download_button("Descargar", "datos", "test.csv")
with col3:
    if st.button("Procesar"):
        st.balloons()

# Inputs
st.subheader("📝 Inputs")
col1, col2 = st.columns(2)
with col1:
    st.text_input("Nombre del estudiante")
    st.selectbox("Seleccione el grado", ["8°", "9°", "10°", "11°"])
with col2:
    st.number_input("Edad", min_value=10, max_value=20, value=15)
    st.radio("Género", ["Masculino", "Femenino"])

# Gráficos
st.subheader("📈 Gráficos con Colores Parrish")

# Datos de ejemplo
data = pd.DataFrame({
    'Materia': ['Matemáticas', 'Español', 'Ciencias', 'Inglés', 'Sociales'],
    'Promedio': [85, 78, 82, 88, 75],
    'Estudiantes': [120, 125, 118, 110, 130]
})

col1, col2 = st.columns(2)

with col1:
    # Gráfico de barras
    fig_bar = px.bar(data, x='Materia', y='Promedio', 
                     title="Promedio por Materia",
                     color='Promedio')
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    # Gráfico de líneas
    fig_line = px.line(data, x='Materia', y='Estudiantes',
                       title="Número de Estudiantes por Materia",
                       markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

# Dataframe
st.subheader("📋 Tabla de Datos")
st.dataframe(data, use_container_width=True)

# Paleta de colores
st.subheader("🎨 Paleta de Colores Parrish")
colors = get_parrish_colors()

color_cols = st.columns(5)
color_names = ['Verde Parrish', 'Verde Claro', 'Amarillo Parrish', 'Morado Parrish', 'Verde Oscuro']
color_values = colors['palette']

for i, (col, name, color) in enumerate(zip(color_cols, color_names, color_values)):
    with col:
        st.markdown(f"""
        <div style="
            background-color: {color};
            height: 80px;
            border-radius: 8px;
            margin: 5px 0;
            border: 2px solid #ddd;
        "></div>
        <p style="text-align: center; font-size: 12px; margin: 5px 0;">
            <strong>{name}</strong><br>
            {color}
        </p>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #00541f; padding: 20px;">
    <h4>✅ Test de Colores Completado</h4>
    <p>Todos los elementos están usando los colores de marca Parrish</p>
</div>
""", unsafe_allow_html=True)
