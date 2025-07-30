# Aplicación de Visualización de Hurtos - Sistema de Alumbrado Público Neiva

## Descripción

Esta aplicación Dash permite visualizar la distribución geográfica y temporal de los hurtos de luminarias del Sistema de Alumbrado Público del Municipio de Neiva, administrado por ESIP SAS ESP.

## Características

- **Mapa Interactivo**: Visualización geográfica de hurtos con zoom y scroll
- **Filtros por Año**: Selección múltiple de años para filtrar datos
- **Gráficos Estadísticos**: Distribución por mes y año
- **Colores por Año**: 
  - 2022: Púrpura (#8338ec)
  - 2023: Verde Brillante (#38b000)
  - 2024: Rosa (#ff006e)
  - 2025: Azul (#3a86ff)

## Instalación

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verificar archivos**:
   - `Bd_hurtos_06_2025_v1.csv` (datos de hurtos)
   - `logo_esip_clear.png` (logo de ESIP)

## Ejecución

1. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

2. **Acceder a la aplicación**:
   - Abrir navegador en: `http://localhost:8050`

## Estructura de Datos

El archivo CSV debe contener las siguientes columnas:
- `FECHA HURTO`: Fecha del hurto (formato DD/MM/AAAA)
- `LATITUD`: Coordenada de latitud
- `LONGITUD`: Coordenada de longitud
- `STICKER`: Identificador único de la luminaria
- `DIRECCION`: Dirección del hurto

## Funcionalidades

### Mapa Interactivo
- Visualización de puntos georreferenciados
- Zonas de calor (heatmap) para identificar áreas de alta densidad
- Zoom con scroll del mouse
- Hover con información detallada
- Leyenda por año
- Opciones de visualización: puntos individuales, zonas de calor, o ambos

### Filtros
- Selección múltiple de años
- Estadísticas en tiempo real
- Actualización automática de gráficos

### Gráficos
- **Distribución por Mes**: Gráfico de barras apiladas
- **Distribución por Año**: Gráfico de barras simple

## Tecnologías Utilizadas

- **Dash**: Framework web para aplicaciones analíticas
- **Plotly**: Biblioteca de gráficos interactivos
- **Pandas**: Manipulación y análisis de datos
- **OpenStreetMap**: Mapas base

## Desarrollado por

A.V. ESIP SAS ESP. © Todos los Derechos Reservados 