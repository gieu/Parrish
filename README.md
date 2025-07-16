# 📊 Formulario de Captura de Datos Educativos - Streamlit

Este proyecto es una aplicación web desarrollada con Streamlit que permite capturar datos educativos de estudiantes a través de un formulario interactivo.

## 🚀 Características

- **Formulario interactivo** para capturar 14 variables educativas
- **Validación de datos** con rangos apropiados
- **Visualización inmediata** de los datos capturados
- **Exportación a CSV** de los datos ingresados
- **Interfaz moderna** y fácil de usar

## 📋 Variables Capturadas

1. **estu_mujer**: Género del estudiante (0=Hombre, 1=Mujer)
2. **edad_grado**: Edad por grado
3. **educ_max_padremadre1-5**: Nivel educativo máximo de los padres/madres
4. **total_faltas_disc**: Total de faltas disciplinarias
5. **human_langs_08**: Calificación en Lenguajes Humanos 2008
6. **maths_08**: Calificación en Matemáticas 2008
7. **nat_sc_08**: Calificación en Ciencias Naturales 2008
8. **soc_sc_08**: Calificación en Ciencias Sociales 2008
9. **nwea_math_perc**: Percentil NWEA Matemáticas
10. **nwea_reading_perc**: Percentil NWEA Lectura

## 🛠️ Instalación

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación:**
   ```bash
   streamlit run app.py
   ```

3. **Abrir en el navegador:**
   La aplicación se abrirá automáticamente en `http://localhost:8501`

## 🎯 Uso

1. Completa todos los campos del formulario
2. Haz clic en "🚀 Procesar Datos"
3. Revisa el resumen de datos capturados
4. Descarga los datos en formato CSV si es necesario

## 📁 Estructura del Proyecto

```
Streamlit/
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias
├── README.md                      # Este archivo
├── B.D.Visualización_enviar.xlsx  # Base de datos existente
└── Coeficientes_modelos.xlsx      # Coeficientes del modelo
```

## 🔧 Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web
- **Pandas**: Manipulación de datos
- **NumPy**: Operaciones numéricas
- **OpenPyXL**: Lectura de archivos Excel

## 📝 Notas

- Todos los campos tienen validaciones apropiadas
- Los datos se pueden exportar en formato CSV
- La interfaz es responsive y funciona en dispositivos móviles
