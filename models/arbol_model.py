import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.tree import export_graphviz
from sklearn.tree import export_text
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import LabelBinarizer
import time
from .MLAlgorithms import MLAlgorithms

class RegTreeModel(MLAlgorithms):
    def __init__(self, dataCSV, columnas, colClase):
        super().__init__(dataCSV, columnas, colClase)

    def previewData(self):
        colsCompletas = self.columnas
        dataCSV = self.dataCSV[colsCompletas]
        return dataCSV

    def resolve(self):
        dataCSV = self.previewData()

        # División de los datos en train y test
        X_train, X_test, y_train, y_test = train_test_split(
            dataCSV.drop(columns = self.colClase),
            dataCSV[self.colClase],
            test_size=0.3,
            random_state = 123
        )

        start_fit = time.time()
        # Creación del modelo
        modelo = DecisionTreeRegressor(
            max_depth         = 3,
            random_state      = 123
        )

        # Binarizar etiquetas
        lb = LabelBinarizer()
        y_train_bin = lb.fit_transform(y_train)
        y_test_bin = lb.transform(y_test)

        # Entrenamiento del modelo
        modelo.fit(X_train, y_train_bin)
        fit_time = time.time() - start_fit
        
        # Prediccion del modelo
        start_pred = time.time()
        y_pred = modelo.predict(X_test)
        predict_time = time.time() - start_pred

        # 4. Métricas de eficiencia
        r2 = r2_score(y_test_bin, y_pred)
        mse = mean_squared_error(y_test_bin, y_pred)
        mae = mean_absolute_error(y_test_bin, y_pred)

        # Estructura del árbol creado
        fig, ax = plt.subplots(figsize=(12, 5))

        print(f"Profundidad del árbol: {modelo.get_depth()}")
        print(f"Número de nodos terminales: {modelo.get_n_leaves()}")

        plot_tree(
            decision_tree = modelo,
            feature_names = dataCSV.drop(columns = self.colClase).columns,
            class_names   = dataCSV[self.colClase],
            filled        = True,
            impurity      = False,
            fontsize      = 10,
            precision     = 2,
            ax            = ax
        )
        #plt.show()
        
        return {
            "graph": plt, 
            "details": f"<p><b>Tiempo de procesamiento:</b></p><ul><li>Entrenamiento: ~{fit_time:.4f} segundos</li><li>Prediccion: ~{predict_time:.4f} segundos</li></ul><p><b>Eficiencia:</b></p><ul><li>R²: ~{r2:.4f}</li><li>MSE: ~{mse:.4f}</li><li>MAE: ~{mae:.4f}</li></ul>"
        }