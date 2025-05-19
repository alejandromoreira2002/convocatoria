import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from .MLAlgorithms import MLAlgorithms

class KMeansModel(MLAlgorithms):
    def __init__(self, dataCSV, columnas, colClase):
        super().__init__(dataCSV, columnas, colClase)

    def resolve(self, n):
        self.n = n

        dataCSV = self.previewData()
        self.columnas.remove(self.colClase)
        x = dataCSV[self.columnas[0]]
        y = dataCSV[self.columnas[1]]
        classes = dataCSV[self.colClase]
        
        X = list(zip(x, y))

        start_time = time.time()
        k_means = KMeans(n_clusters=self.n)
        k_means.fit(X)
        end_time = time.time()
        processing_time = end_time - start_time
        centroides = k_means.cluster_centers_
        etiquetas = k_means.labels_
        
        inertia = k_means.inertia_
        silhouette = silhouette_score(X, etiquetas)

        plt.cla()
        plt.clf()
        plt.plot(x, y,'g.', label='datos')

        plt.plot(centroides[:,0],centroides[:,1],'mo',markersize=8, label='centroides')

        plt.legend(loc='best')
        #plt.show()

        return {
            "graph": plt, 
            "details": f"<p><b>Tiempo de procesamiento:</b></p><p>~{processing_time:.4f} segundos</p><p><b>Eficiencia:</b></p><ul><li>Inercia: ~{inertia:.2f}</li><li>Puntaje de Silhouette: ~{silhouette:.4f}</li></ul>"
        }