import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def cargar_data():
    datos = pd.read_csv('cancer_de_mama_update.csv')
    return datos

def separar_data(data):
    X = data.drop('class', axis=1)
    y = data['class']
    return X, y

def normalizar(X):
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    return X

def entrenar_datos(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    return knn, X_test, y_test, X_train, y_train

def predecir(knn, X_test):
    prediccion = knn.predict(X_test)
    return prediccion

def mostrar_precision_modelo (knn, X_test, y_test):
    precision = knn.score(X_test, y_test)
    return precision

def knn_prediction(new_data):

    data = cargar_data()
    X, y = separar_data(data)
    X = normalizar(X)
    knn, X_test, y_test, X_train, y_train = entrenar_datos(X, y)

    # Utiliza el modelo para hacer predicciones sobre el conjunto de prueba
    predicciones = knn.predict(X_test)

    # Hacemos una predicción utilizando el modelo
    y_pred = knn.predict(new_data)

    # Precision del modelo
    precision = mostrar_precision_modelo(knn, X_test, y_test)

    # Devuelve los resultados de la predicción
    return y_pred, precision
