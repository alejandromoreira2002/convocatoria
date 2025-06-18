from flask import Flask, render_template, url_for, request, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import json
import base64
from controllers.ml_controller import MLController
#import json
#import os
#from dotenv import load_dotenv
#import requests
#import random
#import string

#load_dotenv(os.path.join(os.getcwd(), '.env'))

#cargar variables globales


#cargar controladores
max_registros = 1000

app = Flask(__name__)
app.config['TEMP_FOLDER'] = os.path.join(os.getcwd(), 'temp')

with app.test_request_context():
    url_for('static', filename='/css/')
    url_for('static', filename='/js/')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('static', filename)

@app.get('/')
def Index():
    return render_template('index.html')

@app.post('/prueba')
def prueba():
    f = request.files['file-upload']
    f.save('./uploads/temp_file.csv')
    
    return {'filename': f.filename}

@app.get('/preview')
def previewData():
    metodo = request.args.get('metodo')
    filename = request.args.get('filename')
    columnas = request.args.get('columnas').split(',')
    colClase = None

    if 'colClase' in request.args:
        colClase = request.args.get('colClase')

    ruta_archivo = os.path.join(app.config['TEMP_FOLDER'], filename)
    dataCSV = pd.read_csv(ruta_archivo)
    #print(json_data)
    #dataCSV = pd.DataFrame(json.loads(json_data))

    limite = 1000
    if dataCSV.shape[0] < limite:
        limite = dataCSV.shape[0]
    
    dataCSV = dataCSV[:limite]

    # filename = request.form['filename']
    # colClase = request.form['colClase']
    # columnas = request.form['columnas'].split(',')
    
    controladorML = MLController(metodo)
    dfmodel = controladorML.previsualizar(dataCSV, columnas, colClase)

    return dfmodel.to_json(orient='records') 
    #return jsonify({"res": "ok"})

@app.get('/process')
def processData():
    metodo = request.args.get('metodo')
    filename = request.args.get('filename')
    columnas = request.args.get('columnas').split(',')
    colClase = None

    if 'colClase' in request.args:
        colClase = request.args.get('colClase')

    #json_data = request.get_json()
    #print(json_data)
    ruta_archivo = os.path.join(app.config['TEMP_FOLDER'], filename)
    dataCSV = pd.read_csv(ruta_archivo)
    #dataCSV = pd.DataFrame(json.loads(json_data))

    print(metodo)
    print(filename)
    print(colClase)
    print(columnas)
    print(dataCSV.head())

    # metodo = request.args.get('metodo')
    # json_data = request.form.get('data')
    # dataCSV = pd.DataFrame(json.loads(json_data))

    # filename = request.form['filename']
    # colClase = request.form['colClase']
    # columnas = request.form['columnas'].split(',')

    controladorML = MLController(metodo)
    resultado = controladorML.procesar(dataCSV, columnas, colClase, request.args)
    resultado['filename'] = filename
    return jsonify(resultado)

@app.post('/file/read')
def readFile():
    archivo = request.form.get('filename')
    pagina = 0
    if 'pagina' in request.args:
        pagina = int(request.args.get('pagina'))-1
    
    ruta_archivo = os.path.join(app.config['TEMP_FOLDER'], archivo)
    df = pd.read_csv(ruta_archivo)
    num_filas = df.shape[0]

    inicio = pagina * max_registros
    fin = inicio + max_registros
    limite = num_filas if fin > num_filas else fin

    df = df[inicio:limite]

    return df.to_json(orient='records')

@app.post('/file/upload')
def uploadFile():
    resultado = {
        "ok": False,
        "datos": None,
        "observacion": None
    }
    
    if 'dataFile' not in request.files:
        resultado['observacion'] = 'No se encontró el campo de archivo'
        return jsonify(resultado), 400

    file = request.files.get('dataFile')
    if not file or file.filename == '':
        resultado['observacion'] = 'No hay archivo seleccionado.'
        return jsonify(resultado), 400
    
    
    fname = secure_filename(file.filename)
    dest = os.path.join(app.config['TEMP_FOLDER'], fname)
    file.save(dest)

    numero = pd.read_csv(dest).shape[0]
    print(numero)
    paginas = int(pd.read_csv(dest).shape[0]) // max_registros

    resultado['ok'] = True
    resultado['datos'] = {"nombre_archivo": fname, "paginas": paginas}

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(port=3000, debug=True, threaded=True, host="0.0.0.0")