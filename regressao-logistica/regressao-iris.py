import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score  # Corrigido aqui

# Carregar dados
iris = pd.read_csv("iris.csv")

# Filtrar a espécie virginica
iris = iris[iris['species'] != 'virginica']

# Separar em variáveis independentes (X) e dependentes (y)
X = iris.drop('species', axis=1)
y = iris['species']

# Mapear a variável alvo (y) para valores numéricos
y = y.map({'setosa': 0, 'versicolor': 1})

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Normalizar os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)  # Corrigido aqui

# Criar e treinar o modelo de Regressão Logística
modelo = LogisticRegression(solver="sag")
modelo.fit(X_train, y_train)

# Fazer predições
predicoes = modelo.predict(X_test)

# Exibir as predições e os valores reais
print(predicoes)
print(y_test)

# Calcular a acurácia
acc = accuracy_score(y_test, predicoes)  # Corrigido aqui
print(acc)
