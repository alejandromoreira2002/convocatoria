from flask import Flask, render_template, url_for, request, session, jsonify, send_from_directory
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


app = Flask(__name__)

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

@app.post('/preview')
def prevKNN():
    metodo = request.args.get('metodo')
    filename = request.args.get('filename')
    colClase = request.args.get('colClase')
    columnas = request.args.get('columnas').split(',')

    #json_data = request.form.get('data')
    json_data = request.get_json()
    #print(json_data)
    dataCSV = pd.DataFrame(json.loads(json_data))

    # filename = request.form['filename']
    # colClase = request.form['colClase']
    # columnas = request.form['columnas'].split(',')
    
    controladorML = MLController(metodo)
    dfmodel = controladorML.previsualizar(dataCSV, columnas, colClase)

    return dfmodel.to_json(orient='records') 
    #return jsonify({"res": "ok"})

@app.post('/process')
def processData():
    metodo = request.args.get('metodo')
    filename = request.args.get('filename')
    colClase = request.args.get('colClase')
    columnas = request.args.get('columnas').split(',')

    json_data = request.get_json()
    #print(json_data)
    dataCSV = pd.DataFrame(json.loads(json_data))

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
    
@app.post('/file/upload')
def uploadFile():
    df = pd.read_csv(request.files['dataFile'])

    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(port=3000, debug=True, threaded=True, host="0.0.0.0")