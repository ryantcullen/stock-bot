import yfinance as yf
import pandas as _pd
import numpy as np
import pylab as pl


ticker = ' '
ticker = input("Enter ticker: ")

while ticker != 'exit':

    ticker_info = yf.Ticker(ticker)
    price_history = ticker_info.history(start="2010-12-1",  end="2020-12-12")

    opens = price_history['Open']
    closes = price_history['Close']
    old_price = (opens[0] + closes[0])/2
    prices = []

    days = opens.size
    for i in range(days):
        price = (opens[i] + closes[i])/2
        prices.append(price)

    x = np.linspace(0, days, days)
    y = prices
    pl.plot(x,y)


    pl.show()
    ticker = input("Enter ticker: ")