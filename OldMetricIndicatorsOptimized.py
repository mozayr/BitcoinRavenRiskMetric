!pip install quandl 
import pandas as pd
import quandl as quandl
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import date
import warnings
warnings.filterwarnings('ignore')

#df = pd.read_csv('gdrive/MyDrive/RiskData/BTC_FullHistory.csv',usecols=["Date", "Value"])

df = quandl.get("BCHAIN/MKPRU", api_key="FYzyusVT61Y4w65nFESX").reset_index()

df["Date"] = pd.to_datetime(df["Date"])
df.sort_values(by="Date", inplace=True)
df = df[df["Value"] > 0]

#200DayMA

df['365'] = df['Value'].rolling(200).mean().dropna()
df["MA"] = (np.log(df.Value) - np.log(df["365"])) * df.index**0.527864075

df["MA"] = (df["MA"] - df["MA"].cummin()) / (df["MA"].cummax() - df["MA"].cummin())

#PuelleMultiple

df["btcIssuance"] = 7200 / 2 ** (np.floor(df.index / 1458))
df["usdIssuance"] = df["btcIssuance"] * df["Value"]
df['MAusdIssuance'] = df['usdIssuance'].rolling(205).mean().dropna()
df["Puelle"] = (np.log(df["usdIssuance"]) - np.log(df["MAusdIssuance"])) * df.index**0.463434152111863

df["Puelle"] = (df["Puelle"] - df["Puelle"].cummin()) / (df["Puelle"].cummax() - df["Puelle"].cummin())

#Sharpe

df["Return%"] = df["Value"].pct_change() * 100
df["365Return%MA-1"]= df["Return%"].rolling(195).mean().dropna() - 1
df["365Return%STD"] = df["Return%"].rolling(195).std().dropna()
df["Sharpe"] = (df["365Return%MA-1"] / df["365Return%STD"])*df.index**0.854101994086665

df["Sharpe"] = (df["Sharpe"] - df["Sharpe"].cummin()) / (df["Sharpe"].cummax() - df["Sharpe"].cummin())

#PowerLaw

def ossValue(days):
    X = np.array(np.log10(df.index[:days])).reshape(-1, 1)
    y = np.array(np.log10(df.Value[:days]))
    reg = LinearRegression().fit(X, y)
    values = reg.predict(X)
    return values[-1]

df["Power"] = (np.log10(df.Value) - [ossValue(x + 1) for x in range(len(df))])*df.index**0.91

df["Power"] = (df["Power"] - df["Power"].cummin()) / (df["Power"].cummax() - df["Power"].cummin())

#df["avg"] = 0.105*df["MA"] + 0.6*df["Puelle"] + 0.105*df["Sharpe"] + 0.155*df["Power"] 

print(df)
