import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

with open('dataset_mention_predict.json', 'r') as f:
    df = pd.read_json(f)

    mark_INF101 = df["Semestre_1"].apply(lambda x: x['INF101'])
    mark_INF104 = df["Semestre_1"].apply(lambda x: x['INF104'])
    mark_INF107 = df["Semestre_1"].apply(lambda x: x['INF107'])
    mark_MTH101 = df["Semestre_1"].apply(lambda x: x['MTH101'])
    mark_MTH102 = df["Semestre_1"].apply(lambda x: x['MTH102'])
    mark_ORG101 = df["Semestre_1"].apply(lambda x: x['ORG101'])

    mark_INF102 = df["Semestre_2"].apply(lambda x: x['INF102'])
    mark_INF103 = df["Semestre_2"].apply(lambda x: x['INF103'])
    mark_INF105 = df["Semestre_2"].apply(lambda x: x['INF105'])
    mark_MTH106 = df["Semestre_2"].apply(lambda x: x['MTH106'])
    mark_MTH103 = df["Semestre_2"].apply(lambda x: x['MTH103'])
    mark_MTH105 = df["Semestre_2"].apply(lambda x: x['MTH105'])

    mark_INF201 = df["Semestre_3"].apply(lambda x: x['INF201'])
    mark_INF202 = df["Semestre_3"].apply(lambda x: x['INF202'])
    mark_INF203 = df["Semestre_3"].apply(lambda x: x['INF203'])
    mark_INF208 = df["Semestre_3"].apply(lambda x: x['INF208'])
    mark_MTH201 = df["Semestre_3"].apply(lambda x: x['MTH201'])
    mark_ORG201 = df["Semestre_3"].apply(lambda x: x['ORG201'])

    mention = df["mention"]

    df['mark_INF101'] = mark_INF101
    df['mark_INF104'] = mark_INF104
    df['mark_INF107'] = mark_INF107
    df['mark_MTH101'] = mark_MTH101
    df['mark_MTH102'] = mark_MTH102
    df['mark_ORG101'] = mark_ORG101

    df['mark_INF102'] = mark_INF102
    df['mark_INF103'] = mark_INF103
    df['mark_INF105'] = mark_INF105
    df['mark_MTH106'] = mark_MTH106
    df['mark_MTH103'] = mark_MTH103
    df['mark_MTH105'] = mark_MTH105

    df['mark_INF201'] = mark_INF201
    df['mark_INF202'] = mark_INF202
    df['mark_INF203'] = mark_INF203
    df['mark_INF208'] = mark_INF208
    df['mark_MTH201'] = mark_MTH201
    df['mark_ORG201'] = mark_ORG201

    df['mention'] = mention

    data = df[["mark_INF101", "mark_INF104", "mark_INF107", "mark_MTH101", "mark_ORG101", "mark_INF102", "mark_INF103",
               "mark_INF105", "mark_MTH106", "mark_MTH103", "mark_MTH105", "mark_INF201", "mark_INF202", "mark_INF203",
               "mark_INF208", "mark_MTH201", "mark_ORG201"]]
    df_x = pd.DataFrame(data, columns=data.keys())
    df_y = pd.DataFrame(df[["mention"]])
    data_training, data_test, result_training, result_test = train_test_split(df_x, df_y, test_size=0.2,
                                                                              random_state=42)
    reg = LinearRegression()
    reg.fit(data_training, result_training)
    result_prediction = reg.predict(data_test)

    print(df_x)
    print(result_prediction)
    print(result_test)

    """
     mention BD data
    mark_MTH101_BD = df["Semestre_1"].apply(lambda x: x['MTH101'])
    mark_MTH102_BD = df["Semestre_1"].apply(lambda x: x['MTH102'])
    mark_INF107_BD = df["Semestre_1"].apply(lambda x: x['INF107'])

    mark_INF102_BD = df["Semestre_2"].apply(lambda x: x['INF102'])
    mark_INF103_BD = df["Semestre_2"].apply(lambda x: x['INF103'])
    mark_INF105_BD = df["Semestre_2"].apply(lambda x: x['INF105'])
    mark_MTH105_BD = df["Semestre_2"].apply(lambda x: x['MTH105'])

    mark_INF202_BD = df["Semestre_3"].apply(lambda x: x['INF202'])
    mark_INF203_BD = df["Semestre_3"].apply(lambda x: x['INF203'])
    mark_INF208_BD = df["Semestre_3"].apply(lambda x: x['INF208'])
    mark_ORG201_BD = df["Semestre_3"].apply(lambda x: x['ORG201'])

    # mention web_design
    mark_INF101_web = df["Semestre_1"].apply(lambda x: x['INF101'])
    mark_INF104_web = df["Semestre_1"].apply(lambda x: x['INF104'])
    mark_INF107_web = df["Semestre_1"].apply(lambda x: x['INF107'])

    mark_INF106_web = df["Semestre_2"].apply(lambda x: x['INF105'])

    mark_INF201_web = df["Semestre_1"].apply(lambda x: x['INF201'])
    mark_MTH201_web = df["Semestre_1"].apply(lambda x: x['MTH201'])
    """
