from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from knn import knn_prediction
from knn import *

app = Flask(__name__)

CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'breast_cancer' #nombre de la BD
mysql = MySQL(app)

@app.route('/')
def bienvenida():
    return jsonify({"bienvenida": "hola"})

@app.route("/insertar_datos_paciente/", methods = ['POST'])
def insertar_datos_paciente():

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

    edad = datos_usuario['edad']
    menopausia = datos_usuario['menopausia']
    tumorTamaño = datos_usuario['tumorTamaño']
    invNodes = datos_usuario['invNodes']
    nodesCaps = datos_usuario['nodesCaps']
    gradoTumor = datos_usuario['gradoTumor']
    breast = datos_usuario['breast']
    breastQuead = datos_usuario['breastQuead']
    irradiat = datos_usuario['irradiat']

    print(datos_usuario)

    new_data = pd.DataFrame([[edad, menopausia, tumorTamaño, invNodes, nodesCaps, gradoTumor, breast, breastQuead, irradiat]], columns=['age', 'menopause', 'tumor-size', 'inv-nodes', 'node-caps', 'deg-malig', 'breast', 'breast-quad', 'irradiat'])

    print(new_data)

    #Llamamos a la función knn_prediction del archivo knvecinos.py
    resultado = knn_prediction(new_data)
    res = str(resultado)

    print(res)

    #cur = mysql.connection.cursor()
    #cur.execute("INSERT INTO informacion_paciente (age, menopause, tumor_size, inv_nodes, nodes_caps, deg_malig, breast, breast_quead, irradiat) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (edad, menopausia, tumorTamaño, invNodes, nodesCaps, gradoTumor, breast, breastQuead, irradiat))
    #cur.close()

    #mysql.connection.commit()
    #print("Datos añadidos a la BD ")
    return jsonify({
        "informacion":res})


if __name__ == '__main__':
    app.run(debug = True, port = 4000)