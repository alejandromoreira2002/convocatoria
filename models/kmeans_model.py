import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from .MLAlgorithms import MLAlgorithms

class KMeansModel(MLAlgorithms):
    def __init__(self, dataCSV, columnas, colClase):
        super().__init__(dataCSV, columnas, colClase)

    def previewData(self):
        colsCompletas = self.columnas
        dataCSV = self.dataCSV[colsCompletas]
        return dataCSV

    def resolve(self, n):
        self.n = n

        dataCSV = self.previewData()
        #self.columnas.remove(self.colClase)
        features = dataCSV[self.columnas]
        #y = dataCSV[self.columnas[1]]
        #classes = dataCSV[self.colClase]
        start_time = time.time()
        
        #X = list(zip(x, y))
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(features)

        k_means = KMeans(n_clusters=self.n, random_state=42)
        clusters = k_means.fit_predict(X_scaled)
        
        #processing_time = end_time - start_time
        centroides = k_means.cluster_centers_
        etiquetas = k_means.labels_
        inertia = k_means.inertia_

        silhouette = silhouette_score(
            X_scaled,
            clusters,
            sample_size=round(dataCSV.shape[0]*0.2),      # número de puntos a muestrear
            random_state=42        # para reproducibilidad
        )


        # 5. Reducir dimensión para visualización con PCA
        pca = PCA(n_components=2, random_state=42)
        X_pca = pca.fit_transform(X_scaled)

        elapsed_time = time.time() - start_time
        # 6. Gráfica de dispersión de los clusters
        plt.figure(figsize=(8, 6))
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, edgecolor='k', s=50)
        plt.xlabel('Componente Principal 1')
        plt.ylabel('Componente Principal 2')
        plt.title(f'Agrupamiento KMeans (k={self.n}) en City Payroll Data')
        #plt.show()

        #plt.plot(centroides[:,0],centroides[:,1],'mo',markersize=8, label='centroides')

        #plt.legend(loc='best')
        #plt.show()

        return {
            "graph": plt, 
            "details": f"<p><b>Tiempo de procesamiento:</b></p><p>~{elapsed_time:.4f} segundos</p><p><b>Eficiencia:</b></p><ul><li>Inercia: ~{inertia:.2f}</li><li>Puntaje de Silhouette: ~{silhouette:.4f}</li></ul>"
        }