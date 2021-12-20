import pandas as pd
import numpy as np
from scipy.optimize import minimize, Bounds, minimize_scalar, LinearConstraint, differential_evolution
from datetime import date
import warnings
warnings.filterwarnings('ignore')

#create sell function

def sell(Samount, price, Tbalance, Tbtc):
    fee = 0.001
    BTCSamount = Samount * price * (1-fee)
    Tbalance = Tbalance + BTCSamount
    Tbtc = Tbtc - Samount
    return Tbalance, Tbtc

#create buy function

def buy(Bamount,price, Tbalance, Tbtc):
    fee = 0.001
    BTCamount = Bamount / (price*(1+fee))
    Tbalance = Tbalance - Bamount
    Tbtc = Tbtc + BTCamount
    return Tbalance, Tbtc

#create risk level based strategy

def Ratio(avg, signal, price, Tbalance, Tbtc):

    if signal == "S":
        if Tbtc != 0:
            if 0.5 < avg <= 0.6:
                Samount = 0*Tbtc/10
                Tbalance,Tbtc = sell(Samount, price, Tbalance, Tbtc)
            elif 0.6 < avg <= 0.7:
                Samount = 0*Tbtc/10
                Tbalance, Tbtc = sell(Samount, price, Tbalance, Tbtc)
            elif 0.7 < avg <= 0.8:
                Samount = 0*Tbtc/10
                Tbalance, Tbtc = sell(Samount, price, Tbalance, Tbtc)
            elif 0.8 < avg <= 0.9:
                Samount = 0*Tbtc/10
                Tbalance, Tbtc = sell(Samount, price, Tbalance, Tbtc)
            elif avg > 0.9:
                Samount = 10*Tbtc/10
                Tbalance, Tbtc = sell(Samount, price, Tbalance, Tbtc)

    elif signal == "B":

        if Tbalance != 0:
            Bamount = Tbalance/10
            if 0.4 < avg <= 0.5:
                Bamount = min(Bamount * 0, Tbalance)
                Tbalance, Tbtc = buy(Bamount, price, Tbalance, Tbtc)
            elif 0.3 < avg <= 0.4:
                Bamount = min(Bamount * 0, Tbalance)
                Tbalance, Tbtc = buy(Bamount, price, Tbalance, Tbtc)
            elif 0.2 < avg <= 0.3:
                Bamount = min(Bamount * 0,Tbalance)
                Tbalance, Tbtc = buy(Bamount, price, Tbalance, Tbtc)
            elif 0.1 < avg <= 0.2:
                Bamount = min(Bamount * 0,Tbalance)
                Tbalance, Tbtc = buy(Bamount, price, Tbalance, Tbtc)
            elif avg < 0.1:
                Bamount = min(Bamount * 10,Tbalance)
                Tbalance, Tbtc = buy(Bamount, price, Tbalance, Tbtc)

    elif signal == "W":
        pass

    return Tbalance, Tbtc

#This function returns the portfolio value assuming we use the above strategy

def return_calc(x1, x2, x3, x4):

    df = pd.read_csv('gdrive/MyDrive/RiskData/OldRiskIndicators.csv',usecols=["Date", "Value", "MA", "Puelle", "Sharpe", "Power"])

    df["Date"] = pd.to_datetime(df["Date"])

    df["avg"] = x1*df["MA"] + x2*df["Puelle"] + x3*df["Sharpe"] + x4*df["Power"] 
    

    df = df[df.Date > pd.to_datetime(date(2015, 1, 7))]
    df = df[df.Date < pd.to_datetime(date(2021, 11, 30))]

    df = df.set_index("Date").resample('W').mean()

    df["Tbal"] = ""
    df["Tbal"].iloc[0] = 100000

    df["Tbtc"] = ""
    df["Tbtc"].iloc[0] = 0

    df["Total"] = ""
    df["Total"].iloc[0] = ((df['Value'].iloc[0]) * (df['Tbtc'].iloc[0])) + df['Tbal'].iloc[0]

    

    for i in range(1, df.shape[0]):
        if df["avg"][i] <= 0.5:
            signal = "B"
        elif df["avg"][i] > 0.5:
            signal = "S"
        else:
            signal ="W"

        df["Tbal"][i] = Ratio(avg=df["avg"][i], signal=signal, price=df["Value"][i], Tbalance=df["Tbal"][i-1], Tbtc=df["Tbtc"][i-1])[0]
        df["Tbtc"][i] = Ratio(avg=df["avg"][i], signal=signal, price=df["Value"][i], Tbalance=df["Tbal"][i-1], Tbtc=df["Tbtc"][i-1])[1]
        df["Total"][i] = ((df['Value'][i])*(df['Tbtc'][i])) + df['Tbal'][i]
    
    DCArtn = df["Total"].iloc[-1]

    df["Hodl"] = ""
    df["Hodl"] = (df["Tbal"].iloc[0] / df['Value'].iloc[1]) * df['Value']
    df["Hodl"].iloc[0] = 100000

    BuyHoldRtn = df["Hodl"].iloc[-1]

    return DCArtn, BuyHoldRtn

#Perform optimisation

def objective(x):
  x1 = x[0]
  x2 = x[1]
  x3 = x[2]
  x4 = x[3]
  return -return_calc(x1,x2,x3,x4)[0]

bounds = Bounds([0,0,0,0],[1,1,1,1])

sol = differential_evolution(objective, bounds)

np.set_printoptions(formatter={'float_kind':'{:f}'.format})

print(sol)

print(sol.x)

print(return_calc(0.104691, 0.635181, 0.105839, 0.155178)[0])
