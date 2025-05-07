import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Cargar el archivo CSV
df = pd.read_csv('Hurtos_marzo.csv')

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Configuración del servidor
server = app.server

# Layout del tablero
app.layout = html.Div([
    html.Div([
        html.H1("Tablero de Hurtos de Luminarias ESIP 2022-2025", style={'textAlign': 'center'}),
        
        # Filtro de año
        html.Div([
            html.Label("Seleccione el año:", style={'fontSize': '20px', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in df['AÑO'].unique()],
                value=[df['AÑO'].unique()[0]],
                multi=True,
                clearable=False,
                style={'width': '100%', 'marginBottom': '20px'}
            ),
        ], style={'width': '100%', 'padding': '10px'}),

        # Gráficos
        html.Div([
            dcc.Graph(id='bar-chart'),
            dcc.Graph(id='map', style={'height': '600px'})
        ], style={'width': '100%', 'padding': '10px'}),

        # Tabla centrada
        html.Div([
            html.H3("Detalle de Hurtos", style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Div(id='year-table-container', style={'display': 'flex', 'justifyContent': 'center'})
        ], style={'width': '100%', 'padding': '10px'})
    ], style={'paddingBottom': '50px'}),

    # Footer
    html.Div(
        "© 2025 - ESIP SAS ESP - Todos los derechos Reservados- Desarrollado por Alejandra Valderrama",
        style={
            'position': 'fixed',
            'bottom': '10px',
            'right': '20px',
            'color': '#555',
            'fontSize': '14px',
            'backgroundColor': 'rgba(255, 255, 255, 0.7)',
            'padding': '5px 10px',
            'borderRadius': '5px'
        }
    )
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('map', 'figure'),
     Output('year-table-container', 'children')],
    [Input('year-dropdown', 'value')]
)
def update_graphs(selected_years):
    filtered_df = df[df['AÑO'].isin(selected_years)]
    
    # Gráfico de barras
    bar_fig = px.bar(
        filtered_df,
        x='Mes',
        y='Farola',
        title='Hurtos de Luminarias por Mes',
        color='AÑO',
        barmode='group'
    )
    
    # Mapa usando scattermap (versión actualizada)
    map_fig = go.Figure()
    if 'Latitud' in filtered_df.columns and 'Longitud' in filtered_df.columns:
        for year in selected_years:
            year_df = filtered_df[filtered_df['AÑO'] == year]
            valid_coords = year_df.dropna(subset=['Latitud', 'Longitud'])
            map_fig.add_trace(go.Scattermapbox(
                lat=valid_coords['Latitud'],
                lon=valid_coords['Longitud'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=px.colors.qualitative.Plotly[selected_years.index(year) % len(px.colors.qualitative.Plotly)]
                ),
                name=str(year),
                hovertext=valid_coords['Farola'],
                hovertemplate="<b>Año:</b> %{name}<br>" +
                             "<b>Cantidad:</b> %{hovertext}<br>" +
                             "<b>Latitud:</b> %{lat:.4f}<br>" +
                             "<b>Longitud:</b> %{lon:.4f}<extra></extra>"
            ))
    
    # Configuración del mapa
    map_fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(
                lat=filtered_df['Latitud'].mean() if not filtered_df['Latitud'].isnull().all() else 4.6097,
                lon=filtered_df['Longitud'].mean() if not filtered_df['Longitud'].isnull().all() else -74.0817
            ),
            zoom=10
        ),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        uirevision=True,
        dragmode='zoom'
    )

    # Tabla: conteo de hurtos por año
    year_count = filtered_df.groupby('AÑO').size().reset_index(name='Cantidad de Hurtos')
    table = dash_table.DataTable(
        columns=[
            {'name': 'Año', 'id': 'AÑO', 'type': 'numeric'},
            {'name': 'Cantidad de Hurtos', 'id': 'Cantidad de Hurtos', 'type': 'numeric'}
        ],
        data=year_count.to_dict('records'),
        style_table={
            'width': '400px',
            'margin': '0 auto',
            'boxShadow': '0 0 10px rgba(0,0,0,0.1)',
            'borderRadius': '10px'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '12px',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '16px',
            'border': '1px solid #ddd'
        },
        style_header={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'padding': '12px',
            'fontSize': '18px'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        page_size=10
    )
    return bar_fig, map_fig, table

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))