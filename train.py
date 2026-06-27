import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("student-mat.csv", sep=";")

df["pass"] = (df["G3"] >= 10).astype(int)

features = ["studytime", "failures", "absences", "G1", "G2"]

X = df[features]

y = df["pass"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier()

model.fit(X_train, y_train)

joblib.dump(model, "model.pkl")

print("Model trained successfully!")