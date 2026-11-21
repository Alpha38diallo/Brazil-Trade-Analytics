import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
df = pd.read_csv(
    "data/processed/brazil_trade_2020_2025_clean.csv"
)

print("\n===== DATASET OVERVIEW =====")
print(df.head())

print("\n===== SHAPE =====")
print(df.shape)

print("\n===== INFO =====")
print(df.info())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DESCRIPTIVE STATS =====")
print(df.describe())

print("\n===== TOTAL TRADE VALUE =====")

exports = df[df["trade_flow"] == "Export"]["trade_value_usd"].sum()
imports = df[df["trade_flow"] == "Import"]["trade_value_usd"].sum()

balance = exports - imports

print(f"Total Exports : ${exports:,.0f}")
print(f"Total Imports : ${imports:,.0f}")
print(f"Trade Balance : ${balance:,.0f}")
trade_year = (
    df.groupby(["period", "trade_flow"])["trade_value_usd"]
    .sum()
    .reset_index()
)

print("\n===== TRADE BY YEAR =====")
print(trade_year)

top_partners = (
    df.groupby("partner_country")["trade_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 PARTNERS =====")
print(top_partners)

top_exports = (
    df[df["trade_flow"] == "Export"]
    .groupby("commodity_description")["trade_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 EXPORTED PRODUCTS =====")
print(top_exports)

top_imports = (
    df[df["trade_flow"] == "Import"]
    .groupby("commodity_description")["trade_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 IMPORTED PRODUCTS =====")
print(top_imports)