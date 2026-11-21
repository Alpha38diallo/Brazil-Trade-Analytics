from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw/brazil")
OUTPUT_DIR = Path("data/processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = sorted(DATA_DIR.glob("*.csv"))

dfs = []

for file in files:
    print(f"Loading {file.name}")

    df = pd.read_csv(
        file,
        low_memory=False
    )

    dfs.append(df)

master_df = pd.concat(
    dfs,
    ignore_index=True
)

print(f"Shape avant nettoyage : {master_df.shape}")

master_df.to_csv(
    OUTPUT_DIR / "brazil_trade_2020_2025_raw.csv",
    index=False
)

print("Dataset fusionné créé ✅") 