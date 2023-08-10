from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import os

app = Flask(__name__)

lista_carrito = []

def cargar_productos():
    ruta_archivo = r'C:\Users\José Gabriel\Documents\calRumba\version 2\productos.json'
    with open(ruta_archivo, 'r') as file:
        return json.load(file)


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
def inicio():
    if request.method == 'POST':
        return redirect(url_for('catalogo'))
    return render_template('index.html')

@app.route('/catalogo', methods=['GET', 'POST'])
def catalogo():
    productos = cargar_productos()
    cotizacion_actual = cotizacion()

    if request.method == 'POST':
        producto_seleccionado = request.form['producto']
        cantidad = int(request.form[producto_seleccionado + '_cantidad'])  # Usamos la clave del producto para acceder a la cantidad

        if producto_seleccionado in productos:
            producto = productos[producto_seleccionado]
            precio_unitario = round(float(producto['price']), 2)
            total_dolar = precio_unitario * cantidad
            total_bs = total_dolar * cotizacion_actual

            # Agregar al carrito
            lista_carrito.append({
                "producto": producto_seleccionado,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "total_dolar": total_dolar,
                "total_bs": total_bs
            })

    return render_template('catalogo.html', catalogo=productos, cotizacion=cotizacion_actual)


@app.route('/carrito', methods=['GET'])
def ver_carrito():
    return render_template('carrito.html', carrito=lista_carrito)


@app.route('/calcular_pago', methods=['POST'])
def calcular_pago():
    num_personas = int(request.form['num_personas'])
    total_dolar = sum(item['total_dolar'] for item in lista_carrito)
    total_bs = sum(item['total_bs'] for item in lista_carrito)
    total_dolar_por_persona = total_dolar / num_personas
    total_bs_por_persona = total_bs / num_personas

    return render_template('pago.html', total_dolar=total_dolar, total_bs=total_bs,
                           total_dolar_por_persona=total_dolar_por_persona, total_bs_por_persona=total_bs_por_persona,
                           num_personas=num_personas)
    

if __name__ == '__main__':
    app.run(debug=True)