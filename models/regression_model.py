import matplotlib
matplotlib.use("Agg")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import time
from .MLAlgorithms import MLAlgorithms

class RegresionModel(MLAlgorithms):
    def __init__(self, dataCSV, columnas, colClase):
        super().__init__(dataCSV, columnas, colClase)

    def previewData(self):
        colsCompletas = self.columnas
        dataCSV = self.dataCSV[colsCompletas]
        return dataCSV

    def resolve(self):
        html = "<p><b>Tiempo de procesamiento:</b></p><ul>"

        dataCSV = self.previewData()
        self.columnas.remove(self.colClase)

        # Selección de características y variable objetivo
        # Usamos item_price y quantity para predecir transaction_amount
        X = dataCSV[self.columnas]
        y = dataCSV[self.colClase]

        # División en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Entrenar el modelo de regresión lineal
        train_time_start = time.time()
        model = LinearRegression()
        model.fit(X_train, y_train)
        train_time_end = time.time()
        html += f"<li>Entrenamiento: {train_time_end - train_time_start:.3f} segundos</li>"

        # Evaluación del modelo
        intercept = model.intercept_
        coefficients = dict(zip(X.columns, model.coef_))
        r2_score = model.score(X_test, y_test)
        
        # Prediccion del modelo
        pred_time_start = time.time()
        y_pred = model.predict(X_test)
        pred_time_end = time.time()
        html += f"<li>Prediccion: {pred_time_end - pred_time_start:.3f} segundos</li>"

        html += "</ul><p><b>Eficiencia:</b></p><ul>"

        html += f'<li>Intercept (β₀): {intercept:.3f}</li><li>Coeficientes (βᵢ):</li><ul>'
        for feat, coef in coefficients.items():
            html += f'<li> {feat}: {coef:.3f}</li>'
        html += f'</ul><li>R²: {r2_score:.3f}</li></ul>'

        # Visualización: scatter de valores reales vs predichos
        plt.figure()
        plt.scatter(y_test, y_pred, alpha=0.6)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], linestyle='--')
        plt.xlabel('Monto real de la transacción')
        plt.ylabel('Monto predicho por el modelo')
        plt.title('Regresión Lineal: Transacción real vs predicha')
        #plt.show()

        return {
            "graph": plt, 
            "details": html
        }