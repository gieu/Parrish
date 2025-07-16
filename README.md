# 📊 Sistema de Predicción Académica - Colegio Parrish

Sistema web avanzado desarrollado con Streamlit para predicción del rendimiento académico de estudiantes usando modelos de machine learning. La aplicación cuenta con dos módulos principales: análisis individual y análisis masivo de estudiantes.

## 🚀 Características Principales

### 📝 **Módulo Individual**
- **Formulario interactivo** para capturar datos de estudiantes individuales
- **Predicciones automáticas** en 6 materias (Lectura, Matemáticas, Ciencias Sociales, Ciencias Naturales, Inglés, Global)
- **Explicaciones detalladas** del método de cálculo (regresión lineal)
- **Interpretaciones pedagógicas** con recomendaciones personalizadas
- **Cálculos paso a paso** de cada predicción
- **Selector automático de módulo** según el grado del estudiante

### 📊 **Módulo de Análisis Masivo**
- **Carga masiva** de datos desde archivos Excel
- **Procesamiento automático** con barra de progreso
- **Estadísticas descriptivas** completas por materia
- **Visualizaciones interactivas** con Plotly:
  - Distribuciones de predicciones
  - Matrices de correlación
  - Análisis por género
  - Factores de riesgo
- **Identificación automática** de estudiantes en riesgo
- **Exportación completa** de resultados y estadísticas

### 🤖 **Sistema de Predicción**
- **Modelos de regresión lineal** entrenados previamente
- **Dos módulos de coeficientes**: Módulo 14 (grados 8-9) y Módulo 24 (grados 10-11)
- **Manejo robusto de errores** y validación de datos
- **Cache optimizado** para carga rápida de modelos

## 📋 Variables del Modelo

| Variable | Descripción | Rango/Tipo |
|----------|-------------|------------|
| `id` | Identificador único del estudiante | Texto |
| `estu_mujer` | Género (1=Mujer, 0=Hombre) | Binario |
| `edad_grado` | Edad del estudiante a la fecha de grado | 10-25 años |
| `educ_max_padremadre1` | Hasta bachillerato/secundaria completa | 0 o 1 |
| `educ_max_padremadre2` | Técnica o tecnológica | 0 o 1 |
| `educ_max_padremadre3` | Educación profesional incompleta | 0 o 1 |
| `educ_max_padremadre4` | Educación profesional completa | 0 o 1 |
| `educ_max_padremadre5` | Postgrado | 0 o 1 |
| `total_faltas_disc` | Número total de faltas disciplinarias | 0-100 |
| `human_langs_08` | Promedio Humanidades 8° grado | 0-100 |
| `maths_08` | Promedio Matemáticas 8° grado | 0-100 |
| `nat_sc_08` | Promedio Ciencias Naturales 8° grado | 0-100 |
| `soc_sc_08` | Promedio Ciencias Sociales 8° grado | 0-100 |
| `nwea_math_perc` | Percentil NWEA Matemáticas | 1-99 |
| `nwea_reading_perc` | Percentil NWEA Lectura | 1-99 |

## 🎯 Materias Predichas

1. **Lectura** - Comprensión lectora y análisis textual
2. **Matemáticas** - Competencias matemáticas generales
3. **Ciencias Sociales** - Historia, geografía, constitución
4. **Ciencias Naturales** - Biología, química, física
5. **Inglés** - Competencia en lengua extranjera
6. **Global** - Rendimiento académico general

## 🛠️ Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- Archivo `Coeficientes_modelos.xlsx` con los modelos entrenados

### Pasos de Instalación

1. **Clonar o descargar el proyecto:**
   ```bash
   git clone [URL-del-repositorio]
   cd "Colegio Parrish"
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verificar archivos requeridos:**
   - `Coeficientes_modelos.xlsx` (debe estar en el directorio raíz)
   - Contener hojas con formato: `s11_[materia]_mod[14|24]`

4. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

5. **Acceder a la aplicación:**
   - URL Local: `http://localhost:8501`
   - La aplicación se abre automáticamente en el navegador

## 📖 Manual de Uso

### 📝 **Análisis Individual**

1. **Seleccionar grado:** Elija entre "8 o 9" o "10 o 11" (selecciona automáticamente el módulo)
2. **Completar formulario:** Ingrese todos los datos del estudiante
3. **Procesar datos:** Haga clic en "🚀 Procesar Datos"
4. **Revisar resultados:**
   - Predicciones por materia
   - Interpretaciones pedagógicas
   - Cálculos detallados (opcional)
   - Recomendaciones personalizadas
5. **Descargar:** Exporte los resultados en formato CSV

### 📊 **Análisis Masivo**

1. **Preparar archivo Excel:**
   - Incluir todas las columnas requeridas
   - Formato exacto según especificaciones
2. **Seleccionar grado:** Configurar módulo para todos los estudiantes
3. **Cargar archivo:** Usar el uploader de archivos Excel
4. **Procesar:** Ejecutar análisis masivo (incluye barra de progreso)
5. **Revisar resultados:**
   - Estadísticas generales
   - Visualizaciones interactivas
   - Análisis de riesgo
6. **Descargar:** Resultados completos y estadísticas en CSV

## 📁 Estructura del Proyecto

```
Colegio Parrish/
├── app.py                          # ✨ Aplicación principal (multi-página)
├── requirements.txt                # 📋 Dependencias actualizadas
├── README.md                      # 📖 Documentación (este archivo)
├── setup.bat                      # 🔧 Script de instalación
├── Coeficientes_modelos.xlsx      # 🤖 Modelos de ML entrenados
└── B.D.Visualización_enviar.xlsx  # 📊 Base de datos de referencia
```

## 🔧 Tecnologías y Dependencias

- **Streamlit** - Framework de aplicaciones web
- **Pandas** - Manipulación y análisis de datos
- **NumPy** - Operaciones numéricas avanzadas
- **Plotly** - Visualizaciones interactivas
- **OpenPyXL** - Lectura de archivos Excel
- **Pathlib** - Manejo de rutas de archivos

## � Interpretación de Resultados

### Escala de Predicciones
- **Valores positivos:** Por encima del promedio poblacional
- **Valores negativos:** Por debajo del promedio poblacional
- **Cerca de 0:** Rendimiento promedio esperado
- **Mayor valor absoluto:** Mayor diferencia respecto al promedio

### Códigos de Color
- 🟢 **Por encima del promedio** (> 0.5)
- 🟡 **Ligeramente por encima** (0 a 0.5)
- 🟠 **Ligeramente por debajo** (-0.5 a 0)
- 🔴 **Por debajo del promedio** (< -0.5)

## 🎯 Casos de Uso

### Para Docentes
- Identificación temprana de estudiantes en riesgo
- Planificación de estrategias pedagógicas personalizadas
- Seguimiento individual del progreso académico

### Para Coordinadores Académicos
- Análisis poblacional de cohortes
- Identificación de patrones y tendencias
- Toma de decisiones basada en datos

### Para Investigadores
- Análisis estadístico de factores predictivos
- Validación de modelos educativos
- Generación de reportes académicos

## 🔒 Consideraciones de Privacidad

- Los datos se procesan localmente
- No se almacenan datos de estudiantes en la aplicación
- Cumple con estándares de protección de datos educativos
- Recomendado para uso interno institucional

## 🚨 Solución de Problemas

### Error de Carga de Modelos
- Verificar que `Coeficientes_modelos.xlsx` existe
- Confirmar formato correcto de las hojas del Excel
- Revisar permisos de archivo

### Error en Análisis Masivo
- Validar formato del archivo Excel de entrada
- Verificar nombres exactos de columnas
- Comprobar tipos de datos numéricos

### Problemas de Rendimiento
- La aplicación usa cache para optimizar la carga
- Para archivos muy grandes (>1000 estudiantes), considerar dividir en lotes

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema:
- Revisar la documentación integrada en la aplicación
- Verificar logs de error en la consola de Streamlit
- Contactar al equipo de desarrollo institucional

---

**Versión:** 2.0 - Sistema Multi-Página con Análisis Masivo  
**Última actualización:** Julio 2025  
**Desarrollado para:** Colegio Parrish
