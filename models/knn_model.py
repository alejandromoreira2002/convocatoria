import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from .MLAlgorithms import MLAlgorithms
import time

class KNNModel(MLAlgorithms):
    def __init__(self, dataCSV, columnas, colClase):
        super().__init__(dataCSV, columnas, colClase)

    def resolve2(self, k, centro=(0,0)):
        self.k = k
        self.centro = centro

        dataCSV = self.previewData()
        self.columnas.remove(self.colClase)
        x = dataCSV[self.columnas[0]]
        y = dataCSV[self.columnas[1]]

        classes = dataCSV[self.colClase]

        

        # Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )

        # Crear un modelo KNN con K=1
        data = list(zip(x, y))
        start_fit = time.time()
        knn = KNeighborsClassifier(n_neighbors= self.k)
        knn.fit(data, classes)
        end_fit = time.time()
        fit_time = end_fit - start_fit

        # Clasificar un nuevo punto
        new_x, new_y = self.centro
        #new_x = 63
        #new_y = 175
        new_point = [(new_x, new_y)]
        start_pred = time.time()
        prediction = knn.predict(new_point)
        end_pred = time.time()
        predict_time = end_pred - start_pred

        accuracy = accuracy_score(y_test, y_pred)

        self.prediction = self.binaClasses[prediction[0]]

        colors = ["blue", "red", "orange", "purple", "black", "green", "grey"]
        plt.cla()
        plt.clf()
        ax = plt.axes()
        for i in range(0, len(self.binaClasses)):
            ax.scatter(dataCSV.loc[dataCSV[self.colClase] == i, self.columnas[0]],
                    dataCSV.loc[dataCSV[self.colClase] == i, self.columnas[1]],
                    c=colors[i],
                    label=self.binaClasses[i])

        ax.scatter(new_x,
                new_y,
                c="yellow",
                s=110,
                marker= "*",
                edgecolors="black")
        plt.text(x=new_x-8.2, y=new_y-4.2, s=f"Centro, predicho: {self.prediction}", backgroundcolor= "#0000008F", c="white")
        plt.xlabel(self.columnas[0])
        plt.ylabel(self.columnas[1])
        ax.legend()

        return {
            "graph": plt, 
            "details": f"<p><b>Tiempo de procesamiento:</b></p><ul><li>Entrenamiento: ~{fit_time:.4f} segundos</li><li>Prediccion: ~{predict_time:.4f} segundos</li></ul><p><b>Eficiencia:</b></p><ul><li>Inercia: ~{inertia:.2f}</li><li>Puntaje de Silhouette: ~{silhouette:.4f}</li></ul>"
        }
    
    def resolve(self, k, centro=(0,0)):
        self.k = k
        self.centro = centro

        dataCSV = self.previewData()
        self.columnas.remove(self.colClase)
        x = dataCSV[self.columnas[0]]
        y = dataCSV[self.columnas[1]]

        classes = dataCSV[self.colClase]

        # Codificar Gender
        le = LabelEncoder()
        dataCSV['ClassEncoded'] = le.fit_transform(dataCSV[self.colClase])
        dataCSV['Color'] = dataCSV['ClassEncoded']

        # Definir características
        X = dataCSV[self.columnas]
        y = dataCSV['ClassEncoded']

        # Dividir datos
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Medir tiempos
        start_fit = time.time()
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_train, y_train)
        fit_time = time.time() - start_fit

        start_pred = time.time()
        y_pred = knn.predict(X_test)
        predict_time = time.time() - start_pred

        # Calcular exactitud
        accuracy = accuracy_score(y_test, y_pred)

        self.prediction = self.binaClasses[y_pred[0]]

        # Calcular centroides por género (media)
        centroids = dataCSV.groupby(self.colClase)[self.columnas].mean()


        # Graficar scatter y centroides
        plt.figure()
        plt.scatter(dataCSV[self.columnas[0]], dataCSV[self.columnas[1]], c=dataCSV['Color'])
        for gender, row in centroids.iterrows():
            plt.scatter(row[self.columnas[0]], row[self.columnas[1]], s=200, marker='X')
            plt.text(row[self.columnas[0]], row[self.columnas[1]], gender, fontsize=12, verticalalignment='bottom')
        
        # Etiquetas y título
        plt.xlabel(self.columnas[0])
        plt.ylabel(self.columnas[1])

        return {
            "graph": plt, 
            "details": f"<p><b>Tiempo de procesamiento:</b></p><ul><li>Entrenamiento: ~{fit_time:.4f} segundos</li><li>Prediccion: ~{predict_time:.4f} segundos</li></ul><p><b>Eficiencia:</b></p><ul><li>Exactitud: ~{accuracy:.4f}</li></ul>"
        }