import pandas as pd
import lightgbm as lgb
import joblib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from features.feature_engineering import add_features

MODEL_PATH = "models/lightgbm_model.txt"
FEATURE_PATH = "data/btcusdt_1h.csv"

FEATURES = [
    'close', 'volume', 'sma_5', 'sma_10', 'sma_15', 'return',
    'rsi_14', 'bb_middle', 'bb_upper', 'bb_lower', 'bb_width',
    'macd', 'momentum'
]

def load_model():
    if MODEL_PATH.endswith(".pkl"):
        return joblib.load(MODEL_PATH)
    else:
        return lgb.Booster(model_file=MODEL_PATH)

def prepare_latest_features():
    df = pd.read_csv(FEATURE_PATH)
    df_feat = add_features(df)
    return df_feat.iloc[-1:][FEATURES]  # exakt gleiche Features wie im Training!

def predict_signal():
    model = load_model()
    X = prepare_latest_features()
    prediction = model.predict(X)[0]
    if prediction > 0.6:
        return "BUY"
    elif prediction < 0.4:
        return "SELL"
    else:
        return "HOLD"

if __name__ == "__main__":
    signal = predict_signal()
    print(f"🚨 Predicted Signal: {signal}")
