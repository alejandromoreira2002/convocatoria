import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
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

        k_means = KMeans(n_clusters=self.n)
        k_means.fit(X)
        centroides = k_means.cluster_centers_
        etiquetas = k_means.labels_

        plt.cla()
        plt.clf()
        plt.plot(x, y,'g.', label='datos')

        plt.plot(centroides[:,0],centroides[:,1],'mo',markersize=8, label='centroides')

        plt.legend(loc='best')
        #plt.show()
        return plt