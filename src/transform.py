import pandas as pd

INPUT_FILE = "data/processed/brazil_trade_2020_2025_raw.csv"
OUTPUT_FILE = "data/processed/brazil_trade_2020_2025_clean.csv"

df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

print("Avant nettoyage :", df.shape)

# Suppression des doublons
df = df.drop_duplicates()

# Colonnes importantes uniquement
columns_to_keep = [
    "period",
    "reporterDesc",
    "partnerDesc",
    "flowDesc",
    "cmdCode",
    "cmdDesc",
    "primaryValue",
    "netWgt"
]

df = df[columns_to_keep]

# Renommage
df = df.rename(columns={
    "reporterDesc": "reporter_country",
    "partnerDesc": "partner_country",
    "flowDesc": "trade_flow",
    "cmdCode": "commodity_code",
    "cmdDesc": "commodity_description",
    "primaryValue": "trade_value_usd",
    "netWgt": "net_weight_kg"
})

# Types
df["trade_value_usd"] = pd.to_numeric(
    df["trade_value_usd"],
    errors="coerce"
)

df["net_weight_kg"] = pd.to_numeric(
    df["net_weight_kg"],
    errors="coerce"
)

# Suppression lignes invalides
df = df.dropna(
    subset=[
        "trade_value_usd",
        "commodity_code"
    ]
)

# Valeurs négatives
df = df[df["trade_value_usd"] >= 0]

print("Après nettoyage :", df.shape)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Dataset nettoyé créé ✅")