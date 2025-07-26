import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_features(file_path: str):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])
    df.set_index("timestamp", inplace=True)

    print("📊 Shape:", df.shape)
    print("🕳️ Missing Values:\n", df.isnull().sum())

    # Korrelation
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("📈 Korrelationsmatrix")
    plt.tight_layout()
    plt.savefig("analytics/correlation_matrix.png")
    print("✅ Korrelation gespeichert: analytics/correlation_matrix.png")

    # Verteilung der wichtigsten Features
    important_features = ['close', 'sma_5', 'sma_20', 'rsi_14']
    df[important_features].hist(figsize=(10, 8), bins=40)
    plt.tight_layout()
    plt.savefig("analytics/feature_distributions.png")
    print("✅ Verteilungen gespeichert: analytics/feature_distributions.png")

if __name__ == "__main__":
    analyze_features("data/btcusdt_1h_features.csv")
