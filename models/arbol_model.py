import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.tree import export_graphviz
from sklearn.tree import export_text
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from .MLAlgorithms import MLAlgorithms

class RegTreeModel(MLAlgorithms):
    def __init__(self, dataCSV, columnas, colClase):
        super().__init__(dataCSV, columnas, colClase)

    def previewData(self):
        colsCompletas = [self.colClase] + self.columnas
        dataCSV = self.dataCSV[colsCompletas]
        return dataCSV

    def resolve(self):
        #Eliminacion de variables innecesarias
        #datos = datos.drop(columns = ["Date", "Holiday_Flag", "Store", "Unemployment"])

        #datos.head()
        #self.n = n

        dataCSV = self.previewData()

        # División de los datos en train y test
        # ------------------------------------------------------------------------------
        X_train, X_test, y_train, y_test = train_test_split(
                                                dataCSV.drop(columns = self.colClase),
                                                dataCSV[self.colClase],
                                                random_state = 123
                                            )
        # Creación del modelo
        # ------------------------------------------------------------------------------
        modelo = DecisionTreeRegressor(
                    max_depth         = 3,
                    random_state      = 123
                )

        # Entrenamiento del modelo
        # ------------------------------------------------------------------------------
        modelo.fit(X_train, y_train)
        
        # Estructura del árbol creado
        # ------------------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(12, 5))

        print(f"Profundidad del árbol: {modelo.get_depth()}")
        print(f"Número de nodos terminales: {modelo.get_n_leaves()}")

        plt = plot_tree(
                decision_tree = modelo,
                feature_names = dataCSV.drop(columns = self.colClase).columns,
                class_names   = dataCSV[self.colClase],
                filled        = True,
                impurity      = False,
                fontsize      = 10,
                precision     = 2,
                ax            = ax
        )
        return plt