# regression.py
import csv
import numpy as np
from sklearn.linear_model import LinearRegression


def load_training_data_csv(path="df_weather.csv"):
    temps = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # 👉 CỘT NHIỆT ĐỘ CHUẨN
        TEMP_COL = "day.avgtemp_c"

        for row in reader:
            if row[TEMP_COL] != "":
                temps.append(float(row[TEMP_COL]))

    X = np.arange(len(temps)).reshape(-1, 1)
    y = np.array(temps)

    return X, y


def predict_next_24h_from_csv(csv_path="df_weather.csv"):
    X, y = load_training_data_csv(csv_path)

    model = LinearRegression()
    model.fit(X, y)

    # ⚠️ Vì data là THEO NGÀY → dự đoán 8 NGÀY TIẾP
    next_X = np.arange(len(y), len(y) + 8).reshape(-1, 1)
    predicted = model.predict(next_X)

    return y.tolist(), predicted.tolist()
