import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_iris
from sklearn import metrics

with open('new_data.json', 'r') as f:
    df = pd.read_json(f)
    mark_INF101 = df["Semestre_1"].apply(lambda x: x['INF101'])
    mark_INF104 = df["Semestre_1"].apply(lambda x: x['INF104'])
    mark_INF107 = df["Semestre_1"].apply(lambda x: x['INF107'])
    mark_MTH101 = df["Semestre_1"].apply(lambda x: x['MTH101'])
    mark_MTH102 = df["Semestre_1"].apply(lambda x: x['MTH102'])
    mark_ORG101 = df["Semestre_1"].apply(lambda x: x['ORG101'])
    Nb_retard = df["Semestre_1"].apply(lambda x: x['Nb_retard'])
    Nb_absence = df["Semestre_1"].apply(lambda x: x['Nb_absence'])
    Pb_abandonnement = df["Semestre_1"].apply(lambda x: x['Pb_abandonnement'])

    df['mark_INF101'] = mark_INF101
    df['mark_INF104'] = mark_INF104
    df['mark_INF107'] = mark_INF107
    df['mark_MTH101'] = mark_MTH101
    df['mark_MTH102'] = mark_MTH102
    df['mark_ORG101'] = mark_ORG101
    df['Nb_retard'] = Nb_retard
    df['Nb_absence'] = Nb_absence
    df['Pb_abandonnement'] = Pb_abandonnement

data = df[["mark_INF101", "mark_INF104", "mark_INF107", "mark_MTH101", "mark_MTH102", "mark_ORG101", "Nb_retard",
           "Nb_absence"]]
df_x = pd.DataFrame(data, columns=data.keys())
df_y = pd.DataFrame(df[["Pb_abandonnement"]])
data_training, data_test, result_training, result_test = train_test_split(df_x, df_y, test_size=0.2, random_state=42)
reg = LinearRegression()
reg.fit(data_training, result_training)
result_prediction = reg.predict(data_test)

newdata = [[10, 7, 7, 11, 8, 6, 20, 6]]
newTest = pd.DataFrame(newdata, columns=["mark_INF101", "mark_INF104", "mark_INF107", "mark_MTH101", "mark_MTH102",
                                         "mark_ORG101", "Nb_retard",
                                         "Nb_absence"])
pred = reg.predict(newTest)
# print(pred)
print(df_x)
print(result_prediction)
print(result_test)
print("pred", pred)
# print(metrics.r2_score(result_test, result_prediction))
"""
    data = df[["retard", "absence"]]
    df_x = pd.DataFrame(data, columns=data.keys())
    df_y = pd.DataFrame(df[["pourcentage"]])

data_training, data_test, result_training, result_test = train_test_split(df_x, df_y, test_size=0.2, random_state=42)
reg = LinearRegression()
reg.fit(data_training, result_training)
result_prediction = reg.predict(data_test)

print(result_prediction)
print(result_test)
print('efficaccité du model', metrics.r2_score(result_test, result_prediction))
"""
# print(df_x.head())
# print(df_y.head())

"""
iris = load_iris()
df_x = pd.DataFrame(iris.data, columns=iris.feature_names)
df_y = pd.DataFrame(iris.target)

data_training, data_test, result_training, result_test = train_test_split(df_x, df_y, test_size=0.2, random_state=42)

reg = LinearRegression()

reg.fit(data_training, result_training)

result_prediction = reg.predict(data_test)
print(df_x)
print(df_y)
# print(df_y.head())
print(result_prediction)
print(result_test)
print('efficaccité du model', metrics.r2_score(result_test, result_prediction))
"""
