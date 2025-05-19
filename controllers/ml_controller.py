from models.kmeans_model import KMeansModel
from models.knn_model import KNNModel
from models.arbol_model import RegTreeModel
import base64
from io import BytesIO
import json

class MLController:
    def __init__(self, metodo):
        self.metodo = metodo

    def previsualizar(self, dataCSV, columnas, colClase):
        dfmodel = None
        if self.metodo == "knn":
            knnmodel = KNNModel(dataCSV, columnas, colClase)
            dfmodel = knnmodel.previewData()
        elif self.metodo == "kmeans":
            kmeansmodel = KMeansModel(dataCSV, columnas, colClase)
            dfmodel = kmeansmodel.previewData()
        elif self.metodo == "tree":
            rTree = RegTreeModel(dataCSV, columnas, colClase)
            dfmodel = rTree.previewData()
        
        return dfmodel

    def procesar(self, dataCSV, columnas, colClase, peticion):
        if self.metodo == "knn":
            k = int(peticion.get('k'))
            centro = tuple([int(x) for x in peticion.get('centro').split(',')])
            
            knnmodel = KNNModel(dataCSV, columnas, colClase)
            cleandata = knnmodel.previewData()
            resultado = knnmodel.resolve(k, centro)
            graph = resultado['graph']

            img_data = BytesIO()
            graph.savefig(img_data, format='png')
            img_data.seek(0)
            graph.close()

            encoded_img = base64.b64encode(img_data.read()).decode('utf-8')

            prediction = knnmodel.prediction

            return {
                "algType": "knn",
                "cleandata": cleandata.to_json(orient='records'),
                "details": json.dumps({"k": k, "centro": peticion.get('centro')}),
                "res_details": resultado['details'],
                "prediction": prediction,
                "plot": encoded_img
            }
        elif self.metodo == "kmeans":
            n = int(peticion.get('n'))
        
            kmeansmodel = KMeansModel(dataCSV, columnas, colClase)
            cleandata = kmeansmodel.previewData()
            resultado = kmeansmodel.resolve(n)
            graph = resultado['graph']
            
            img_data = BytesIO()
            graph.savefig(img_data, format='png')
            img_data.seek(0)
            graph.close()

            encoded_img = base64.b64encode(img_data.read()).decode('utf-8')

            return {
                "algType": "kmeans",
                "cleandata": cleandata.to_json(orient='records'),
                "details": json.dumps({"n": n}),
                "res_details": resultado['details'],
                "plot": encoded_img
            }
        
        elif self.metodo == "tree":
            regTreeModel = RegTreeModel(dataCSV, columnas, colClase)
            cleandata = regTreeModel.previewData()
            print(cleandata.head())
            resultado = regTreeModel.resolve()
            graph = resultado['graph']
            
            img_data = BytesIO()
            graph.savefig(img_data, format='png')
            img_data.seek(0)
            graph.close()

            encoded_img = base64.b64encode(img_data.read()).decode('utf-8')
            return {
                "algType": "tree",
                "cleandata": cleandata.to_json(),
                #"details": json.dumps({"n": n}),
                "res_details": resultado['details'],
                "plot": encoded_img
            }