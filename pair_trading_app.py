import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import yfinance as yf

st.set_page_config(page_title="Pair Trading Options", layout="wide")

st.title(" Pair Trading sur Options - Interface Streamlit")

# --- Paramètres utilisateur ---
st.sidebar.header("Paramètres")
tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN', 'NVDA', 'TSLA']
ticker1 = st.sidebar.selectbox("Sélectionnez le premier actif", tickers, index=2)
ticker2 = st.sidebar.selectbox("Sélectionnez le second actif", tickers, index=3)
rolling_window = st.sidebar.slider("Fenêtre de moyenne mobile (jours)", 5, 60, 20, step=5)
frais_transaction = st.sidebar.number_input("Frais par opération (USD)", 0.0, 1.0, 0.05, step=0.01)
debut = st.sidebar.date_input("Date de début", pd.to_datetime("2024-01-01"))
fin = st.sidebar.date_input("Date de fin", pd.to_datetime("2024-04-01"))

# --- Données simulées d'options ---
dates = pd.bdate_range(start=debut, end=fin)
np.random.seed(42)
price1 = pd.Series(5 + np.cumsum(np.random.normal(0, 0.1, len(dates))), index=dates)
price2 = pd.Series(5 + np.cumsum(np.random.normal(0, 0.1, len(dates))), index=dates)

options_df = pd.DataFrame({
    f'{ticker1}_Call': price1,
    f'{ticker2}_Call': price2
})

options_df['Spread'] = options_df[f'{ticker1}_Call'] - options_df[f'{ticker2}_Call']
spread_mean = options_df['Spread'].rolling(window=rolling_window).mean()
spread_std = options_df['Spread'].rolling(window=rolling_window).std()
options_df['Z_Score'] = (options_df['Spread'] - spread_mean) / spread_std

options_df['Signal'] = 0
options_df.loc[options_df['Z_Score'] > 1, 'Signal'] = -1
options_df.loc[options_df['Z_Score'] < -1, 'Signal'] = 1
options_df['Position'] = options_df['Signal'].shift()
options_df['Spread_Return'] = options_df['Spread'].diff()
options_df['PnL'] = options_df['Position'] * options_df['Spread_Return']
options_df['PnL_after_costs'] = options_df['PnL'] - frais_transaction * (options_df['Signal'] != 0).astype(int)
options_df['Cumulative_PnL'] = options_df['PnL_after_costs'].cumsum()

# --- Indicateurs ---
adf_stat, adf_pvalue = adfuller(options_df['Spread'].dropna())[:2]
daily_return = options_df['PnL_after_costs'].mean()
volatility = options_df['PnL_after_costs'].std()
sharpe_ratio = (daily_return / volatility) * np.sqrt(252) if volatility != 0 else np.nan
max_drawdown = (options_df['Cumulative_PnL'].cummax() - options_df['Cumulative_PnL']).max()
num_trades = (options_df['Signal'] != 0).sum()
win_rate = (options_df['PnL_after_costs'] > 0).sum() / num_trades if num_trades > 0 else np.nan

# --- Affichage ---
st.subheader("Résultats de la stratégie")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
col2.metric("Max Drawdown", f"{max_drawdown:.2f} USD")
col3.metric("Trades", f"{num_trades}")
col4.metric("Win Rate", f"{win_rate:.2%}")

st.markdown("### Test de stationnarité (ADF)")
st.write(f"Statistique ADF : {adf_stat:.4f}, p-value : {adf_pvalue:.4f}")

st.markdown("### Évolution du Spread")
fig1, ax1 = plt.subplots()
ax1.plot(options_df.index, options_df['Spread'], label='Spread')
ax1.plot(options_df.index, spread_mean, label='Moyenne mobile')
ax1.set_title('Spread entre options')
ax1.legend()
st.pyplot(fig1)

st.markdown("### Z-Score du Spread")
fig2, ax2 = plt.subplots()
ax2.plot(options_df.index, options_df['Z_Score'], label='Z-Score')
ax2.axhline(1, color='red', linestyle='--')
ax2.axhline(-1, color='green', linestyle='--')
ax2.set_title('Z-Score et seuils de trading')
ax2.legend()
st.pyplot(fig2)

st.markdown("### PnL Cumulé")
fig3, ax3 = plt.subplots()
ax3.plot(options_df.index, options_df['Cumulative_PnL'], label='PnL Cumulé', color='black')
ax3.set_title('Performance de la stratégie')
ax3.legend()
st.pyplot(fig3)

st.markdown("---")
st.markdown("Application Streamlit construite pour un projet de Pair Trading sur options.\nDonnées simulées avec marche aléatoire.")
