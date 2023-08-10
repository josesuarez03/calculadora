from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

app = Flask(__name__)

def cotizacion():
    base_url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar"

    endpoint = "bcv_oficial"
    url = f"{base_url}/{endpoint}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            bcv_dollar = data['bcv']
            price = float(bcv_dollar['price'])
            return price
        else:
            print("Error en la solicitud:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error en la solicitud:", e)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        con_promo = 20
        sin_promo = 25

        try:
            person = int(request.form['person'])
            cantidad_servicio = int(request.form['cantidad_servicio'])
            servicio = request.form['servicio']

            if servicio == 'sin_promo':
                servicio_costo = sin_promo
            elif servicio == 'con_promo':
                servicio_costo = con_promo
            else:
                return "Error en el servicio seleccionado."

            price = cotizacion()
            total = (servicio_costo * cantidad_servicio) / person
            total_bs = total * price

            return render_template('index.html', total_dolar=total, total_bs=total_bs)
        except:
            return "Error en los datos ingresados."

    return render_template('index.html')

@app.route('/limpiar', methods=['GET', 'POST'])
def limpiar():
    if request.method == 'GET':
        return render_template('index.html', total_dolar=None, total_bs=None)
    else:
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
