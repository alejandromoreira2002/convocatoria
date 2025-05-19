from flask import Flask, render_template, url_for, request, session, jsonify, send_from_directory
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import json
import base64
from models.kmeans_model import KMeansModel
from models.knn_model import KNNModel
from models.arbol_model import RegTreeModel
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
    
    dfmodel = None
    if metodo == "knn":
        knnmodel = KNNModel(dataCSV, columnas, colClase)
        dfmodel = knnmodel.previewData()
    elif metodo == "kmeans":
        kmeansmodel = KMeansModel(dataCSV, columnas, colClase)
        dfmodel = kmeansmodel.previewData()
    elif metodo == "tree":
        rTree = RegTreeModel(dataCSV, columnas, colClase)
        dfmodel = rTree.previewData()
        #print(dfmodel.head())

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

    if metodo == "knn":
        k = int(request.args.get('k'))
        centro = tuple([int(x) for x in request.args.get('centro').split(',')])
        
        knnmodel = KNNModel(dataCSV, columnas, colClase)
        cleandata = knnmodel.previewData()
        encoded_img = knnmodel.resolve(k, centro)

        prediction = knnmodel.prediction

        return jsonify({
            "algType": "knn",
            "filename": filename,
            "cleandata": cleandata.to_json(orient='records'),
            "details": json.dumps({"k": k, "centro": request.form['centro']}),
            "prediction": prediction,
            "plot": encoded_img
        })
    elif metodo == "kmeans":
        n = int(request.args.get('n'))
    
        kmeansmodel = KMeansModel(dataCSV, columnas, colClase)
        cleandata = kmeansmodel.previewData()
        encoded_img = kmeansmodel.resolve(n)
        
        return jsonify({
            "algType": "kmeans",
            "filename": filename,
            "cleandata": cleandata.to_json(orient='records'),
            "details": json.dumps({"n": n}),
            "plot": encoded_img
        }) 
    
    elif metodo == "tree":
        regTreeModel = RegTreeModel(dataCSV, columnas, colClase)
        cleandata = regTreeModel.previewData()
        print(cleandata.head())
        encoded_img = regTreeModel.resolve()
        
        return jsonify({
            "algType": "tree",
            "filename": filename,
            "cleandata": cleandata.to_json(),
            #"details": json.dumps({"n": n}),
            "plot": encoded_img
        })
    
@app.post('/file/upload')
def uploadFile():
    df = pd.read_csv(request.files['dataFile'])

    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(port=3000, debug=True, threaded=True, host="0.0.0.0")