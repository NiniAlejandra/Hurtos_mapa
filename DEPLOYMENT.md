# Guía de Despliegue en Render

## Pasos para Publicar la Aplicación

### 1. Preparar el Repositorio

1. **Crear un repositorio en GitHub:**
   - Ve a [GitHub](https://github.com)
   - Crea un nuevo repositorio llamado `hurtos-esip-dashboard`
   - Sube todos los archivos del proyecto

### 2. Configurar Render

1. **Ir a Render:**
   - Ve a [render.com](https://render.com)
   - Crea una cuenta o inicia sesión

2. **Crear Nuevo Servicio Web:**
   - Haz clic en "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub

3. **Configurar el Servicio:**
   - **Name:** `hurtos-esip-dashboard`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:server --bind 0.0.0.0:$PORT`

### 3. Variables de Entorno (Opcional)

Si necesitas configurar variables de entorno:
- Ve a la sección "Environment" en tu servicio
- Agrega variables como:
  - `DEBUG=False`
  - `PORT=10000`

### 4. Desplegar

1. **Hacer clic en "Create Web Service"**
2. **Esperar el build** (puede tomar 5-10 minutos)
3. **Verificar que la aplicación funcione**

### 5. URL de Acceso

Una vez desplegado, tendrás una URL como:
`https://hurtos-esip-dashboard.onrender.com`

## Archivos Importantes

- `app.py` - Aplicación principal
- `requirements.txt` - Dependencias de Python
- `render.yaml` - Configuración de Render
- `Bd_hurtos_06_2025_v1.csv` - Datos de hurtos
- `logo_esip_clear.png` - Logo de ESIP

## Solución de Problemas

### Error de Build
- Verifica que todas las dependencias estén en `requirements.txt`
- Asegúrate de que el archivo `app.py` tenga la variable `server`

### Error de Runtime
- Revisa los logs en Render
- Verifica que los archivos CSV y PNG estén en el repositorio

### Error de Puerto
- Render asigna automáticamente el puerto
- Usa `$PORT` en lugar de un puerto fijo

## Características del Despliegue

✅ **Mapa Interactivo** con zonas de calor
✅ **Filtros por Año** (2022-2025)
✅ **Gráficos Estadísticos** por mes y año
✅ **Diseño Responsivo** para diferentes dispositivos
✅ **Logo de ESIP** integrado
✅ **Footer con información** de la empresa

## Soporte

Para problemas técnicos:
- Revisa los logs en Render
- Verifica la configuración en `render.yaml`
- Asegúrate de que todos los archivos estén en el repositorio 