import os
import requests

# Obtener la URL del backend desde las variables de entorno
BACKEND_URL = os.getenv('BACKEND_URL', 'https://microservicioproductos-production.up.railway.app/api')

OTHER_SERVICE_URL = os.getenv('OTHER_SERVICE_URL', 'http://4.203.105.3')

# URL del servicio externo
GRAPHQL_ENDPOINT = os.getenv('GRAPHQL_ENDPOINT', 'http://18.218.15.90:8080/graphql')

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
    
#clientes recurrentes
#http://127.0.0.1:8000/sales/recurring-customers
def get_sales_recurring_customers():
    url = f'{OTHER_SERVICE_URL}/sales/recurring-customers'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for bad response status
        return response.json()["recurring_customers"]  # Assuming 'recurring_customers' is the correct key
    except requests.exceptions.RequestException as e:
        print(f'Error fetching recurring customers: {str(e)}')
        return []  # Return empty list or handle error appropriately
    except KeyError as e:
        print(f'KeyError: {str(e)}')
        return []  # Handle KeyError if necessary
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
        return []  # Handle unexpected errors
    
def get_customer_name(customer_id):
    query = '''
    {
        customer(id: %s) {
            id
            name
        }
    }
    ''' % customer_id

    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': query}, headers=headers)
        if response.status_code == 200:
            return response.json().get('data', {}).get('customer', {}).get('name')
        else:
            print(f'Error: {response.status_code}')
            return None
    except Exception as e:
        print(f'Error: {str(e)}')
        return None
    
