import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- Configuration de la page ---
st.set_page_config(
    page_title="Dashboard Dépenses Personnelles",
    page_icon="💸",
    layout="wide"
)

# --- Catégories automatiques par mot-clé (démo de logique métier) ---
CATEGORY_KEYWORDS = {
    "Alimentation": ["migros", "coop", "carrefour", "supermarché", "restaurant", "boulangerie"],
    "Transport": ["cff", "sbb", "essence", "uber", "parking", "tpg", "tl "],
    "Logement": ["loyer", "assurance", "electricité", "eau", "internet"],
    "Loisirs": ["cinema", "netflix", "spotify", "concert", "bar", "sport"],
    "Shopping": ["zalando", "amazon", "vinted", "h&m", "zara"],
    "Santé": ["pharmacie", "médecin", "dentiste", "hopital"],
}

def auto_categorize(description):
    desc = str(description).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(k in desc for k in keywords):
            return category
    return "Autre"

@st.cache_data
def load_sample_data():
    return pd.read_csv("sample_data.csv", parse_dates=["date"])

# --- Sidebar : upload et filtres ---
st.sidebar.title("⚙️ Options")
uploaded_file = st.sidebar.file_uploader(
    "Importer un fichier CSV (colonnes: date, description, montant)",
    type="csv"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, parse_dates=["date"])
else:
    st.sidebar.info("Aucun fichier importé — affichage de données d'exemple.")
    df = load_sample_data()

if "categorie" not in df.columns:
    df["categorie"] = df["description"].apply(auto_categorize)

df["date"] = pd.to_datetime(df["date"])
df["mois"] = df["date"].dt.to_period("M").astype(str)

# --- Filtres ---
st.sidebar.markdown("---")
min_date, max_date = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input(
    "Période",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

categories = st.sidebar.multiselect(
    "Catégories",
    options=sorted(df["categorie"].unique()),
    default=sorted(df["categorie"].unique())
)

if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    df = df[(df["date"] >= start) & (df["date"] <= end)]

df = df[df["categorie"].isin(categories)]

# --- En-tête ---
st.title("💸 Dashboard de Dépenses Personnelles")
st.caption("Importez vos relevés bancaires (CSV) et visualisez vos habitudes de dépenses.")

# --- Indicateurs clés ---
col1, col2, col3, col4 = st.columns(4)
total_depenses = df[df["montant"] < 0]["montant"].sum()
total_revenus = df[df["montant"] > 0]["montant"].sum()
solde = total_revenus + total_depenses
nb_transactions = len(df)

col1.metric("Total dépensé", f"{abs(total_depenses):,.2f} CHF")
col2.metric("Total revenus", f"{total_revenus:,.2f} CHF")
col3.metric("Solde net", f"{solde:,.2f} CHF", delta=f"{solde:,.2f} CHF")
col4.metric("Transactions", nb_transactions)

st.markdown("---")

# --- Graphiques ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Répartition par catégorie")
    depenses_par_cat = (
        df[df["montant"] < 0]
        .groupby("categorie")["montant"]
        .sum()
        .abs()
        .sort_values(ascending=False)
        .reset_index()
    )
    if not depenses_par_cat.empty:
        fig_pie = px.pie(
            depenses_par_cat,
            values="montant",
            names="categorie",
            hole=0.4
        )
        fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Pas de dépenses sur la période sélectionnée.")

with col_right:
    st.subheader("Évolution mensuelle")
    evolution = (
        df.groupby(["mois", "categorie"])["montant"]
        .sum()
        .reset_index()
    )
    evolution_depenses = evolution[evolution["montant"] < 0].copy()
    evolution_depenses["montant"] = evolution_depenses["montant"].abs()
    if not evolution_depenses.empty:
        fig_bar = px.bar(
            evolution_depenses,
            x="mois",
            y="montant",
            color="categorie",
            barmode="stack"
        )
        fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Pas de données sur la période sélectionnée.")

st.markdown("---")

# --- Tableau détaillé ---
st.subheader("📋 Détail des transactions")
st.dataframe(
    df.sort_values("date", ascending=False)[["date", "description", "categorie", "montant"]],
    use_container_width=True,
    hide_index=True
)

# --- Export ---
csv_export = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Télécharger les données filtrées (CSV)",
    csv_export,
    "depenses_filtrees.csv",
    "text/csv"
)

st.markdown("---")
st.caption("Démo créée avec Streamlit, Pandas et Plotly — projet portfolio.")
