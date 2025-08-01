import pandas as pd
import base64
import json

def load_data():
    df = pd.read_csv('Bd_hurtos_06_2025_v1.csv')
    
    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()
    
    # Convertir fecha a datetime
    def parse_date(date_str):
        if pd.isna(date_str) or date_str == '':
            return pd.NaT
        
        formats = ['%m/%d/%Y', '%d/%m/%Y', '%m/%d/%y', '%d/%m/%y']
        
        for fmt in formats:
            try:
                parsed_date = pd.to_datetime(date_str, format=fmt)
                if parsed_date.year >= 2020 and parsed_date.year <= 2025:
                    return parsed_date
            except:
                continue
        
        return pd.NaT
    
    df['FECHA HURTO'] = df['FECHA HURTO'].apply(parse_date)
    df = df.dropna(subset=['FECHA HURTO'])
    
    # Extraer año y mes
    df['AÑO'] = df['FECHA HURTO'].dt.year
    df['MES'] = df['FECHA HURTO'].dt.month
    df['MES_NOMBRE'] = df['FECHA HURTO'].dt.strftime('%B')
    
    # Mapeo de colores por año
    color_map = {
        2022: '#8338ec',
        2023: '#38b000', 
        2024: '#ff006e',
        2025: '#3a86ff'
    }
    
    df['COLOR'] = df['AÑO'].map(color_map)
    
    return df

def encode_image(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except:
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjMkMzRTUwIi8+Cjx0ZXh0IHg9IjMwIiB5PSIzNSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RVNJUDwvdGV4dD4KPC9zdmc+"

def generate_html():
    print("Cargando datos...")
    df = load_data()
    
    print(f"Datos cargados: {len(df)} registros")
    
    # Convertir datos a formato JSON para JavaScript
    data_json = []
    for _, row in df.iterrows():
        record = {
            'AÑO': int(row['AÑO']),
            'MES': int(row['MES']),
            'MES_NOMBRE': str(row['MES_NOMBRE']),
            'LATITUD': float(row['LATITUD']) if pd.notna(row['LATITUD']) else 0.0,
            'LONGITUD': float(row['LONGITUD']) if pd.notna(row['LONGITUD']) else 0.0,
            'STICKER': str(row['STICKER']) if pd.notna(row['STICKER']) else 'N/A',
            'DIRECCION': str(row['DIRECCION']) if pd.notna(row['DIRECCION']) else 'N/A',
            'FECHA_HURTO': row['FECHA HURTO'].strftime('%d/%m/%Y') if pd.notna(row['FECHA HURTO']) else 'N/A',
            'COLOR': str(row['COLOR'])
        }
        data_json.append(record)
    
    print("Generando archivo HTML portable...")
    
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hurtos Sistema de Alumbrado Público - ESIP SAS ESP</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
        .header {{
            display: flex;
            align-items: center;
            padding: 20px;
            background-color: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        .logo {{
            height: 60px;
            margin-right: 20px;
        }}
        .title {{
            color: #2c3e50;
            margin: 0;
            font-size: 28px;
        }}
        .container {{
            display: flex;
            gap: 20px;
            padding: 20px;
            min-height: calc(100vh - 120px);
        }}
        .sidebar {{
            width: 300px;
            padding: 20px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .main-content {{
            flex: 1;
            padding: 20px;
        }}
        .map-section {{
            margin-bottom: 30px;
        }}
        .charts-section {{
            display: flex;
            gap: 20px;
        }}
        .chart-container {{
            width: 50%;
            padding: 10px;
        }}
        .footer {{
            background-color: #f8f9fa;
            border-top: 1px solid #e9ecef;
            text-align: center;
            color: #6c757d;
            font-size: 12px;
            margin: 0;
            padding: 10px;
        }}
        .filter-section {{
            margin-bottom: 20px;
        }}
        .filter-label {{
            font-weight: bold;
            margin-bottom: 5px;
            display: block;
        }}
        .stats-container {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            font-size: 14px;
        }}
        select, input[type="radio"] {{
            margin-bottom: 20px;
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        h3 {{
            color: #2c3e50;
            margin-bottom: 15px;
            text-align: center;
        }}
        .loading {{
            text-align: center;
            padding: 50px;
            font-size: 18px;
            color: #666;
        }}
        .error {{
            text-align: center;
            padding: 50px;
            font-size: 18px;
            color: #dc3545;
        }}
    </style>
</head>
<body>
    <div class="header">
        <img src="{encode_image('logo_esip_clear.png')}" alt="ESIP Logo" class="logo">
        <h1 class="title">Hurtos Sistema de Alumbrado Público</h1>
    </div>
    
    <div class="container">
        <div class="sidebar">
            <h3>Filtros de Visualización</h3>
            
            <div class="filter-section">
                <label class="filter-label">Seleccionar Años:</label>
                <select id="yearFilter" multiple>
                    <option value="2022" selected>2022</option>
                    <option value="2023" selected>2023</option>
                    <option value="2024" selected>2024</option>
                    <option value="2025" selected>2025</option>
                </select>
            </div>
            
            <div class="filter-section">
                <label class="filter-label">Tipo de Visualización:</label>
                <div>
                    <input type="radio" id="both" name="mapType" value="both" checked>
                    <label for="both">Ambos</label>
                </div>
                <div>
                    <input type="radio" id="points" name="mapType" value="points">
                    <label for="points">Puntos Individuales</label>
                </div>
                <div>
                    <input type="radio" id="heatmap" name="mapType" value="heatmap">
                    <label for="heatmap">Zonas de Calor</label>
                </div>
            </div>
            
            <div class="stats-container">
                <h4>Estadísticas Generales</h4>
                <div id="statsContainer">
                    <div class="loading">Cargando datos...</div>
                </div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="map-section">
                <h3>Distribución Geográfica de Hurtos</h3>
                <div id="mapGraph" style="height: 600px;">
                    <div class="loading">Cargando mapa...</div>
                </div>
            </div>
            
            <div class="charts-section">
                <div class="chart-container">
                    <h3>Distribución por Mes</h3>
                    <div id="monthlyChart" style="height: 400px;">
                        <div class="loading">Cargando gráfico...</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <h3>Distribución por Año</h3>
                    <div id="yearlyChart" style="height: 400px;">
                        <div class="loading">Cargando gráfico...</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Desarrollado por A.V. ESIP SAS ESP. © Todos los Derechos Reservados</p>
    </div>

    <script>
        // Datos de hurtos
        const hurtosData = {json.dumps(data_json, ensure_ascii=False)};
        
        console.log('Datos cargados:', hurtosData.length, 'registros');
        
        // Verificar que Plotly esté disponible
        function checkPlotly() {{
            if (typeof Plotly === 'undefined') {{
                console.error('Plotly no está cargado');
                document.getElementById('mapGraph').innerHTML = '<div class="error">Error: Plotly no se pudo cargar. Verifica tu conexión a internet.</div>';
                document.getElementById('monthlyChart').innerHTML = '<div class="error">Error: Plotly no se pudo cargar.</div>';
                document.getElementById('yearlyChart').innerHTML = '<div class="error">Error: Plotly no se pudo cargar.</div>';
                return false;
            }}
            return true;
        }}
        
        // Función para filtrar datos por años
        function filterDataByYears(years) {{
            return hurtosData.filter(hurto => years.includes(hurto.AÑO));
        }}
        
        // Función para actualizar estadísticas
        function updateStats(selectedYears) {{
            const filteredData = filterDataByYears(selectedYears);
            const totalHurtos = filteredData.length;
            
            const statsByYear = {{}};
            filteredData.forEach(hurto => {{
                statsByYear[hurto.AÑO] = (statsByYear[hurto.AÑO] || 0) + 1;
            }});
            
            let statsHTML = `<p style="font-weight: bold;">Total de Hurtos: ${{totalHurtos.toLocaleString()}}</p><br>`;
            
            Object.entries(statsByYear).forEach(([año, cantidad]) => {{
                statsHTML += `<p>${{año}}: ${{cantidad.toLocaleString()}} hurtos</p>`;
            }});
            
            document.getElementById('statsContainer').innerHTML = statsHTML;
        }}
        
        // Función para actualizar mapa
        function updateMap(selectedYears, mapType) {{
            if (!checkPlotly()) return;
            
            const filteredData = filterDataByYears(selectedYears);
            
            if (filteredData.length === 0) {{
                document.getElementById('mapGraph').innerHTML = '<div class="loading">No hay datos para mostrar</div>';
                return;
            }}
            
            const traces = [];
            
            // Agregar heatmap si está seleccionado
            if (mapType === 'heatmap' || mapType === 'both') {{
                traces.push({{
                    type: 'densitymap',
                    lat: filteredData.map(d => d.LATITUD),
                    lon: filteredData.map(d => d.LONGITUD),
                    z: filteredData.map(() => 1),
                    radius: 20,
                    colorscale: 'Reds',
                    opacity: 0.6,
                    name: 'Zonas de Calor',
                    showscale: true,
                    colorbar: {{
                        title: {{text: "Densidad de Hurtos"}}
                    }}
                }});
            }}
            
            // Agregar puntos individuales si está seleccionado
            if (mapType === 'points' || mapType === 'both') {{
                const colorMap = {{
                    2022: '#8338ec',
                    2023: '#38b000',
                    2024: '#ff006e',
                    2025: '#3a86ff'
                }};
                
                selectedYears.forEach(año => {{
                    const añoData = filteredData.filter(d => d.AÑO === parseInt(año));
                    if (añoData.length > 0) {{
                        traces.push({{
                            type: 'scattermap',
                            lat: añoData.map(d => d.LATITUD),
                            lon: añoData.map(d => d.LONGITUD),
                            mode: 'markers',
                            marker: {{
                                size: 8,
                                color: colorMap[año],
                                opacity: 0.7
                            }},
                            text: añoData.map(d => `${{d.STICKER}}<br>${{d.DIRECCION}}<br>${{d.FECHA_HURTO}}`),
                            hoverinfo: 'text',
                            name: `Año ${{año}}`
                        }});
                    }}
                }});
            }}
            
            const layout = {{
                map: {{
                    style: 'open-street-map',
                    center: {{lat: 2.93, lon: -75.29}},
                    zoom: 12
                }},
                title: "Hurtos Sistema de Alumbrado Público: Enero 2022 - Junio 2025",
                title_x: 0.5,
                margin: {{l: 0, r: 0, t: 50, b: 0}},
                height: 600,
                showlegend: true,
                legend: {{
                    yanchor: "top",
                    y: 0.99,
                    xanchor: "left",
                    x: 0.01
                }}
            }};
            
            try {{
                Plotly.newPlot('mapGraph', traces, layout);
            }} catch (error) {{
                console.error('Error al crear el mapa:', error);
                document.getElementById('mapGraph').innerHTML = '<div class="error">Error al cargar el mapa</div>';
            }}
        }}
        
        // Función para actualizar gráfico mensual
        function updateMonthlyChart(selectedYears) {{
            if (!checkPlotly()) return;
            
            const filteredData = filterDataByYears(selectedYears);
            
            if (filteredData.length === 0) {{
                document.getElementById('monthlyChart').innerHTML = '<div class="loading">No hay datos para mostrar</div>';
                return;
            }}
            
            // Agrupar por mes y año
            const monthlyData = {{}};
            filteredData.forEach(hurto => {{
                const key = `${{hurto.AÑO}}-${{hurto.MES_NOMBRE}}`;
                monthlyData[key] = (monthlyData[key] || 0) + 1;
            }});
            
            const traces = [];
            const colorMap = {{
                2022: '#8338ec',
                2023: '#38b000',
                2024: '#ff006e',
                2025: '#3a86ff'
            }};
            
            selectedYears.forEach(año => {{
                const añoData = Object.entries(monthlyData)
                    .filter(([key]) => key.startsWith(año + '-'))
                    .map(([key, cantidad]) => ({{
                        mes: key.split('-')[1],
                        cantidad: cantidad
                    }}));
                
                if (añoData.length > 0) {{
                    traces.push({{
                        type: 'bar',
                        x: añoData.map(d => d.mes),
                        y: añoData.map(d => d.cantidad),
                        name: `Año ${{año}}`,
                        marker: {{color: colorMap[año]}}
                    }});
                }}
            }});
            
            const layout = {{
                title: "Distribución de Hurtos por Mes",
                xaxis: {{title: "Mes"}},
                yaxis: {{title: "Cantidad de Hurtos"}},
                barmode: 'stack',
                height: 400,
                showlegend: true
            }};
            
            try {{
                Plotly.newPlot('monthlyChart', traces, layout);
            }} catch (error) {{
                console.error('Error al crear el gráfico mensual:', error);
                document.getElementById('monthlyChart').innerHTML = '<div class="error">Error al cargar el gráfico</div>';
            }}
        }}
        
        // Función para actualizar gráfico anual
        function updateYearlyChart(selectedYears) {{
            if (!checkPlotly()) return;
            
            const filteredData = filterDataByYears(selectedYears);
            
            if (filteredData.length === 0) {{
                document.getElementById('yearlyChart').innerHTML = '<div class="loading">No hay datos para mostrar</div>';
                return;
            }}
            
            // Agrupar por año
            const yearlyData = {{}};
            filteredData.forEach(hurto => {{
                yearlyData[hurto.AÑO] = (yearlyData[hurto.AÑO] || 0) + 1;
            }});
            
            const colorMap = {{
                2022: '#8338ec',
                2023: '#38b000',
                2024: '#ff006e',
                2025: '#3a86ff'
            }};
            
            const trace = {{
                type: 'bar',
                x: Object.keys(yearlyData),
                y: Object.values(yearlyData),
                marker: {{
                    color: Object.keys(yearlyData).map(año => colorMap[año])
                }},
                text: Object.values(yearlyData),
                textposition: 'auto'
            }};
            
            const layout = {{
                title: "Distribución de Hurtos por Año",
                xaxis: {{title: "Año"}},
                yaxis: {{title: "Cantidad de Hurtos"}},
                height: 400,
                showlegend: false
            }};
            
            try {{
                Plotly.newPlot('yearlyChart', [trace], layout);
            }} catch (error) {{
                console.error('Error al crear el gráfico anual:', error);
                document.getElementById('yearlyChart').innerHTML = '<div class="error">Error al cargar el gráfico</div>';
            }}
        }}
        
        // Función para actualizar todos los gráficos
        function updateAllCharts() {{
            const selectedYears = Array.from(document.getElementById('yearFilter').selectedOptions).map(option => parseInt(option.value));
            const mapType = document.querySelector('input[name="mapType"]:checked').value;
            
            updateStats(selectedYears);
            updateMap(selectedYears, mapType);
            updateMonthlyChart(selectedYears);
            updateYearlyChart(selectedYears);
        }}
        
        // Event listeners
        document.getElementById('yearFilter').addEventListener('change', updateAllCharts);
        document.querySelectorAll('input[name="mapType"]').forEach(radio => {{
            radio.addEventListener('change', updateAllCharts);
        }});
        
        // Inicializar gráficos cuando la página esté lista
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('Página cargada, inicializando gráficos...');
            setTimeout(() => {{
                if (checkPlotly()) {{
                    updateAllCharts();
                }}
            }}, 2000);
        }});
        
        // Verificar Plotly cada 5 segundos
        setInterval(() => {{
            if (typeof Plotly !== 'undefined' && document.getElementById('mapGraph').innerHTML.includes('Cargando')) {{
                console.log('Plotly detectado, actualizando gráficos...');
                updateAllCharts();
            }}
        }}, 5000);
    </script>
</body>
</html>
"""
    
    # Guardar el archivo HTML
    with open('hurtos_portable_fixed.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("¡Archivo HTML portable mejorado generado exitosamente!")
    print("Archivo: hurtos_portable_fixed.html")
    print("Puedes abrir este archivo en cualquier navegador web sin necesidad de servidor.")

if __name__ == '__main__':
    generate_html() 