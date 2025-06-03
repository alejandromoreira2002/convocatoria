import pandas as pd

class MLAlgorithms:
    def __init__(self, data, columnas, colClase):
        self.dataCSV = data
        self.columnas = columnas
        self.colClase = colClase
        self.cleanData()
    
    def cleanData(self):
        # Eliminacion de variables
        for column in self.dataCSV:
            rows = self.dataCSV[column].size
            nrows = self.dataCSV[column].isnull().sum()
            perc = (nrows*100)/rows
            if perc > 60:
                del self.dataCSV[column]

        # Reemplazo de valores vacios
        fillnavals = {}
        for col in self.dataCSV:
            column = self.dataCSV[col]
            if column.dtype =='int64':
                media = column.mean()
                fillnavals[col] = media
            elif column.dtype =='O':
                moda = column.mode()[0]
                fillnavals[col] = moda
        self.dataCSV = self.dataCSV.fillna(fillnavals)

    def previewData(self):
        # Datos de ejemplo
        dataCSV = self.dataCSV[self.columnas]

        self.binaClasses = pd.unique(self.dataCSV[self.colClase])
        mapeo = { elemento: indice for indice, elemento in enumerate(self.binaClasses) }
        print(dataCSV.head())
        #dataCSV[self.colClase] = self.dataCSV[self.colClase].replace(mapeo, inplace=True)
        dataCSV[self.colClase] = self.dataCSV[self.colClase].map(mapeo)
        #for i in range(0, len(self.binaClasses)):
        #    dataCSV[self.colClase] = self.dataCSV[self.colClase].replace(self.binaClasses[i], i)
        print(dataCSV.head())
        return dataCSV