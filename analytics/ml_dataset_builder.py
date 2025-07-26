import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

def prepare_ml_dataset(input_path: str, output_dir: str, target_column: str = "future_return", test_size=0.2):
    df = pd.read_csv(input_path, parse_dates=["timestamp"])
    
    if target_column not in df.columns:
        raise ValueError(f"❌ '{target_column}' nicht im Dataset gefunden.")

    df = df.dropna()

    X = df.drop(columns=["timestamp", target_column])
    y = df[target_column]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)

    # Normalisierung
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save
    os.makedirs(output_dir, exist_ok=True)
    pd.DataFrame(X_train_scaled, columns=X.columns).to_csv(f"{output_dir}/X_train.csv", index=False)
    pd.DataFrame(X_test_scaled, columns=X.columns).to_csv(f"{output_dir}/X_test.csv", index=False)
    y_train.to_csv(f"{output_dir}/y_train.csv", index=False)
    y_test.to_csv(f"{output_dir}/y_test.csv", index=False)

    print("✅ ML-Dataset gespeichert unter:", output_dir)

if __name__ == "__main__":
    prepare_ml_dataset(
        input_path="data/btcusdt_1h_features.csv",
        output_dir="data/ml_dataset",
        target_column="future_return"  # oder z.B. 'label' wenn du Klassifikation willst
    )
