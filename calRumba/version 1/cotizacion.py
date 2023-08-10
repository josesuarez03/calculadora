import requests
import json

# URL base de la API
base_url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar"

# Endpoint para obtener información sobre el precio del dólar promedio
endpoint = "bcv_oficial"

# Construir la URL completa
url = f"{base_url}/{endpoint}"

precio_a_multiplicar = 50

try:
    # Realizar la solicitud GET a la API
    response = requests.get(url)
    
    # Verificar el código de estado de la respuesta
    if response.status_code == 200:
        data = response.json()  # Convertir la respuesta JSON en un objeto Python

        bcv_dollar = data['bcv']
        price = float(bcv_dollar['price'])  

        
        # Guardar los datos en un archivo JSON
        with open('dolar.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        
        print("Información del precio del dólar promedio en Venezuela guardada en 'dolar.json'")
    else:
        print("Error en la solicitud:", response.status_code)
except requests.exceptions.RequestException as e:
    print("Error en la solicitud:", e)

