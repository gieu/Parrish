import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm
from io import BytesIO

# --------------------------------------------------
# Configuración de colores y estilos
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
        background-color: #f5f5f5 !important;
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
    
    /* Botones de descarga */
    .stDownloadButton > button {
        background-color: var(--amarillo-parrish) !important;
        color: var(--verde-oscuro) !important;
        border: 2px solid var(--verde-parrish) !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: var(--verde-claro) !important;
        color: white !important;
    }
    
    /* Radio buttons */
    .stRadio > div > label > div:first-child {
        background-color: var(--verde-parrish) !important;
    }
    
    /* Radio button selected state */
    .stRadio > div > label > div[data-baseweb="radio"] > div:first-child {
        border-color: var(--verde-parrish) !important;
    }
    
    .stRadio > div > label > div[aria-checked="true"] > div:first-child {
        background-color: var(--verde-parrish) !important;
        border-color: var(--verde-parrish) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label > span:first-child {
        border-color: var(--verde-parrish) !important;
    }
    
    .stCheckbox > label > span[aria-checked="true"]:first-child {
        background-color: var(--verde-parrish) !important;
        border-color: var(--verde-parrish) !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background-color: var(--verde-parrish) !important;
    }
    
    .stSlider > div > div > div > div > div {
        border-color: var(--verde-parrish) !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div > div > div {
        border-color: var(--verde-parrish) !important;
    }
    
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: var(--verde-parrish) !important;
        color: white !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div > div {
        border-color: var(--verde-parrish) !important;
    }
    
    /* Selectbox dropdown styling */
    .stSelectbox > div > div > div > div:hover {
        border-color: var(--verde-parrish) !important;
    }
    
    /* Selectbox selected option */
    div[data-baseweb="select"] > div {
        border-color: var(--verde-claro) !important;
    }
    
    /* Links */
    a {
        color: var(--verde-parrish) !important;
    }
    
    a:hover {
        color: var(--verde-oscuro) !important;
    }
    
    /* Spinner/Loading */
    .stSpinner > div {
        border-top-color: var(--verde-parrish) !important;
    }
    
    /* File uploader */
    .stFileUploader section button {
        background-color: var(--verde-parrish) !important;
        border-color: var(--verde-parrish) !important;
        color: white !important;
    }
    
    .stFileUploader section button:hover {
        background-color: var(--verde-oscuro) !important;
        border-color: var(--verde-oscuro) !important;
    }
    
    /* Tab styling */
    .stTabs > div > div > div > div {
        border-bottom-color: var(--verde-parrish) !important;
    }
    
    .stTabs > div > div > div > div > button[aria-selected="true"] {
        border-bottom-color: var(--verde-parrish) !important;
        color: var(--verde-parrish) !important;
    }
    
    /* Number input arrows */
    .stNumberInput > div > div > input::-webkit-outer-spin-button,
    .stNumberInput > div > div > input::-webkit-inner-spin-button {
        color: var(--verde-parrish) !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-color: var(--verde-claro) !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--verde-parrish) !important;
        box-shadow: 0 0 5px rgba(4, 151, 53, 0.3) !important;
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
    
    /* Tablas */
    .stDataFrame {
        border: 2px solid var(--verde-claro) !important;
        border-radius: 8px !important;
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
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(4, 151, 53, 0.1) !important;
        border-radius: 8px !important;
        border: 1px solid var(--verde-claro) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: var(--verde-parrish) !important;
    }
    
    # /* Formularios */
    # .stForm {
    #     border: 2px solid var(--verde-claro) !important;
    #     border-radius: 10px !important;
    #     padding: 20px !important;
    #     background-color: #F4F4F4 !important;
    # }
    
    /* Sidebar texto */
    .css-1d391kg .stMarkdown {
        color: #333333 !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: var(--verde-oscuro) !important;
    }
    
    /* Form submit button especial */
    .stForm .stButton > button {
        background: linear-gradient(135deg, var(--verde-parrish), var(--verde-claro)) !important;
        color: white !important;
        font-size: 16px !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(4, 151, 53, 0.3) !important;
    }
    
    .stForm .stButton > button:hover {
        background: linear-gradient(135deg, var(--verde-oscuro), var(--verde-parrish)) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 12px rgba(4, 151, 53, 0.4) !important;
    }
    
    /* Columnas con bordes */
    .element-container {
        border-radius: 8px !important;
    }
    
    /* Divider personalizado */
    hr {
        border-color: var(--verde-claro) !important;
        border-width: 2px !important;
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
    
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close() # Or writer.save() for older pandas versions
    processed_data = output.getvalue()
    return processed_data

def create_colored_header(text, color_key='primary', level=1):
    """Crea un header con colores personalizados"""
    colors = get_parrish_colors()
    color = colors.get(color_key, colors['primary'])
    
    if level == 1:
        return f'<h1 style="color: {color}; font-weight: bold; margin-bottom: 0;">{text}</h1>'
    elif level == 2:
        return f'<h2 style="color: {color}; font-weight: bold; margin-bottom: 0;">{text}</h2>'
    elif level == 3:
        return f'<h3 style="color: {color}; font-weight: bold; margin-bottom: 0;">{text}</h3>'
    else:
        return f'<h4 style="color: {color}; font-weight: bold; margin-bottom: 0;">{text}</h4>'

def create_success_box(text):
    """Crea una caja de éxito personalizada"""
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(109, 171, 60, 0.1), rgba(4, 151, 53, 0.05));
        border-left: 4px solid #6dab3c;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(109, 171, 60, 0.2);
    ">
        <p style="color: #00541f; margin: 0; font-weight: 500;">✅ {text}</p>
    </div>
    """

def create_info_box(text):
    """Crea una caja de información personalizada"""
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(247, 197, 0, 0.1), rgba(247, 197, 0, 0.05));
        border-left: 4px solid #f7c500;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(247, 197, 0, 0.2);
    ">
        <p style="color: #00541f; margin: 0; font-weight: 500;">ℹ️ {text}</p>
    </div>
    """

def convert_df_to_excel(df, sheet_name='Data'):
    """Convierte un DataFrame a formato Excel en bytes"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output.getvalue()

def convert_multiple_dfs_to_excel(dataframes_dict):
    """Convierte múltiples DataFrames a un archivo Excel con varias hojas"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in dataframes_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output.getvalue()

# 📂 Ruta del archivo de coeficientes
MODELOS_XLSX = Path(__file__).with_name("Coeficientes_modelos.xlsx")

# --------------------------------------------------
# Utilidades
# --------------------------------------------------
# @st.cache_data
def cargar_modelos(path: Path) -> dict[str, pd.Series]:
    """
    Devuelve un diccionario:
        clave   -> nombre de la hoja
        valor   -> Series con coeficientes (index = variable, value = coef)
    """
    try:
        xl = pd.ExcelFile(path)
        modelos: dict[str, pd.Series] = {}
        for sheet in xl.sheet_names:
            df = xl.parse(sheet)
            # Los coeficientes están en la fila 0
            coefs = df.iloc[0]
            # Convertir todos los valores a numéricos, forzando errores a NaN
            coefs = pd.to_numeric(coefs, errors='coerce').fillna(0.0)
            modelos[sheet] = coefs
        return modelos
    except Exception as e:
        st.error(f"Error al cargar modelos: {e}")
        return {}


def predecir_con_detalles(modelo: pd.Series, datos: dict[str, float], nombre_materia: str) -> tuple[float, list]:
    """
    Calcula Σ (coef_i * dato_i)  +  _cons y retorna detalles del cálculo
    """
    detalles = []
    suma = 0.0
    
    # Obtener la constante
    try:
        constante = float(modelo.get("_cons", 0.0))
        suma = constante
        detalles.append(f"Constante: {constante:.6f}")
    except (ValueError, TypeError):
        constante = 0.0
        suma = 0.0
        detalles.append("Constante: 0.0 (error al leer)")
    
    # Sumar cada término
    for var, coef in modelo.items():
        if var == "_cons":
            continue
        
        try:
            # Convertir coeficiente a float
            coef_num = float(coef)
            # Obtener valor de la variable y convertir a float
            var_val = float(datos.get(var, 0))
            contribucion = coef_num * var_val
            suma += contribucion
            # Probit: probability = Φ(suma), where Φ is the standard normal CDF
            probabilidad = norm.cdf(suma)

            
            if abs(contribucion) > 0.001:  # Solo mostrar contribuciones significativas
                detalles.append(f"{var}: {coef_num:.6f} × {var_val} = {contribucion:.6f}")
            
        except (ValueError, TypeError) as e:
            detalles.append(f"{var}: Error - {e}")
            continue
    
    return float(probabilidad), detalles

def predecir_probit(modelo: pd.Series, datos: dict[str, float]) -> float:
    """
    modelos Probit
    """
    suma = 0.0
    try:
        suma = float(modelo.get("_cons", 0.0))
    except (ValueError, TypeError):
        suma = 0.0

    for var, coef in modelo.items():
        if var == "_cons":
            continue
        try:
            coef_num = float(coef)
            var_val = float(datos.get(var, 0))
            suma += coef_num * var_val
        except (ValueError, TypeError):
            continue

    # Probit: probability = Φ(suma), where Φ is the standard normal CDF
    probabilidad = norm.cdf(suma)
    return float(probabilidad)


def predecir(modelo: pd.Series, datos: dict[str, float]) -> float:
    """
    Calcula Σ (coef_i * dato_i)  +  _cons
    Si falta alguna variable, asume 0.
    """
    suma = 0.0
    
    # Obtener la constante
    try:
        suma = float(modelo.get("_cons", 0.0))
    except (ValueError, TypeError):
        suma = 0.0
    
    # Sumar cada término
    for var, coef in modelo.items():
        if var == "_cons":
            continue
        
        try:
            # Convertir coeficiente a float
            coef_num = float(coef)
            # Obtener valor de la variable y convertir a float
            var_val = float(datos.get(var, 0))
            suma += coef_num * var_val
        except (ValueError, TypeError) as e:
            # Si hay error, asumir que el coeficiente es 0
            print(f"Warning: No se pudo convertir coeficiente para {var}: {coef} - Error: {e}")
            continue
    
    return float(suma)


# --------------------------------------------------
# Cargar todos los modelos al iniciar la app
# --------------------------------------------------
try:
    MODELOS = cargar_modelos(MODELOS_XLSX)
    if not MODELOS:
        st.error("❌ No se pudieron cargar los modelos. Verifique que el archivo 'Coeficientes_modelos.xlsx' existe.")
        st.stop()
except Exception as e:
    st.error(f"❌ Error al cargar modelos: {e}")
    st.stop()

# --------------------------------------------------
# Interfaz Principal
# --------------------------------------------------
st.set_page_config(
    page_title="Sistema de Predicción Colegio Parrish",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

# Aplicar estilos personalizados de marca Parrish
apply_custom_styles()

# Configurar tema de gráficos Plotly
configure_plotly_theme()

## Add a banner from utils/banner.png
st.image("utils/banner.png", use_container_width=True)
st.markdown("---")

# Crear sidebar para navegación
st.sidebar.title(":material/explore: Navegación")

pagina = st.sidebar.radio(
    "Seleccione una opción:",
    [":material/person_search: Estudiante Individual", ":material/article_person: Análisis Masivo"]
)

# st.sidebar.markdown("---")
st.sidebar.markdown(" ")
st.sidebar.markdown("""
<div style="background: rgba(4, 151, 53, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #049735;">
    <h3 style="color: #00541f; margin-top: 0;">Acerca del Sistema</h3>
    <ul style="color: #333333; margin-bottom: 0;">
        <li><strong>Página Individual</strong>: Analiza un estudiante específico</li>
        <li><strong>Análisis Masivo</strong>: Procesa múltiples estudiantes desde Excel</li>
    </ul>
</div>
""", unsafe_allow_html=True)

## set footer image
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
st.sidebar.markdown("---")
st.sidebar.image("utils/img-footer.png", use_container_width=True)
st.sidebar.markdown("""<div style="text-align: center; padding: 10px 0;">
    <p style="color: #00541f; font-size: 14px; margin: 0;">© 2025 Colegio Karl C. Parrish</p>
</div>""", unsafe_allow_html=True)

# --------------------------------------------------
# Página 1: Estudiante Individual
# --------------------------------------------------
if pagina == ":material/person_search: Estudiante Individual":

    st.title(" Análisis Individual de Estudiante :material/person_search:")
    st.markdown("Ingrese los datos de un estudiante para obtener predicciones personalizadas.")
    
    # ---------- Selector de grado ----------
    grado = st.radio(
        "Seleccione el grado en que se encuentra el estudiante",
        options=["9 o 10", "11"],
        horizontal=True,
    )

    # Asignar el módulo basado en la selección
    if grado == "9 o 10":
        modulo = 14
    else:  # "11"
        modulo = 24
    st.markdown("---")

    st.markdown(create_colored_header("Información del Estudiante", 'secondary', 2), unsafe_allow_html=True)

    # ---------- Formulario ----------
    with st.form("formulario_estudiante"):
        # Identificación
        st.subheader("Código del estudiante")
        id_estudiante = st.text_input(
            "Identificador del estudiante, se utiliza para guardar los resultados",
            value="",
            help="Ingrese el identificador único del estudiante",
        )

        # 📋 Información Demográfica
        st.subheader("Información Demográfica")
        col1, col2 = st.columns(2)
        with col1:
            estu_mujer = st.selectbox(
                "Género del estudiante",
                options=[0, 1],
                format_func=lambda x: "Mujer" if x == 1 else "Hombre",
                help="1 = Mujer, 0 = Hombre",
            )
        with col2:
            edad_grado = st.number_input(
                "Edad del estudiante a la fecha de grado",
                min_value=10,
                max_value=35,
                value=17,
                step=1,
                help="Edad estimada del estudiante al momento de grado",
            )

        # 🎓 Educación padres
        st.subheader(":material/School: Educación Máxima de los Padres/Madres")
        st.markdown('''Seleccione el *máximo nivel educativo alcanzado* entre los padres del estudiante.''')
        
        educ_max_total = st.radio(
            "¿Qué nivel educativo alcanzó el padre o la madre con mayor educación?",
            options=[
                "Hasta bachillerato/secundaria completa",
                "Técnica o tecnológica (incompleta o completa)",
                "Educación profesional incompleta",
                "Educación profesional completa",
                "Postgrado"
            ],
        )
        
        # Convertir la selección del radio button a variables binarias
        educ_max_padremadre1 = 1 if educ_max_total == "Hasta bachillerato/secundaria completa" else 0
        educ_max_padremadre2 = 1 if educ_max_total == "Técnica o tecnológica (incompleta o completa)" else 0
        educ_max_padremadre3 = 1 if educ_max_total == "Educación profesional incompleta" else 0
        educ_max_padremadre4 = 1 if educ_max_total == "Educación profesional completa" else 0
        educ_max_padremadre5 = 1 if educ_max_total == "Postgrado" else 0
        
    
        # ⚠️ Faltas
        st.subheader(":material/person_alert: Comportamiento")
        total_faltas_disc = st.number_input(
            "Número total de faltas disciplinarias del estudiante",
            min_value=0,
            max_value=100,
            value=0,
        )

        # 📚 Promedios 8°
        st.subheader(":material/rubric: Promedios de 8° Grado")
        st.markdown("*Promedio obtenido en 8° grado en cada área (escala 0-100)*")
        col1, col2 = st.columns(2)
        with col1:
            human_langs_08 = st.number_input(
                "Humanidades, lengua castellana e idiomas extranjeros",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
            )
            maths_08 = st.number_input(
                "Matemáticas",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
            )
        with col2:
            nat_sc_08 = st.number_input(
                "Ciencias naturales y educación ambiental",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
            )
            soc_sc_08 = st.number_input(
                "Ciencias sociales, historia, geografía, constitución política y democracia",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
            )
        
        if human_langs_08 == 0.0 or maths_08 == 0.0 or nat_sc_08 == 0.0 or soc_sc_08 == 0.0:
            st.warning('''Al menos uno de los promedios de 8° grado es 0.
                       Verifique que los datos son correctos.''')
        
        if modulo == 24:
            # 📊 NWEA
            st.subheader("📊 Pruebas NWEA MAP (Grados 9° y 10°)")
            st.markdown("*Percentiles obtenidos en las pruebas estandarizadas NWEA MAP*")
            col1, col2 = st.columns(2)
            with col1:
                nwea_math_perc = st.number_input(
                    "Percentil en Matemáticas NWEA MAP",
                    min_value=1.0,
                    max_value=99.0,
                    value=50.0,
                    step=0.1,
                )
            with col2:
                nwea_reading_perc = st.number_input(
                    "Percentil en Comprensión Lectora NWEA MAP",
                    min_value=1.0,
                    max_value=99.0,
                    value=50.0,
                    step=0.1,
                )
        else:
            # Para grados 8° y 9°, no se usa NWEA
            nwea_math_perc = 50.0
            nwea_reading_perc = 50.0

        st.markdown("---")

        
        submitted = st.form_submit_button("🚀 Procesar Datos", use_container_width=True)

    # ---------- Procesar ----------
    if submitted:
        if not id_estudiante.strip():
            st.error("⚠️ Por favor ingrese un identificador del estudiante")
            st.stop()

        # 1️⃣ Construir diccionario con todos los datos del formulario
        datos = {
            "id": id_estudiante,
            "estu_mujer": estu_mujer,
            "edad_grado": edad_grado,
            "educ_max_padremadre1": educ_max_padremadre1,
            "educ_max_padremadre2": educ_max_padremadre2,
            "educ_max_padremadre3": educ_max_padremadre3,
            "educ_max_padremadre4": educ_max_padremadre4,
            "educ_max_padremadre5": educ_max_padremadre5,
            "total_faltas_disc": total_faltas_disc,
            "human_langs_08": human_langs_08,
            "maths_08": maths_08,
            "nat_sc_08": nat_sc_08,
            "soc_sc_08": soc_sc_08,
            "nwea_math_perc": nwea_math_perc,
            "nwea_reading_perc": nwea_reading_perc,
        }

        # 2️⃣ Calcular predicciones para todas las materias
        materias = ["global", "lectura", "math", "cnat", "soc", "ingles",]
        resultados = {}
        detalles_calculo = {}
        errores = []
        
        nombres_materias = {
            "GLOBAL": "Global",
            "LECTURA": "Lectura",
            "MATH": "Matemáticas",
            "CNAT": "Ciencias Naturales",
            "SOC": "Ciencias Sociales",
            "INGLES": "Inglés",
        }
        
        for materia in materias:
            try:
                hoja = f"s11_{materia}_mod{modulo}"
                if hoja not in MODELOS:
                    errores.append(f"No se encontró el modelo para {materia} (hoja: {hoja})")
                    continue
                
                modelo = MODELOS[hoja]
                prediccion, detalles = predecir_con_detalles(modelo, datos, materia)
                resultados[materia.upper()] = prediccion
                detalles_calculo[materia.upper()] = detalles
                
            except Exception as e:
                errores.append(f"Error al predecir {materia}: {str(e)}")
        
        # Mostrar errores si los hay
        if errores:
            for error in errores:
                st.warning(f"⚠️ {error}")
        
        if not resultados:
            st.error("❌ No se pudieron calcular predicciones. Revise el archivo de coeficientes.")
            st.stop()

        # 3️⃣ Mostrar confirmación y resumen
        st.markdown(create_success_box("¡Datos capturados y procesados exitosamente!"), unsafe_allow_html=True)

        with st.expander("Resumen de Datos Ingresados"):

            df_resumen = (
                pd.DataFrame({"Variable": list(datos.keys()), "Valor": list(datos.values())})
                .set_index("Variable")
            )
            st.dataframe(df_resumen, use_container_width=True)
        
        # ---- Resumen de predicciones
        st.subheader(":material/dictionary: Predicción por Materia")
        
 
        
        for materia, valor in resultados.items():
            nombre_materia = nombres_materias.get(materia, materia)
            if valor > 0.7:
                interpretacion = "🟢 "
                emoji = "✅"
            elif valor > 0.5:
                interpretacion = "🟡 "
                emoji = "📈"
            elif valor > 0.3:
                interpretacion = "🟠 "
                emoji = "⚠️"
            else:
                interpretacion = "🔴 "
                emoji = "📉"

            st.markdown(f"""
            **{emoji} {nombre_materia}**: {interpretacion} `{valor:.2f}`

            """)
            
        st.markdown("""
            ---
            ### 📏 **Escala de Interpretación:**
            - 🟢 No requiere apoyo (predicción > 0.7 )
            - 🟡 Apoyo básico (predicción > 0.5)
            - 🟠 Apoyo moderado (predicción > 0.3)
            - 🔴 Apoyo prioritario (predicción ≤ 0.3)
    
            """)

        
        # ---- Explicación de cómo se calculan las predicciones
        with st.expander("🧮 ¿Cómo se calculan estas predicciones?"):
            st.markdown("""
            ###  **Método de Cálculo: Modelo Probit**
            
            Cada predicción se calcula usando la fórmula matemática:
            
            **Predicción = G(Constante + (Coef₁ × Variable₁) + (Coef₂ × Variable₂) + ... + (Coefₙ × Variableₙ))**
            
            Donde:
            - **G** es la función de distribución acumulativa de la normal estándar (Probit)
            - **Constante (_cons)**: Valor base del modelo
            - **Coeficientes**: Pesos que determinan la importancia de cada variable
            - **Variables**: Los datos que ingresaste del estudiante
            
            ### 🎯 **Ejemplo de cálculo para una materia:**
            ```
            Predicción MATH = G(_cons + 
                            (coef_estu_mujer × estu_mujer) +
                            (coef_edad_grado × edad_grado) +
                            (coef_human_langs_08 × human_langs_08) +
                            ... (todas las demás variables))
            ```
            """)
        
        
        # ---- Cálculos detallados por materia
        with st.expander("🔬 Ver Cálculos Paso a Paso por Materia"):
            st.markdown("###  **Detalles de los Cálculos**")
            st.markdown("*Solo se muestran las contribuciones significativas (> 0.001)*")
            
            for materia in sorted(resultados.keys()):
                with st.container():
                    st.markdown(f"#### 📚 **{materia}** (Resultado: {resultados[materia]:.6f})")
                    
                    detalles = detalles_calculo.get(materia, [])
                    if detalles:
                        for detalle in detalles[:10]:  # Mostrar solo las primeras 10 contribuciones
                            st.code(detalle)
                        
                        if len(detalles) > 10:
                            st.caption(f"... y {len(detalles) - 10} términos adicionales")
                    else:
                        st.error("No se pudieron obtener los detalles del cálculo")
                        
                    st.markdown("---")
        
        # ---- Recomendaciones basadas en resultados
        with st.expander("💡 Recomendaciones Pedagógicas"):
            st.markdown("### 🎯 **Recomendaciones basadas en las predicciones:**")
            
            # Identificar fortalezas y áreas de mejora
            materias_ordenadas = sorted(resultados.items(), key=lambda x: x[1], reverse=True)
            mejor_materia = materias_ordenadas[0]
           
            nombre_mejor_materia = nombres_materias[mejor_materia[0]]
            peor_materia = materias_ordenadas[-1]
            nombre_peor_materia = nombres_materias[peor_materia[0]]

            st.markdown(f"""
            **🌟 Fortaleza principal:** {nombre_mejor_materia} (predicción: {mejor_materia[1]:.3f})
            - Aprovechar esta fortaleza para motivar al estudiante
            - Usar estrategias exitosas de esta área en otras materias

            **🎯 Área de mayor atención:** {nombre_peor_materia} (predicción: {peor_materia[1]:.3f})
            - Implementar estrategias de apoyo específicas
            - Considerar tutoría adicional o recursos complementarios
            """)
            
            # Recomendaciones generales
            promedio_predicciones = sum(resultados.values()) / len(resultados)
            if promedio_predicciones > 0.3:
                st.success("✅ **Perfil general positivo:** El estudiante muestra un buen potencial académico general.")
            elif promedio_predicciones > -0.3:
                st.info("📊 **Perfil equilibrado:** El estudiante tiene un desempeño esperado cercano al promedio.")
            else:
                st.warning("⚠️ **Necesita apoyo:** Se recomienda implementar estrategias de apoyo integral.")
                
            st.markdown(f"**Promedio de predicciones:** {promedio_predicciones:.3f}")
                
        # ---- Descargar datos + predicciones
        st.markdown("---")
        out = {**datos, **{f"pred_{k.lower()}": v for k, v in resultados.items()}}
        df_download = pd.DataFrame([out])
        

        # Descargar como Excel
        excel_data = convert_df_to_excel(df_download, 'Datos_Estudiante')
        st.download_button(
            "Descargar como Excel",
            data=excel_data,
            file_name=f"datos_estudiante_{id_estudiante}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# --------------------------------------------------
# Página 2: Análisis Masivo
# --------------------------------------------------
elif pagina == ":material/article_person: Análisis Masivo":
    st.title(":material/article_person: Análisis Masivo de Estudiantes")
    st.markdown("Suba un archivo Excel con datos de múltiples estudiantes para análisis estadístico completo.")
    
    # Instrucciones del formato
    with st.expander(":material/article: Formato del Archivo Excel"):
        st.markdown("""
        ### **Formato Requerido del Excel:**
        
        El archivo debe contener las siguientes columnas exactamente:
        
        | Columna | Descripción | Tipo |
        |---------|-------------|------|
        | `id` | Identificador del estudiante | Texto |
        | `estu_mujer` | 1=Mujer, 0=Hombre | Numérico |
        | `edad_grado` | Edad del estudiante | Numérico |
        | `educ_max_padremadre1` | Hasta bachillerato | 0 o 1 |
        | `educ_max_padremadre2` | Técnica/tecnológica | 0 o 1 |
        | `educ_max_padremadre3` | Profesional incompleta | 0 o 1 |
        | `educ_max_padremadre4` | Profesional completa | 0 o 1 |
        | `educ_max_padremadre5` | Postgrado | 0 o 1 |
        | `total_faltas_disc` | Número de faltas | Numérico |
        | `human_langs_08` | Promedio Humanidades 8° | Numérico (0-100) |
        | `maths_08` | Promedio Matemáticas 8° | Numérico (0-100) |
        | `nat_sc_08` | Promedio Ciencias Naturales 8° | Numérico (0-100) |
        | `soc_sc_08` | Promedio Ciencias Sociales 8° | Numérico (0-100) |
        | `nwea_math_perc` | Percentil NWEA Matemáticas | Numérico (1-99) |
        | `nwea_reading_perc` | Percentil NWEA Lectura | Numérico (1-99) |
        """)
    
    # Selector de grado para análisis masivo
    grado_masivo = st.radio(
        "Seleccione el grado de los estudiantes",
        options=["9 o 10", "11"],
        horizontal=True,
        key="grado_masivo"
    )
    if grado_masivo == "9 o 10":
        modulo_masivo = 14
    else:
        modulo_masivo = 24

    
    # Upload del archivo
    uploaded_file = st.file_uploader(
        ":material/attachment: Seleccione el archivo Excel con los datos de estudiantes",
        type=['xlsx', 'xls'],
        help="El archivo debe contener todas las columnas requeridas"
    )
    
    if uploaded_file is not None:
        try:
            # Cargar el archivo
            df_estudiantes = pd.read_excel(uploaded_file, sheet_name="Data")
            
            st.success(f"Archivo cargado exitosamente: {len(df_estudiantes)} estudiantes encontrados")
            
            # Verificar columnas requeridas
            columnas_requeridas = [
                'id', 'estu_mujer', 'edad_grado', 'educ_max_padremadre1',
                'educ_max_padremadre2', 'educ_max_padremadre3', 'educ_max_padremadre4',
                'educ_max_padremadre5', 'total_faltas_disc', 'human_langs_08',
                'maths_08', 'nat_sc_08', 'soc_sc_08', 'nwea_math_perc', 'nwea_reading_perc'
            ]
            
            columnas_faltantes = [col for col in columnas_requeridas if col not in df_estudiantes.columns]
            
            if columnas_faltantes:
                st.error(f"❌ Faltan las siguientes columnas: {', '.join(columnas_faltantes)}")
                st.stop()
            
            # Mostrar vista previa
            with st.expander("👁️ Vista Previa de los Datos"):
                st.dataframe(df_estudiantes.head(10), use_container_width=True)
            
            # Botón para procesar
            if st.button("🚀 Procesar Análisis Masivo", type="primary", use_container_width=True):
                with st.spinner("Calculando predicciones para todos los estudiantes..."):
                    
                    # Calcular predicciones para todos los estudiantes
                    materias = ["lectura", "math", "soc", "cnat", "ingles", "global"]
                    resultados_masivos = []
                    
                    progress_bar = st.progress(0)
                    total_estudiantes = len(df_estudiantes)
                    
                    for idx, row in df_estudiantes.iterrows():
                        # Crear diccionario de datos del estudiante
                        datos_estudiante = {
                            "id": row['id'],
                            "estu_mujer": row['estu_mujer'],
                            "edad_grado": row['edad_grado'],
                            "educ_max_padremadre1": row['educ_max_padremadre1'],
                            "educ_max_padremadre2": row['educ_max_padremadre2'],
                            "educ_max_padremadre3": row['educ_max_padremadre3'],
                            "educ_max_padremadre4": row['educ_max_padremadre4'],
                            "educ_max_padremadre5": row['educ_max_padremadre5'],
                            "total_faltas_disc": row['total_faltas_disc'],
                            "human_langs_08": row['human_langs_08'],
                            "maths_08": row['maths_08'],
                            "nat_sc_08": row['nat_sc_08'],
                            "soc_sc_08": row['soc_sc_08'],
                            "nwea_math_perc": row['nwea_math_perc'],
                            "nwea_reading_perc": row['nwea_reading_perc'],
                        }
                        
                        # Calcular predicciones
                        predicciones_estudiante = {"id": row['id']}
                        for mat in materias:
                            try:
                                hoja = f"s11_{mat}_mod{modulo_masivo}"
                                if hoja in MODELOS:
                                    modelo = MODELOS[hoja]
                                    prediccion = predecir_probit(modelo, datos_estudiante)
                                    predicciones_estudiante[f"pred_{mat}"] = prediccion
                                else:
                                    predicciones_estudiante[f"pred_{mat}"] = np.nan
                            except:
                                predicciones_estudiante[f"pred_{mat}"] = np.nan
                        
                        resultados_masivos.append(predicciones_estudiante)
                        
                        # Actualizar barra de progreso
                        progress_bar.progress((idx + 1) / total_estudiantes)
                    
                    # Crear DataFrame con resultados
                    df_resultados = pd.DataFrame(resultados_masivos)
                    
                    # Combinar datos originales con predicciones
                    df_completo = df_estudiantes.merge(df_resultados, on='id', how='left')
                    
                    st.success("✅ ¡Análisis masivo completado!")
                    
                    # --------------------------------------------------
                    # ESTADÍSTICAS Y VISUALIZACIONES
                    # --------------------------------------------------
                    
                    st.header(":material/bar_chart_4_bars: Estadísticas Generales")
                    
                    # Métricas principales
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Estudiantes", len(df_completo))
                    with col2:
                        mujeres = df_completo['estu_mujer'].sum()
                        st.metric("Mujeres", f"{mujeres} ({mujeres/len(df_completo)*100:.1f}%)")
                    with col3:
                        edad_promedio = df_completo['edad_grado'].mean()
                        st.metric("Edad Promedio", f"{edad_promedio:.1f} años")
                    with col4:
                        faltas_promedio = df_completo['total_faltas_disc'].mean()
                        st.metric("Faltas Promedio", f"{faltas_promedio:.1f}")
                    
                    # Estadísticas de predicciones
                    st.subheader(":material/finance_mode: Estadísticas de Predicciones")
                    
                    # Crear tabla de estadísticas
                    materias_pred = ['pred_global', 'pred_lectura', 'pred_math', 'pred_cnat', 'pred_soc', 'pred_ingles' ]
                    stats_data = []
                    
                    for materia in materias_pred:
                        if materia in df_completo.columns:
                            serie = df_completo[materia].dropna()
                            stats_data.append({
                                'Materia': materia.replace('pred_', '').upper(),
                                'Promedio': serie.mean(),
                                'Mediana': serie.median(),
                                'Desv. Estándar': serie.std(),
                                'Mínimo': serie.min(),
                                'Máximo': serie.max(),
                                'Positivos (%)': (serie > 0).sum() / len(serie) * 100
                            })
                    
                    df_stats = pd.DataFrame(stats_data)
                    df_stats = df_stats.round(3)
                    st.dataframe(df_stats, use_container_width=True)
                    
                    # --------------------------------------------------
                    # VISUALIZACIONES
                    # --------------------------------------------------

                    st.subheader(":material/analytics: Visualizaciones")

                    # Gráfico de distribución de predicciones
                    fig_dist = make_subplots(
                        rows=2, cols=3,
                        subplot_titles=[mat.replace('pred_', '').upper() for mat in materias_pred],
                        specs=[[{"secondary_y": False}]*3]*2
                    )
                    
                    for i, materia in enumerate(materias_pred):
                        if materia in df_completo.columns:
                            row = (i // 3) + 1
                            col = (i % 3) + 1
                            
                            data = df_completo[materia].dropna()
                            fig_dist.add_trace(
                                go.Histogram(x=data, name=materia.replace('pred_', '').upper(), showlegend=False),
                                row=row, col=col
                            )
                    
                    fig_dist.update_layout(
                        title="Distribución de Predicciones por Materia",
                        height=600,
                        showlegend=False
                    )
                    st.plotly_chart(fig_dist, use_container_width=True)
                    
  
                    
                    # Gráfico de rendimiento por género
                    if 'estu_mujer' in df_completo.columns:
                        st.subheader(":material/groups_3: Análisis por Género")
                        
                        # Preparar datos para el gráfico
                        genero_data = []
                        for materia in materias_pred:
                            if materia in df_completo.columns:
                                for genero in [0, 1]:
                                    subset = df_completo[df_completo['estu_mujer'] == genero]
                                    if len(subset) > 0:
                                        promedio = subset[materia].mean()
                                        promedio = round(promedio, 2)
                                        genero_data.append({
                                            'Materia': materia.replace('pred_', '').upper(),
                                            'Género': 'Mujer' if genero == 1 else 'Hombre',
                                            'Promedio': promedio
                                        })
                        
                        if genero_data:
                            df_genero = pd.DataFrame(genero_data)
                            fig_genero = px.bar(
                                df_genero, 
                                x='Materia', 
                                y='Promedio', 
                                color='Género',
                                title="Promedio de Predicciones por Género",
                                barmode='group',
                                range_y=(0,1.1)
                            )
                            st.plotly_chart(fig_genero, use_container_width=True)
                    
                    # Análisis de factores de riesgo
                    st.subheader(":material/crisis_alert: Análisis de Factores de Riesgo")
                    
                    # Estudiantes con bajo rendimiento
                    threshold = 0.5
                    materias_bajo = []
                    for materia in materias_pred:
                        if materia in df_completo.columns:
                            bajo_rendimiento = (df_completo[materia] < threshold).sum()
                            porcentaje = bajo_rendimiento / len(df_completo) * 100
                            porcentaje = round(porcentaje, 2)
                            materias_bajo.append({
                                'Materia': materia.replace('pred_', '').upper(),
                                'Estudiantes en Riesgo': bajo_rendimiento,
                                'Porcentaje': porcentaje
                            })
                    
                    if materias_bajo:
                        df_riesgo = pd.DataFrame(materias_bajo)
                        st.dataframe(df_riesgo, use_container_width=True)
                        
                        # Gráfico de factores de riesgo
                        fig_riesgo = px.bar(
                            df_riesgo,
                            x='Materia',
                            y='Porcentaje',
                            title="Porcentaje de Estudiantes en Riesgo por Materia",
                            color='Porcentaje',
                            color_continuous_scale="Reds",
                            range_y=(0, 101)
                        )
                        st.plotly_chart(fig_riesgo, use_container_width=True)
                    
                    # --------------------------------------------------
                    # DESCARGA DE RESULTADOS
                    # --------------------------------------------------
                    
                    st.subheader("Descargar Resultados")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Descarga completa como Excel
                        excel_completo = convert_df_to_excel(df_completo, 'Analisis_Completo')
                        st.download_button(
                            "Descargar Datos Completos (Excel)",
                            data=excel_completo,
                            file_name="analisis_masivo_completo.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                                            
                    with col2:
                        # Descarga estadísticas como Excel
                        excel_stats = convert_df_to_excel(df_stats, 'Estadisticas')
                        st.download_button(
                            "Descargar Estadísticas (Excel)",
                            data=excel_stats,
                            file_name="estadisticas_predicciones.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                    # Vista previa de resultados
                    with st.expander("Vista Previa de Resultados Completos"):
                        st.dataframe(df_completo, use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")
            st.info("Verifique que el archivo tenga el formato correcto y todas las columnas requeridas.")
