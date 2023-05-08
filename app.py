from flask import Flask, jsonify, request
from flask_cors import CORS
from knn import knn_prediction
from knn import *
import json
import pandas as pd
import requests

app = Flask(__name__)

CORS(app)

@app.route('/')
def bienvenida():
    return jsonify({"bienvenida": "hola"})

@app.route("/insertar_datos_paciente/", methods = ['POST'])
def insertar_datos_paciente():

    #Se almacenan los datos de la información obtenida (desde la página web)
    datos_usuario_temporal = []
    datos_usuario = {
        'edad': request.json['edad'],
        'menopausia': request.json['menopausia'],
        'tumorTamaño': request.json['tumorTamaño'],
        'invNodes': request.json['invNodes'],
        'nodesCaps': request.json['nodesCaps'],
        'gradoTumor': request.json['gradoTumor'],
        'breast': request.json['breast'],
        'breastQuead': request.json['breastQuead'],
        'irradiat': request.json['irradiat'],
    }

    datos_usuario_temporal.append(datos_usuario)
    #Se almacenan cada resultado en una variable
    edad = datos_usuario['edad']
    menopausia = datos_usuario['menopausia']
    tumorTamaño = datos_usuario['tumorTamaño']
    invNodes = datos_usuario['invNodes']
    nodesCaps = datos_usuario['nodesCaps']
    gradoTumor = datos_usuario['gradoTumor']
    breast = datos_usuario['breast']
    breastQuead = datos_usuario['breastQuead']
    irradiat = datos_usuario['irradiat']

    #Los datos se convierten a un dataFrame para que pueda ser leído en la predicción
    new_data = pd.DataFrame([[edad, menopausia, tumorTamaño, invNodes, nodesCaps, gradoTumor, breast, breastQuead, irradiat]], columns=['age', 'menopause', 'tumor-size', 'inv-nodes', 'node-caps', 'deg-malig', 'breast', 'breast-quad', 'irradiat'])

    #Se envía la data hacia el archivo que realiza la predicción y se guarda el resultado para luego convertirlo en un string
    resulatdo_prueba_sin_formatear, precision = knn_prediction(new_data)
    #resultado convertido a string
    resultado_prueba = convertir_a_string(resulatdo_prueba_sin_formatear)

    #Una vez obtenido los resultados de la predicción, se almacena dentro de la BD de supabase
    #Se convierte los datos obtenidos en un JSON
    datos_insertar = convertir_a_json(edad, menopausia, tumorTamaño, invNodes, nodesCaps, gradoTumor, breast, breastQuead, irradiat)
    precision_modelo = str(precision)
    #Se envia los datos a la BD y returna el código si fue exitoso el proceso
    code = insertar_resultados_bd(datos_insertar)
    #Se devuelve el resultado de la petición a la página web
    return jsonify({"status": code, "prueba": "xsad", "resultado_prueba": resultado_prueba, "precision": precision_modelo})

# Realizar una solicitud POST a la API de SUPABASE
def insertar_resultados_bd(datos_insertar):
    headers = {
        'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1tcGh6YXl4dnZoZHRydGN2anNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODI2MDY3NDYsImV4cCI6MTk5ODE4Mjc0Nn0.QZWfmiw-KMFgHOTSyxNGFlcOZvDRa305OkZH-YHTzDI',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1tcGh6YXl4dnZoZHRydGN2anNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODI2MDY3NDYsImV4cCI6MTk5ODE4Mjc0Nn0.QZWfmiw-KMFgHOTSyxNGFlcOZvDRa305OkZH-YHTzDI',
        'Content-Type' : 'application/json'
        }

    requests.post('https://mmphzayxvvhdtrtcvjsq.supabase.co/rest/v1/registros_prueba', data = datos_insertar, headers = headers)

    return 201


def convertir_a_string(resulatdo_prueba_sin_formatear):
    res = str(resulatdo_prueba_sin_formatear)
    x = res.replace("[", "")
    y = x.replace("]","")
    return y

def convertir_a_json(edad, menopausia, tumorTamaño, invNodes, nodesCaps, gradoTumor, breast, breastQuead, irradiat):
    datos_json = {
        "age": edad,
        "menopause": menopausia,
        "tumor_size": tumorTamaño,
        "inv_nodes": invNodes,
        "nodes_caps": nodesCaps,
        "deg_malig": gradoTumor,
        "breast": breast,
        "breast_quead": breastQuead,
        "irradiat": irradiat
    }
    datos_insertar = json.dumps(datos_json)
    return datos_insertar

if __name__ == '__main__':
    app.run(debug = True, port = 4000)