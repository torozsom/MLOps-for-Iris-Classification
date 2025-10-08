import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import json


def main():
    data_path = "data/data.csv"
    df = pd.read_csv(data_path, header=None)
    X = df.iloc[:, 0:4]
    y = df.iloc[:, 4]

    label_encoder = LabelEncoder()
    y_encoded = pd.DataFrame(label_encoder.fit_transform(y), columns=[y.name])
    test_size = 0.2
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=test_size)

    train_path = "data/train.csv"
    test_path = "data/test.csv"
    pd.concat((X_train, y_train), axis=1).to_csv(train_path, index=False, header=False)
    pd.concat((X_test, y_test), axis=1).to_csv(test_path, index=False, header=False)

    class_path = "data/classes.json"
    class_names = label_encoder.classes_.tolist()
    with open(class_path, 'w') as f:
        json.dump(class_names, f, indent=4)


if __name__ == '__main__':
    main()
