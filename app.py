import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm

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
    page_title="Sistema de Predicción",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Sistema de Predicción - Colegio Parrish")
st.markdown("---")

# Crear sidebar para navegación
st.sidebar.title("🧭 Navegación")
pagina = st.sidebar.radio(
    "Seleccione una opción:",
    ["📝 Estudiante Individual", "📊 Análisis Masivo"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📋 **Acerca del Sistema**
- **Página Individual**: Analiza un estudiante específico
- **Análisis Masivo**: Procesa múltiples estudiantes desde Excel
""")

# --------------------------------------------------
# Página 1: Estudiante Individual
# --------------------------------------------------
if pagina == "📝 Estudiante Individual":

    st.header("📝 Análisis Individual de Estudiante")
    st.markdown("Ingrese los datos de un estudiante para obtener predicciones personalizadas.")
    
    # ---------- Selector de grado ----------
    grado = st.radio(
        "Seleccione el grado en que se encuentra el estudiante",
        options=["8 o 9", "10 o 11"],
        horizontal=True,
    )

    # Asignar el módulo basado en la selección
    if grado == "8 o 9":
        modulo = 14
    else:  # "10 o 11"
        modulo = 24
    st.markdown("---")

    st.subheader("Información del Estudiante")

    # ---------- Formulario ----------
    with st.form("formulario_estudiante"):
        # 🆔 Identificación
        st.subheader("🆔 Identificación")
        id_estudiante = st.text_input(
            "Identificador del estudiante",
            value="",
            help="Ingrese el identificador único del estudiante",
        )

        # 📋 Información Demográfica
        st.subheader("📋 Información Demográfica")
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
        st.subheader("🎓 Educación Máxima de los Padres/Madres")
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
        st.subheader("⚠️ Comportamiento")
        total_faltas_disc = st.number_input(
            "Número total de faltas disciplinarias del estudiante",
            min_value=0,
            max_value=100,
            value=0,
        )

        # 📚 Promedios 8°
        st.subheader("📚 Promedios de 8° Grado")
        st.markdown("*Promedio obtenido en 8° grado en cada área (escala 0-100)*")
        col1, col2 = st.columns(2)
        with col1:
            human_langs_08 = st.number_input(
                "Humanidades, lengua castellana e idiomas extranjeros",
                min_value=0.0,
                max_value=100.0,
                value=85.0,
                step=0.1,
            )
            maths_08 = st.number_input(
                "Matemáticas",
                min_value=0.0,
                max_value=100.0,
                value=85.0,
                step=0.1,
            )
        with col2:
            nat_sc_08 = st.number_input(
                "Ciencias naturales y educación ambiental",
                min_value=0.0,
                max_value=100.0,
                value=85.0,
                step=0.1,
            )
            soc_sc_08 = st.number_input(
                "Ciencias sociales, historia, geografía, constitución política y democracia",
                min_value=0.0,
                max_value=100.0,
                value=85.0,
                step=0.1,
            )
            
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
        materias = ["lectura", "math", "soc", "cnat", "ingles", "global"]
        resultados = {}
        detalles_calculo = {}
        errores = []
        
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
        st.success("✅ ¡Datos capturados y procesados exitosamente!")

        # ---- Resumen de predicciones
        st.subheader("📈 Predicción por Materia")
        pred_df = (
            pd.Series(resultados)
            .rename_axis("Materia")
            .reset_index(name="Predicción")
        )
        pred_df['Alto'] = pred_df['Predicción'] > 0.5
        
        # Redondear predicciones para mejor visualización
        pred_df["Predicción"] = pred_df["Predicción"].round(4)
        st.dataframe(pred_df, use_container_width=True)
        
        # ---- Explicación de cómo se calculan las predicciones
        with st.expander("🧮 ¿Cómo se calculan estas predicciones?"):
            st.markdown("""
            ### 📊 **Método de Cálculo: Modelo Probit**
            
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
        
        # ---- Interpretación de resultados
        with st.expander("📋 Interpretación de los Resultados"):
            st.markdown("### 🎯 **¿Qué significan estos números?**")
            
            for materia, valor in sorted(resultados.items()):
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
                **{emoji} {materia}**: `{valor:.4f}`  
                {interpretacion}
                """)
            
            st.markdown("""
            ---
            ### 📏 **Escala de Interpretación:**
            - 🟢 Alto potencial (predicción > 0.7 )
            - 🟡 Potencial moderado (predicción > 0.5)
            - 🟠 Potencial bajo (predicción > 0.3)
            - 🔴 Necesita apoyo (predicción ≤ 0.3)
    
            """)
        
        # ---- Cálculos detallados por materia
        with st.expander("🔬 Ver Cálculos Paso a Paso por Materia"):
            st.markdown("### 🧮 **Detalles de los Cálculos**")
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
            peor_materia = materias_ordenadas[-1]
            
            st.markdown(f"""
            **🌟 Fortaleza principal:** {mejor_materia[0]} (predicción: {mejor_materia[1]:.3f})
            - Aprovechar esta fortaleza para motivar al estudiante
            - Usar estrategias exitosas de esta área en otras materias
            
            **🎯 Área de mayor atención:** {peor_materia[0]} (predicción: {peor_materia[1]:.3f})
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
                
        st.markdown("---")

        # ---- Tabla con los datos capturados
        st.subheader("📋 Resumen de Datos Capturados")
        df_resumen = (
            pd.DataFrame({"Variable": list(datos.keys()), "Valor": list(datos.values())})
            .set_index("Variable")
        )
        st.dataframe(df_resumen, use_container_width=True)

        # ---- Descargar datos + predicciones
        st.markdown("---")
        out = {**datos, **{f"pred_{k.lower()}": v for k, v in resultados.items()}}
        csv = pd.DataFrame([out]).to_csv(index=False)
        st.download_button(
            "📥 Descargar todo como CSV",
            data=csv,
            file_name=f"datos_estudiante_{id_estudiante}.csv",
            mime="text/csv",
        )

# --------------------------------------------------
# Página 2: Análisis Masivo
# --------------------------------------------------
elif pagina == "📊 Análisis Masivo":
    st.header("📊 Análisis Masivo de Estudiantes")
    st.markdown("Suba un archivo Excel con datos de múltiples estudiantes para análisis estadístico completo.")
    
    # Instrucciones del formato
    with st.expander("📋 Formato del Archivo Excel"):
        st.markdown("""
        ### 📁 **Formato Requerido del Excel:**
        
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
    col1, col2 = st.columns(2)
    with col1:
        grado_masivo = st.radio(
            "Seleccione el grado de los estudiantes",
            options=["8 o 9", "10 o 11"],
            horizontal=True,
            key="grado_masivo"
        )
        if grado_masivo == "8 o 9":
            modulo_masivo = 14
        else:
            modulo_masivo = 24
    
    with col2:
        st.info(f"📊 **Usando modelos {modulo_masivo}**")
    
    # Upload del archivo
    uploaded_file = st.file_uploader(
        "📁 Seleccione el archivo Excel con los datos de estudiantes",
        type=['xlsx', 'xls'],
        help="El archivo debe contener todas las columnas requeridas"
    )
    
    if uploaded_file is not None:
        try:
            # Cargar el archivo
            df_estudiantes = pd.read_excel(uploaded_file, sheet_name="Data")
            
            st.success(f"✅ Archivo cargado exitosamente: {len(df_estudiantes)} estudiantes encontrados")
            
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
                    
                    st.header("📊 Estadísticas Generales")
                    
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
                    st.subheader("📈 Estadísticas de Predicciones")
                    
                    # Crear tabla de estadísticas
                    materias_pred = ['pred_lectura', 'pred_math', 'pred_soc', 'pred_cnat', 'pred_ingles', 'pred_global']
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
                    
                    st.subheader("📊 Visualizaciones")
                    
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
                    
                    # Gráfico de correlaciones
                    if len(materias_pred) > 1:
                        materias_disponibles = [mat for mat in materias_pred if mat in df_completo.columns]
                        if len(materias_disponibles) > 1:
                            corr_matrix = df_completo[materias_disponibles].corr()
                            
                            fig_corr = px.imshow(
                                corr_matrix,
                                title="Matriz de Correlación entre Predicciones",
                                color_continuous_scale="RdBu_r",
                                aspect="auto"
                            )
                            fig_corr.update_layout(height=500)
                            st.plotly_chart(fig_corr, use_container_width=True)
                    
                    # Gráfico de rendimiento por género
                    if 'estu_mujer' in df_completo.columns:
                        st.subheader("👥 Análisis por Género")
                        
                        # Preparar datos para el gráfico
                        genero_data = []
                        for materia in materias_pred:
                            if materia in df_completo.columns:
                                for genero in [0, 1]:
                                    subset = df_completo[df_completo['estu_mujer'] == genero]
                                    if len(subset) > 0:
                                        promedio = subset[materia].mean()
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
                                barmode='group'
                            )
                            st.plotly_chart(fig_genero, use_container_width=True)
                    
                    # Análisis de factores de riesgo
                    st.subheader("⚠️ Análisis de Factores de Riesgo")
                    
                    # Estudiantes con bajo rendimiento
                    threshold = -0.5
                    materias_bajo = []
                    for materia in materias_pred:
                        if materia in df_completo.columns:
                            bajo_rendimiento = (df_completo[materia] < threshold).sum()
                            porcentaje = bajo_rendimiento / len(df_completo) * 100
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
                            color_continuous_scale="Reds"
                        )
                        st.plotly_chart(fig_riesgo, use_container_width=True)
                    
                    # --------------------------------------------------
                    # DESCARGA DE RESULTADOS
                    # --------------------------------------------------
                    
                    st.subheader("📥 Descargar Resultados")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Descarga completa
                        csv_completo = df_completo.to_csv(index=False)
                        st.download_button(
                            "📄 Descargar Datos Completos (CSV)",
                            data=csv_completo,
                            file_name="analisis_masivo_completo.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        # Descarga solo estadísticas
                        csv_stats = df_stats.to_csv(index=False)
                        st.download_button(
                            "📊 Descargar Estadísticas (CSV)",
                            data=csv_stats,
                            file_name="estadisticas_predicciones.csv",
                            mime="text/csv"
                        )
                    
                    # Vista previa de resultados
                    with st.expander("👁️ Vista Previa de Resultados Completos"):
                        st.dataframe(df_completo, use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")
            st.info("Verifique que el archivo tenga el formato correcto y todas las columnas requeridas.")
