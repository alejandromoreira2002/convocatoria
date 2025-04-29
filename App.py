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
        rTree = KMeansModel(dataCSV, columnas, colClase)
        dfmodel = rTree.previewData()
        #print(dfmodel.head())

    return dfmodel.to_json(orient='records') 
    #return jsonify({"res": "ok"})

@app.post('/process')
def processKNN():
    metodo = request.args.get('metodo')
    json_data = request.form.get('data')
    dataCSV = pd.DataFrame(json.loads(json_data))

    filename = request.form['filename']
    colClase = request.form['colClase']
    columnas = request.form['columnas'].split(',')

    if metodo == "knn":
        k = int(request.form['k'])
        centro = tuple([int(x) for x in request.form['centro'].split(',')])
        
        knnmodel = KNNModel(dataCSV, columnas, colClase)
        cleandata = knnmodel.previewData()
        fig = knnmodel.resolve(k, centro)

        img_data = BytesIO()
        fig.savefig(img_data, format='png')
        img_data.seek(0)
        fig.close()

        encoded_img = base64.b64encode(img_data.read()).decode('utf-8')
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
        n = int(request.form['n'])
    
        kmeansmodel = KMeansModel(dataCSV, columnas, colClase)
        cleandata = kmeansmodel.previewData()
        fig = kmeansmodel.resolve(n)

        img_data = BytesIO()
        fig.savefig(img_data, format='png')
        img_data.seek(0)
        fig.close()

        encoded_img = base64.b64encode(img_data.read()).decode('utf-8')
        
        return jsonify({
            "algType": "kmeans",
            "filename": filename,
            "cleandata": cleandata.to_json(orient='records'),
            "details": json.dumps({"n": n}),
            "plot": encoded_img
            }) 
    
    elif metodo == "regressionTree":
        regTreeModel = RegTreeModel(dataCSV, columnas, colClase)
        cleandata = regTreeModel.previewData()
        fig = regTreeModel.resolve()

        img_data = BytesIO()
        fig.savefig(img_data, format='png')
        img_data.seek(0)
        fig.close()

        encoded_img = base64.b64encode(img_data.read()).decode('utf-8')
        
        return jsonify({
            "algType": "regressionTree",
            "filename": filename,
            "cleandata": cleandata.to_json(orient='records'),
            #"details": json.dumps({"n": n}),
            "plot": encoded_img
        }) 
@app.post('/file/upload')
def uploadFile():
    df = pd.read_csv(request.files['dataFile'])

    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(port=3000, debug=True)