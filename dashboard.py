import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px
import pandas as pd 
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__)

# Función para obtener los datos de ventas por año
def get_sales_by_year():
    url = 'http://4.203.105.3/sales/total-sales-by-year'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["total_sales_by_year"]
    else:
        print(f'Error: {response.status_code}')
        return []

# Función para obtener los datos de ventas por mes de un año específico
def get_sales_by_month(year):
    url = f'http://4.203.105.3/sales/total-sales-by-month/{year}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["total_sales_by_month"]
    else:
        print(f'Error: {response.status_code}')
        return []

# Función para obtener los datos de ventas por rango de fechas
def get_sales_by_date_range(start_date, end_date):
    url = 'http://4.203.105.3/sales/total-sales-by-date-range'
    params = {'start_date': start_date, 'end_date': end_date}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return {}

# Obtener datos iniciales
sales_by_year = get_sales_by_year()

# Layout de la aplicación Dash
app.layout = html.Div(children=[
    html.Div([
        html.H1(children='DASHBOARD DE VENTAS'),
        html.P('SELECCIONA LAS VENTAS', className='fix_label', style={'color':'black', 'margin-top': '2px'}),
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}),  # Centrar los elementos y agregar margen inferior

    html.Div([
        dcc.RadioItems(
            id='ventas-radioitems',
            labelStyle={'display': 'inline-block'},
            options=[
                {'label': 'Ventas totales por año', 'value': 'ventas_totales_año'},
                {'label': 'Ventas totales por mes', 'value': 'ventas_totales_mes'},
                {'label': 'Ventas totales por rango de fechas', 'value': 'ventas_totales_fecha'}
            ],
            value='ventas_totales_año',
            style={'text-align': 'center', 'color': 'black'},
            className='dcc_compon'
        ),
    ], className='create_container2 five columns', style={'margin-bottom': '20px', 'textAlign': 'center'}),

    html.Div(id='controls-container', style={'textAlign': 'center', 'margin-bottom': '20px'}, children=[
        html.Div([
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': str(year['year']), 'value': year['year']} for year in sales_by_year],
                value=sales_by_year[0]['year'] if sales_by_year else None
            ),
        ], id='year-dropdown-container', style={'display': 'none', 'margin': '0 auto', 'width': '50%'}),  # Centrando el Dropdown

        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=pd.to_datetime('2023-01-01'),
                end_date=pd.to_datetime('2023-12-31'),
                display_format='YYYY-MM-DD',
                style={'margin-bottom': '20px', 'margin': '0 auto'}
            ),
        ], id='date-picker-container', style={'display': 'none', 'textAlign': 'center'}),  # Centrando el DatePickerRange
    ]),

    dcc.Graph(
        id='sales-graph'
    )
])

# Callback para actualizar el gráfico basado en la selección del usuario
@app.callback(
    [Output('sales-graph', 'figure'),
     Output('year-dropdown-container', 'style'),
     Output('date-picker-container', 'style')],
    [Input('ventas-radioitems', 'value'),
     Input('year-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(selected_option, selected_year, start_date, end_date):
    if selected_option == 'ventas_totales_año':
        sales_by_year = get_sales_by_year()
        df_year = pd.DataFrame(sales_by_year)
        fig = px.bar(df_year, x='year', y='total_sales', title='Total de Ventas por Año',
                     labels={'year': 'Año', 'total_sales': 'Total de Ventas'},
                     text_auto=True)
        min_total_sales = df_year['total_sales'].min()
        fig.update_layout(yaxis=dict(range=[min_total_sales, df_year['total_sales'].max()]))
        return fig, {'display': 'none'}, {'display': 'none'}
    
    elif selected_option == 'ventas_totales_mes':
        if selected_year is None:
            return {}, {'display': 'block', 'textAlign': 'center'}, {'display': 'none'}
        sales_by_month = get_sales_by_month(selected_year)
        df_month = pd.DataFrame(sales_by_month)
        fig = px.bar(df_month, x='month', y='total_sales', title=f'Total de Ventas por Mes del {selected_year}',
                     labels={'month': 'Mes', 'total_sales': 'Total de Ventas'},
                     text_auto=True)
        return fig, {'display': 'block', 'textAlign': 'center'}, {'display': 'none'}
    
    elif selected_option == 'ventas_totales_fecha':
        if start_date is None or end_date is None:
            return {}, {'display': 'none'}, {'display': 'block', 'textAlign': 'center'}
        sales_by_date_range = get_sales_by_date_range(start_date, end_date)
        
        # Debug print to check the data format
        print(f'Sales by date range data: {sales_by_date_range}')
        
        # Check if data is in the correct format
        if isinstance(sales_by_date_range, dict) and 'total_sales_by_date_range' in sales_by_date_range:
            total_sales = sales_by_date_range['total_sales_by_date_range']['total_sales']
            df_date_range = pd.DataFrame([{'date': f'{start_date} to {end_date}', 'total_sales': total_sales}])
            fig = px.bar(df_date_range, x='date', y='total_sales', title=f'Total de Ventas desde {start_date} hasta {end_date}',
                         labels={'date': 'Fecha', 'total_sales': 'Total de Ventas'},
                         text_auto=True)
            return fig, {'display': 'none'}, {'display': 'block', 'textAlign': 'center'}
        else:
            print('Error: Unexpected data format')
            return {}, {'display': 'none'}, {'display': 'block', 'textAlign': 'center'}

if __name__ == '__main__':
    app.run_server(debug=True)
