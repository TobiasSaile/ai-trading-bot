import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os
from lightgbm import LGBMClassifier
import lightgbm

FEATURES = [
    'close', 'volume', 'sma_5', 'sma_10', 'sma_15', 'return',
    'rsi_14', 'bb_middle', 'bb_upper', 'bb_lower', 'bb_width',
    'macd', 'momentum'
]

def train_lightgbm(X_train, y_train, X_val, y_val):
    model = LGBMClassifier(n_estimators=1000)
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        eval_metric="logloss",
        callbacks=[
            lightgbm.early_stopping(stopping_rounds=10),
            lightgbm.log_evaluation(0)
        ]
    )
    return model

def load_features(path='data/features.csv'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Feature-Datei nicht gefunden: {path}")
    return pd.read_csv(path)

def prepare_data(df):
    X = df[FEATURES]  # <- NUR die gewünschten Features
    y = df['target']
    print("Trainings-Features:", X.columns.tolist())
    return train_test_split(X, y, test_size=0.2, shuffle=False)

def evaluate_model(model, X_val, y_val):
    y_pred = model.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    print(f"📊 Validierungsgenauigkeit: {acc:.4f}")
    return acc

def save_model(model, path='models/lgbm_model.pkl'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"✅ Modell gespeichert unter: {path}")

if __name__ == '__main__':
    print("🚀 Training gestartet...")
    df = load_features()
    X_train, X_val, y_train, y_val = prepare_data(df)
    model = train_lightgbm(X_train, y_train, X_val, y_val)
    evaluate_model(model, X_val, y_val)
    save_model(model)
    model.booster_.save_model("models/lightgbm_model.txt")
    print("✅ Modell gespeichert unter: models/lightgbm_model.txt")
