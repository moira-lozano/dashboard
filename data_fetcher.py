import os
import requests

# Obtener la URL del backend desde las variables de entorno
BACKEND_URL = os.getenv('BACKEND_URL', 'https://microservicioproductos-production.up.railway.app/api')

OTHER_SERVICE_URL = os.getenv('OTHER_SERVICE_URL', 'http://4.203.105.3')

def get_sales_by_year():
    url = f'{OTHER_SERVICE_URL}/sales/total-sales-by-year'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["total_sales_by_year"]
    else:
        print(f'Error: {response.status_code}')
        return []

def get_sales_by_month(year):
    url = f'{OTHER_SERVICE_URL}/sales/total-sales-by-month/{year}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["total_sales_by_month"]
    else:
        print(f'Error: {response.status_code}')
        return []

def get_sales_by_date_range(start_date, end_date):
    url = f'{OTHER_SERVICE_URL}/sales/total-sales-by-date-range'
    params = {'start_date': start_date, 'end_date': end_date}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return {}
    
#clientes recurrentes
#http://127.0.0.1:8000/sales/recurring-customers
def get_sales_recurring_custoners():
    url = f'{OTHER_SERVICE_URL}/sales/recurring-customers'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["total_sales_recurring_customers"]
    else:
        print(f'Error: {response.status_code}')
        return []


def get_products_by_sizes():
    url = f"{BACKEND_URL}/producto/masCompradosPorTalla"  
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return []
    
def get_products_by_model():
    url = f"{BACKEND_URL}/producto/porModelo" 
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return []
    
def get_products_by_color():
    url = f"{BACKEND_URL}/producto/porColor" 
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return []
    
def get_products_by_brand():
    url = f"{BACKEND_URL}/producto/porMarca" 
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return []
    
def get_products_by_promotion():
    url = f"{BACKEND_URL}/producto/productosConPromo" 
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return []
    
