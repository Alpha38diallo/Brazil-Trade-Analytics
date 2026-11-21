import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

sns.set_style("whitegrid")

df = pd.read_csv(
    "data/processed/brazil_trade_2020_2025_clean.csv",
    dtype={"commodity_code": str},
    low_memory=False
)

df = df[df["partner_country"] != "World"]
df = df[df["commodity_description"] != "All Commodities"]

yearly = (
    df.groupby(["period", "trade_flow"])["trade_value_usd"]
      .sum()
      .reset_index()
)

plt.figure(figsize=(12,6))

sns.lineplot(
    data=yearly,
    x="period",
    y="trade_value_usd",
    hue="trade_flow",
    marker="o"
)

plt.title("Brazil Trade Evolution")
plt.xlabel("Year")
plt.ylabel("USD")

plt.tight_layout()

plt.savefig(
    "reports/figures/trade_evolution.png"
)

plt.close()

exports = (
    df[df["trade_flow"] == "Export"]
    .groupby("period")["trade_value_usd"]
    .sum()
)

imports = (
    df[df["trade_flow"] == "Import"]
    .groupby("period")["trade_value_usd"]
    .sum()
)

balance = exports - imports

plt.figure(figsize=(12,6))

balance.plot(
    kind="bar",
    color="green"
)

plt.title("Brazil Trade Balance")
plt.ylabel("USD")

plt.tight_layout()

plt.savefig(
    "reports/figures/trade_balance.png"
)

plt.close()

partners = (
    df.groupby("partner_country")["trade_value_usd"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

plt.figure(figsize=(12,6))

partners.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Trading Partners")

plt.tight_layout()

plt.savefig(
    "reports/figures/top_partners.png"
)

plt.close()

top_exports = (
    df[df["trade_flow"] == "Export"]
    .groupby("commodity_description")["trade_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(18,10))

top_exports.index = [
    textwrap.shorten(str(x), width=45, placeholder="...")
    for x in top_exports.index
]

top_exports.sort_values().plot(
    kind="barh"
)

plt.title("Top Export Products")

plt.tight_layout()

plt.savefig(
    "reports/figures/top_exports.png"
)

plt.close()

top_imports = (
    df[df["trade_flow"] == "Import"]
    .groupby("commodity_description")["trade_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(18,10))

top_imports.index = [
    textwrap.shorten(str(x), width=45, placeholder="...")
    for x in top_imports.index
]

top_imports.sort_values().plot(
    kind="barh"
)

plt.title("Top Import Products")

plt.tight_layout()

plt.savefig(
    "reports/figures/top_imports.png"
)

plt.close()

