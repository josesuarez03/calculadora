import sys
import requests
import json

def cotizacion():
    base_url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar"

    # Endpoint para obtener información sobre el precio del dólar promedio
    endpoint = "bcv_oficial"

    # Construir la URL completa
    url = f"{base_url}/{endpoint}"

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
            return price
        else:
            print("Error en la solicitud:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)
        return None


def presupuesto(servicio1, servicio2, grupo):
    price = cotizacion()
    if price is None:
        return
    
    print("Servicio\n1. Sin promo (1)\n2. Con Promo(2)\n3. Salir")
    try:
        opcion = int(input("introduce una opcion: "))
        if opcion == 1:
            try:
                n_serv = int(input("introduce la cantidad de servicios a consumir: "))
                total = (servicio1 * n_serv) / grupo
                total_bs = total * price
                print(f"Cada persona debe pagar {total} $ o {total_bs} bs")
            except:
                print('error')
                presupuesto(sin_promo, con_promo, person)
        elif opcion == 2:
            try:
                n_serv = int(input("introduce la cantidad de servicios a consumir: "))
                total = (servicio2 * n_serv) / grupo
                total_bs = total * price
                print(f"Cada persona debe pagar {total} $ o {total_bs} bs")
            except:
                print('error')
                presupuesto(sin_promo, con_promo, person)
        else:
            sys.exit("adios")
    except:
        print("Error")
        presupuesto(sin_promo, con_promo, person)

con_promo = 20
sin_promo = 25

try:
    person = int(input("introducir la cantidad de personas: "))
except:
    print("error")
    sys.exit(1)

presupuesto(sin_promo, con_promo, person)



def index():
    if request.method == 'POST':
        con_promo = 20
        sin_promo = 25

        try:
            person = int(request.form['person'])
            servicio = request.form['servicio']

            if servicio == 'sin_promo':
                servicio_costo = sin_promo
            elif servicio == 'con_promo':
                servicio_costo = con_promo
            else:
                return "Error en el servicio seleccionado."

            grupo = 1  # Actualiza esto según tus necesidades
            price = cotizacion()

            total = (servicio_costo * person) / grupo
            total_bs = total * price

            return render_template('index.html', total_dolar=total, total_bs=total_bs)
        except:
            return "Error en los datos ingresados."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
