# Aplicación de Hurtos - Versión HTML Portable

## Descripción

Esta es una versión HTML portable de la aplicación de análisis de hurtos del Sistema de Alumbrado Público de ESIP SAS ESP. La aplicación permite visualizar y analizar datos de hurtos de manera interactiva sin necesidad de un servidor web.

## Características

- **Visualización Geográfica**: Mapa interactivo con puntos de hurtos y zonas de calor
- **Filtros Dinámicos**: Selección de años y tipos de visualización
- **Gráficos Estadísticos**: Distribución por mes y año
- **Estadísticas en Tiempo Real**: Actualización automática de estadísticas
- **Interfaz Responsiva**: Diseño adaptativo para diferentes dispositivos

## Cómo Usar

### 1. Abrir la Aplicación

1. Navega hasta la carpeta donde se encuentra el archivo `hurtos_portable.html`
2. Haz doble clic en el archivo `hurtos_portable.html`
3. Se abrirá automáticamente en tu navegador web predeterminado

### 2. Funcionalidades

#### Panel de Control (Lado Izquierdo)
- **Filtro de Años**: Selecciona uno o varios años para filtrar los datos
- **Tipo de Visualización**: 
  - **Ambos**: Muestra puntos individuales y zonas de calor
  - **Puntos Individuales**: Solo muestra los puntos de cada hurto
  - **Zonas de Calor**: Solo muestra las áreas de mayor densidad
- **Estadísticas Generales**: Muestra el total de hurtos y desglose por año

#### Mapa Interactivo
- **Zoom**: Usa la rueda del mouse para acercar/alejar
- **Pan**: Haz clic y arrastra para mover el mapa
- **Hover**: Pasa el mouse sobre los puntos para ver detalles
- **Leyenda**: Muestra la información de cada año con colores diferentes

#### Gráficos Estadísticos
- **Distribución por Mes**: Gráfico de barras apiladas por mes y año
- **Distribución por Año**: Gráfico de barras por año

## Requisitos del Sistema

- **Navegador Web Moderno**: Chrome, Firefox, Safari, Edge (versiones recientes)
- **Conexión a Internet**: Requerida para cargar las librerías de Plotly y mapas
- **JavaScript Habilitado**: Necesario para la funcionalidad interactiva

## Datos Incluidos

La aplicación incluye datos de hurtos desde enero de 2022 hasta junio de 2025, con información como:
- Ubicación geográfica (latitud/longitud)
- Fecha del hurto
- Dirección
- Sticker del elemento
- Año y mes

## Ventajas de la Versión Portable

1. **Sin Servidor**: No requiere instalación de servidor web
2. **Fácil Distribución**: Un solo archivo HTML que contiene toda la aplicación
3. **Funcionamiento Offline**: Una vez cargada, funciona sin conexión a internet
4. **Compatibilidad**: Funciona en cualquier navegador moderno
5. **Portabilidad**: Puede ser compartida fácilmente por email o almacenamiento

## Solución de Problemas

### La aplicación no carga
- Verifica que el archivo `hurtos_portable.html` esté completo
- Asegúrate de tener una conexión a internet para cargar las librerías
- Intenta abrir el archivo en un navegador diferente

### Los gráficos no se muestran
- Verifica que JavaScript esté habilitado en tu navegador
- Espera unos segundos para que se carguen los datos
- Recarga la página si es necesario

### El mapa no se carga
- Verifica tu conexión a internet
- Los mapas requieren conexión para cargar las imágenes de OpenStreetMap

## Información Técnica

- **Tecnologías**: HTML5, CSS3, JavaScript, Plotly.js
- **Mapas**: OpenStreetMap (requiere conexión a internet)
- **Datos**: CSV embebido en el archivo HTML
- **Tamaño**: Aproximadamente 570KB

## Contacto

Desarrollado por A.V. ESIP SAS ESP
© Todos los Derechos Reservados

---

**Nota**: Esta versión portable es ideal para presentaciones, demostraciones o cuando no se tiene acceso a un servidor web. Para uso en producción, se recomienda la versión completa con servidor. 