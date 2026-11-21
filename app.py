import pandas as pd
import streamlit as st
import plotly.express as px
import textwrap

# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Brazil Trade Analytics",
    page_icon="🇧🇷",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/processed/brazil_trade_2020_2025_clean.csv",
        low_memory=False
    )

    # Nettoyage des colonnes
    df.columns = df.columns.str.strip()

    # Renommage vers des noms standard
    df = df.rename(columns={
        "période": "period",
        "pays_reporter": "reporter_country",
        "pays_partenaire": "partner_country",
        "flux_commercial": "trade_flow",
        "code_produit": "commodity_code",
        "description_du_produit": "commodity_description",
        "valeur_échange_usd": "trade_value_usd",
        "poids_net_kg": "net_weight_kg"
    })

    df = df[
    ~df["partner_country"].isin(["World"])
]

    df = df[
    ~df["commodity_description"].isin(["All Commodities"])
]

    return df


df = load_data()

# ==================================================
# TITRE
# ==================================================

st.title("🇧🇷 Tableau de bord d'analyse du commerce du Brésil")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Filtres")

years = sorted(df["period"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Années",
    years,
    default=years
)

partners = sorted(df["partner_country"].dropna().unique())

selected_partner = st.sidebar.selectbox(
    "Partenaire commercial",
    ["Tous"] + partners
)

# Produit (HS6 + description)
df["product_label"] = (
    df["commodity_code"].astype(str)
    + " - "
    + df["commodity_description"]
)

products = sorted(
    df["product_label"].dropna().unique()
)

selected_product = st.sidebar.selectbox(
    "Produit",
    ["Tous"] + products
)

# ==================================================
# FILTRES
# ==================================================

df_filtered = df[
    df["period"].isin(selected_years)
]

if selected_partner != "Tous":
    df_filtered = df_filtered[
        df_filtered["partner_country"] == selected_partner
    ]

if selected_product != "Tous":
    df_filtered = df_filtered[
        df_filtered["product_label"] == selected_product
    ]

# ==================================================
# KPI
# ==================================================

exports = df_filtered[
    df_filtered["trade_flow"] == "Export"
]["trade_value_usd"].sum()

imports = df_filtered[
    df_filtered["trade_flow"] == "Import"
]["trade_value_usd"].sum()

balance = exports - imports

partners_count = df_filtered["partner_country"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Exportations",
    f"${exports/1e12:.2f} T"
)

col2.metric(
    "Importations",
    f"${imports/1e12:.2f} T"
)

col3.metric(
    "Balance commerciale",
    f"${balance/1e12:.2f} T"
)

col4.metric(
    "Partenaires",
    f"{partners_count}"
)

st.divider()

# ==================================================
# EVOLUTION IMPORT / EXPORT
# ==================================================

st.subheader("📈 Évolution du commerce")

yearly_trade = (
    df_filtered
    .groupby(["period", "trade_flow"])["trade_value_usd"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    yearly_trade,
    x="period",
    y="trade_value_usd",
    color="trade_flow",
    markers=True,
)

fig1.update_layout(
    xaxis_title="Année",
    yaxis_title="Valeur commerciale (USD)",
    legend_title="Flux commercial"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==================================================
# TOP PARTNERS
# ==================================================

st.subheader("🌍 Top 10 partenaires commerciaux")

partners_df = (
    df_filtered
    .groupby("partner_country")["trade_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    partners_df,
    x="trade_value_usd",
    y="partner_country",
    orientation="h",
    color="trade_value_usd"
)

fig2.update_layout(
    xaxis_title="Valeur commerciale (USD)",
    yaxis_title="",
    coloraxis_showscale=False
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==================================================
# TOP EXPORT PRODUCTS
# ==================================================

st.subheader("🚢 Top 10 produits exportés")

top_exports = (
    df_filtered[df_filtered["trade_flow"] == "Export"]
    .groupby("commodity_description")["trade_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_exports["commodity_description"] = (
    top_exports["commodity_description"]
    .apply(
        lambda x: textwrap.shorten(
            str(x),
            width=60,
            placeholder="..."
        )
    )
)

fig3 = px.bar(
    top_exports,
    x="trade_value_usd",
    y="commodity_description",
    orientation="h",
    color="trade_value_usd"
)

fig3.update_layout(
    xaxis_title="Valeur commerciale (USD)",
    yaxis_title="",
    coloraxis_showscale=False
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==================================================
# TOP IMPORT PRODUCTS
# ==================================================

st.subheader("📦 Top 10 produits importés")

top_imports = (
    df_filtered[df_filtered["trade_flow"] == "Import"]
    .groupby("commodity_description")["trade_value_usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

top_imports["commodity_description"] = (
    top_imports["commodity_description"]
    .apply(
        lambda x: textwrap.shorten(
            str(x),
            width=80,
            placeholder="..."
        )
    )
)

fig4 = px.bar(
    top_imports,
    x="trade_value_usd",
    y="commodity_description",
    orientation="h",
    color="trade_value_usd"
)

fig4.update_layout(
    xaxis_title="Valeur commerciale (USD)",
    yaxis_title="",
    coloraxis_showscale=False
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "Source : UN Comtrade API | Brazil Trade Analytics (2020-2025)"
)