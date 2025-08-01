import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import base64
import os

# Configurar la aplicación Dash para exportación estática
app = dash.Dash(__name__, 
                title="Hurtos Sistema de Alumbrado Público - ESIP SAS ESP",
                suppress_callback_exceptions=True)

# Variable server para Render
server = app.server

# Cargar y procesar los datos
def load_data():
    df = pd.read_csv('Bd_hurtos_06_2025_v1.csv')
    
    # Limpiar nombres de columnas (eliminar espacios)
    df.columns = df.columns.str.strip()
    
    # Convertir fecha a datetime con manejo de múltiples formatos
    def parse_date(date_str):
        if pd.isna(date_str) or date_str == '':
            return pd.NaT
        
        # Intentar diferentes formatos (priorizar formato americano M/D/YYYY)
        formats = ['%m/%d/%Y', '%d/%m/%Y', '%m/%d/%y', '%d/%m/%y']
        
        for fmt in formats:
            try:
                parsed_date = pd.to_datetime(date_str, format=fmt)
                # Validar que la fecha sea razonable
                if parsed_date.year >= 2020 and parsed_date.year <= 2025:
                    return parsed_date
            except:
                continue
        
        return pd.NaT
    
    df['FECHA HURTO'] = df['FECHA HURTO'].apply(parse_date)
    
    # Filtrar solo registros con fechas válidas
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

# Cargar datos
df = load_data()

# Codificar logo en base64
def encode_image(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except:
        # Si no encuentra el logo, usar un placeholder
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjMkMzRTUwIi8+Cjx0ZXh0IHg9IjMwIiB5PSIzNSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSJ3aGl0ZSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RVNJUDwvdGV4dD4KPC9zdmc+"

# Layout de la aplicación
app.layout = html.Div([
    # Header con logo
    html.Div([
        html.Img(src=encode_image('logo_esip_clear.png'), 
                style={'height': '60px', 'marginRight': '20px'}),
        html.H1("Hurtos Sistema de Alumbrado Público", 
                style={'color': '#2c3e50', 'margin': '0', 'fontSize': '28px'}),
    ], style={'display': 'flex', 'alignItems': 'center', 'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderBottom': '2px solid #e9ecef'}),
    
    # Contenedor principal
    html.Div([
        # Panel de control
        html.Div([
            html.H3("Filtros de Visualización", style={'color': '#2c3e50', 'marginBottom': '15px'}),
            html.Label("Seleccionar Años:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='year-filter',
                options=[
                    {'label': '2022', 'value': 2022},
                    {'label': '2023', 'value': 2023},
                    {'label': '2024', 'value': 2024},
                    {'label': '2025', 'value': 2025}
                ],
                value=[2022, 2023, 2024, 2025],
                multi=True,
                style={'marginBottom': '20px'}
            ),
            html.Label("Tipo de Visualización:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
            dcc.RadioItems(
                id='map-type',
                options=[
                    {'label': 'Puntos Individuales', 'value': 'points'},
                    {'label': 'Zonas de Calor', 'value': 'heatmap'},
                    {'label': 'Ambos', 'value': 'both'}
                ],
                value='both',
                style={'marginBottom': '20px'}
            ),
            html.Div([
                html.H4("Estadísticas Generales", style={'color': '#2c3e50', 'marginBottom': '10px'}),
                html.Div(id='stats-container', style={'fontSize': '14px'})
            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px'})
        ], style={'width': '300px', 'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'}),
        
        # Contenido principal
        html.Div([
            # Mapa
            html.Div([
                html.H3("Distribución Geográfica de Hurtos", 
                        style={'color': '#2c3e50', 'marginBottom': '15px', 'textAlign': 'center'}),
                dcc.Graph(
                    id='map-graph',
                    style={'height': '600px'},
                    config={'displayModeBar': True, 'scrollZoom': True}
                )
            ], style={'marginBottom': '30px'}),
            
            # Gráficos
            html.Div([
                html.Div([
                    html.H3("Distribución por Mes", 
                            style={'color': '#2c3e50', 'marginBottom': '15px', 'textAlign': 'center'}),
                    dcc.Graph(
                        id='monthly-chart',
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'padding': '10px'}),
                
                html.Div([
                    html.H3("Distribución por Año", 
                            style={'color': '#2c3e50', 'marginBottom': '15px', 'textAlign': 'center'}),
                    dcc.Graph(
                        id='yearly-chart',
                        style={'height': '400px'}
                    )
                ], style={'width': '50%', 'padding': '10px'})
            ], style={'display': 'flex', 'gap': '20px'})
        ], style={'flex': '1', 'padding': '20px'})
    ], style={'display': 'flex', 'gap': '20px', 'padding': '20px', 'backgroundColor': '#f5f5f5', 'minHeight': 'calc(100vh - 120px)'}),
    
    # Footer
    html.Div([
        html.P("Desarrollado por A.V. ESIP SAS ESP. © Todos los Derechos Reservados", 
               style={'textAlign': 'center', 'color': '#6c757d', 'fontSize': '12px', 'margin': '0', 'padding': '10px'})
    ], style={'backgroundColor': '#f8f9fa', 'borderTop': '1px solid #e9ecef'})
], style={'fontFamily': 'Arial, sans-serif'})

# Callback para actualizar estadísticas
@callback(
    Output('stats-container', 'children'),
    Input('year-filter', 'value')
)
def update_stats(selected_years):
    if not selected_years:
        return html.Div("Seleccione al menos un año")
    
    filtered_df = df[df['AÑO'].isin(selected_years)]
    
    total_hurtos = len(filtered_df)
    total_por_año = filtered_df['AÑO'].value_counts().to_dict()
    
    stats_html = [
        html.P(f"Total de Hurtos: {total_hurtos:,}", style={'fontWeight': 'bold'}),
        html.Br()
    ]
    
    for año, cantidad in total_por_año.items():
        stats_html.append(html.P(f"{año}: {cantidad:,} hurtos"))
    
    return html.Div(stats_html)

# Callback para actualizar el mapa
@callback(
    Output('map-graph', 'figure'),
    [Input('year-filter', 'value'),
     Input('map-type', 'value')]
)
def update_map(selected_years, map_type):
    if not selected_years:
        return go.Figure()
    
    filtered_df = df[df['AÑO'].isin(selected_years)]
    
    # Crear figura del mapa
    fig = go.Figure()
    
    # Agregar heatmap si está seleccionado
    if map_type in ['heatmap', 'both']:
        fig.add_trace(go.Densitymap(
            lat=filtered_df['LATITUD'],
            lon=filtered_df['LONGITUD'],
            z=[1] * len(filtered_df),  # Valor constante para densidad
            radius=20,
            colorscale='Reds',
            opacity=0.6,
            name='Zonas de Calor',
            showscale=True,
            colorbar=dict(
                title=dict(text="Densidad de Hurtos")
            )
        ))
    
    # Agregar puntos individuales si está seleccionado
    if map_type in ['points', 'both']:
        for año in selected_years:
            año_data = filtered_df[filtered_df['AÑO'] == año]
            
            if len(año_data) > 0:
                fig.add_trace(go.Scattermap(
                    lat=año_data['LATITUD'],
                    lon=año_data['LONGITUD'],
                    mode='markers',
                    marker=go.scattermap.Marker(
                        size=8,
                        color=año_data['COLOR'].iloc[0],
                        opacity=0.7
                    ),
                    text=año_data['STICKER'] + '<br>' + 
                         año_data['DIRECCION'] + '<br>' + 
                         año_data['FECHA HURTO'].dt.strftime('%d/%m/%Y'),
                    hoverinfo='text',
                    name=f'Año {año}'
                ))
    
    # Configurar el mapa
    fig.update_layout(
        map=dict(
            style='open-street-map',
            center=dict(lat=2.93, lon=-75.29),  # Centro en Neiva
            zoom=12
        ),
        title="Hurtos Sistema de Alumbrado Público: Enero 2022 - Junio 2025",
        title_x=0.5,
        margin=dict(l=0, r=0, t=50, b=0),
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

# Callback para actualizar gráfico mensual
@callback(
    Output('monthly-chart', 'figure'),
    Input('year-filter', 'value')
)
def update_monthly_chart(selected_years):
    if not selected_years:
        return go.Figure()
    
    filtered_df = df[df['AÑO'].isin(selected_years)]
    
    # Agrupar por mes y año
    monthly_data = filtered_df.groupby(['AÑO', 'MES_NOMBRE', 'MES']).size().reset_index(name='CANTIDAD')
    monthly_data = monthly_data.sort_values(['AÑO', 'MES'])
    
    # Crear gráfico de barras apiladas
    fig = go.Figure()
    
    for año in selected_years:
        año_data = monthly_data[monthly_data['AÑO'] == año]
        
        if len(año_data) > 0:
            fig.add_trace(go.Bar(
                x=año_data['MES_NOMBRE'],
                y=año_data['CANTIDAD'],
                name=f'Año {año}',
                marker_color=año_data['AÑO'].map({2022: '#8338ec', 2023: '#38b000', 2024: '#ff006e', 2025: '#3a86ff'}).iloc[0]
            ))
    
    fig.update_layout(
        title="Distribución de Hurtos por Mes",
        xaxis_title="Mes",
        yaxis_title="Cantidad de Hurtos",
        barmode='stack',
        height=400,
        showlegend=True
    )
    
    return fig

# Callback para actualizar gráfico anual
@callback(
    Output('yearly-chart', 'figure'),
    Input('year-filter', 'value')
)
def update_yearly_chart(selected_years):
    if not selected_years:
        return go.Figure()
    
    filtered_df = df[df['AÑO'].isin(selected_years)]
    
    # Agrupar por año
    yearly_data = filtered_df['AÑO'].value_counts().reset_index()
    yearly_data.columns = ['AÑO', 'CANTIDAD']
    yearly_data = yearly_data.sort_values('AÑO')
    
    # Crear gráfico de barras
    fig = go.Figure(data=[
        go.Bar(
            x=yearly_data['AÑO'],
            y=yearly_data['CANTIDAD'],
            marker_color=[df[df['AÑO'] == año]['COLOR'].iloc[0] for año in yearly_data['AÑO']],
            text=yearly_data['CANTIDAD'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="Distribución de Hurtos por Año",
        xaxis_title="Año",
        yaxis_title="Cantidad de Hurtos",
        height=400,
        showlegend=False
    )
    
    return fig

if __name__ == '__main__':
    # Generar el archivo HTML estático
    print("Generando archivo HTML portable...")
    
    # Crear el HTML con todos los datos embebidos
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
                <div id="statsContainer"></div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="map-section">
                <h3>Distribución Geográfica de Hurtos</h3>
                <div id="mapGraph" style="height: 600px;"></div>
            </div>
            
            <div class="charts-section">
                <div class="chart-container">
                    <h3>Distribución por Mes</h3>
                    <div id="monthlyChart" style="height: 400px;"></div>
                </div>
                
                <div class="chart-container">
                    <h3>Distribución por Año</h3>
                    <div id="yearlyChart" style="height: 400px;"></div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Desarrollado por A.V. ESIP SAS ESP. © Todos los Derechos Reservados</p>
    </div>

    <script>
        // Datos de hurtos (convertidos a JavaScript)
        const hurtosData = {df.to_dict('records')};
        
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
            const filteredData = filterDataByYears(selectedYears);
            
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
                    const añoData = filteredData.filter(d => d.AÑO === año);
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
            
            Plotly.newPlot('mapGraph', traces, layout);
        }}
        
        // Función para actualizar gráfico mensual
        function updateMonthlyChart(selectedYears) {{
            const filteredData = filterDataByYears(selectedYears);
            
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
            
            Plotly.newPlot('monthlyChart', traces, layout);
        }}
        
        // Función para actualizar gráfico anual
        function updateYearlyChart(selectedYears) {{
            const filteredData = filterDataByYears(selectedYears);
            
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
            
            Plotly.newPlot('yearlyChart', [trace], layout);
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
        
        // Inicializar gráficos
        updateAllCharts();
    </script>
</body>
</html>
"""
    
    # Guardar el archivo HTML
    with open('hurtos_portable.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("¡Archivo HTML portable generado exitosamente!")
    print("Archivo: hurtos_portable.html")
    print("Puedes abrir este archivo en cualquier navegador web sin necesidad de servidor.")
    
    # También ejecutar la aplicación normal si se desea
    app.run(debug=True, host='127.0.0.1', port=8050) 