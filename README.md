# 💸 Dashboard de Dépenses Personnelles

Application web interactive qui permet de visualiser et analyser des dépenses
personnelles à partir d'un relevé bancaire au format CSV.

## Fonctionnalités

- **Import CSV** : glisser-déposer un relevé de compte (date, description, montant)
- **Catégorisation automatique** : les transactions sont classées par mots-clés
  (alimentation, transport, logement, loisirs, shopping, santé...)
- **Filtres interactifs** : période et catégories
- **Indicateurs clés** : total dépensé, revenus, solde net, nombre de transactions
- **Graphiques** : répartition par catégorie (camembert) et évolution mensuelle
  (barres empilées), avec Plotly
- **Export** : téléchargement des données filtrées en CSV

## Stack technique

- [Streamlit](https://streamlit.io/) — framework web Python
- [Pandas](https://pandas.pydata.org/) — traitement des données
- [Plotly](https://plotly.com/python/) — visualisations interactives

## Lancer le projet en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

L'application est accessible sur `http://localhost:8501`.

## Format du fichier CSV attendu

| date       | description        | montant |
|------------|---------------------|---------|
| 2026-01-15 | Migros              | -45.20  |
| 2026-01-20 | Salaire job étudiant| 850.00  |

- `date` : format `AAAA-MM-JJ`
- `description` : libellé de la transaction
- `montant` : négatif pour une dépense, positif pour un revenu

Un fichier `sample_data.csv` avec des données d'exemple est inclus pour tester
l'application sans rien importer.

## Déploiement

Déployable gratuitement sur [Streamlit Community Cloud](https://streamlit.io/cloud)
en connectant ce dépôt GitHub.

---

*Projet portfolio — développé comme démonstration de compétences en
visualisation de données et développement web avec Python.*
# Personal-Depenses
