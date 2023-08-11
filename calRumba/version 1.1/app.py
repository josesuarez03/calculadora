from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from flask_cors import CORS

app = Flask(__name__)
app.static_folder = 'static'
CORS(app)

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
def home():
    if request.method == 'POST':
        if 'calculadora_rumba' in request.form:
            return redirect(url_for('calculadora_rumba'))
        elif 'calculadora_pagos' in request.form:
            return redirect(url_for('calculadora_pagos'))
        elif 'dolarbs' in request.form:
            return redirect(url_for('dolarbs'))
    
    return render_template('index.html')

@app.route('/calculadora-pagos', methods=['GET', 'POST'])
def calculadora_pagos():
    if request.method == 'POST':

        try:
            people = int(request.form['person'])
            coste = int(request.form['coste'])

            price = cotizacion()
            total = coste / people
            total_bs = total * price

            return render_template('calculadoraPagos.html', total_dolar=total, total_bs=total_bs)
        except:
            return "Error en los datos ingresados."

    return render_template('calculadoraPagos.html')


@app.route('/calculadora-rumba', methods=['GET', 'POST'])
def calculadora_rumba():
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

            return render_template('calculadoraRumba.html', total_dolar=total, total_bs=total_bs)
        except:
            return "Error en los datos ingresados."

    return render_template('calculadoraRumba.html')



@app.route('/limpiar-1', methods=['GET', 'POST'])
def limpiar_1():
    if request.method == 'GET':
        return render_template('calculadoraRumba.html', total_dolar=None, total_bs=None)
    else:
        return redirect(url_for('calculadora_rumba'))

@app.route('/limpiar-2', methods=['GET', 'POST'])
def limpiar_2():
    if request.method == 'GET':
        return render_template('calculadoraPagos.html', total_dolar=None, total_bs=None)
    else:
        return redirect(url_for('calculadora_pagos'))
    
@app.route('/preciodolarbs', methods=['GET','POST'])
def dolarbs():
    if request.method == 'POST':
        try:
            price = cotizacion()
            return render_template('preciodolar.html', precio_dolar=price)
        except:
            return "Error al obtener la información"
    return render_template('preciodolar.html')


if __name__ == '__main__':
    app.run(debug=True)
