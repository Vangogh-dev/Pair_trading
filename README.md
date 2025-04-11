# Pair Trading sur Options avec Python & Streamlit

Ce projet a été développé dans le cadre d'une initiative personnelle en école de commerce avec pour objectif de modéliser, backtester et visualiser une stratégie de **pair trading sur options**. Il s'adresse à un public avec un intérêt pour la **finance quantitative**, les **produits dérivés** et le **développement Python appliqué à la finance**.

## 🔍 Objectifs
- Sélectionner dynamiquement des paires d'actifs fortement corrélés
- Simuler ou importer les prix d'options de ces actifs
- Appliquer une stratégie de **mean reversion** sur le spread des options
- Backtester les performances et analyser les résultats (PnL, Sharpe, Drawdown)
- Visualiser l'ensemble de manière interactive avec **Streamlit**

## 🧰 Technologies
- **Python 3.9+**
- `pandas`, `numpy`, `matplotlib`, `plotly`, `scipy`, `statsmodels`
- `yfinance` pour les données des sous-jacents
- `streamlit` pour l'interface utilisateur

## 🗂 Structure du projet

```
📁 pair-trading-options
├── pair_trading_app.py         # Interface Streamlit complète
├── pair_trading_options.ipynb  # Notebook d'analyse et backtest
├── README.md                   # Documentation du projet
└── requirements.txt            # Dépendances Python
```

## 🚀 Lancer l'application

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Lancer Streamlit
```bash
streamlit run pair_trading_app.py
```

##  Fonctionnalités de l'application
- **Sélection interactive** des actifs (ticker1 vs ticker2)
- **Paramétrage personnalisé** de la fenêtre de rolling et des frais
- **Backtest complet** avec signaux long/short, PnL, spread, Z-score
- **Tests statistiques** (ADF stationnarité du spread)
- **Visualisations dynamiques** (Spread, Z-Score, PnL Cumulé)

##  Indicateurs calculés
- **Sharpe Ratio** (annualisé)
- **Max Drawdown**
- **Taux de succès des trades**
- **Nombre de signaux générés**

##  Données
Les prix d'options sont **simulés** par une marche aléatoire, faute d'accès gratuit et stable à des APIs professionnelles. Toutefois, le script est modulaire pour intégrer de vraies données si disponibles.

##  Améliorations futures
- Intégration de données réelles via une API professionnelle (Bloomberg incoming)
- Ajout d'une couche Machine Learning pour la génération des signaux


