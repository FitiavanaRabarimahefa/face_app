import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_iris
from sklearn import metrics

iris = load_iris()
df_x = pd.DataFrame(iris.data, columns=iris.feature_names)
df_y = pd.DataFrame(iris.target)

# base de donnée d'entrainement
data_training, data_test, result_training, result_test = train_test_split(df_x, df_y, test_size=0.2, random_state=42)

reg = LinearRegression()

# lancement de l 'entrainement du modele
reg.fit(data_training, result_training)

result_prediction = reg.predict(data_test)
print(df_x.head())
print(df_y.head())
print(result_prediction)
print(result_test)
print('efficaccité du model', metrics.r2_score(result_test, result_prediction))
