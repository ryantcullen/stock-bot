import yfinance as yf
import pandas as _pd
import numpy as np
import pylab as pl


msft = yf.Ticker("MSFT")
ticker = msft.history(start="2010-12-1",  end="2020-12-12")
ticker = ticker.reset_index()

opens = ticker['Open']
closes = ticker['Close']
daily_averages = []

for i in range(opens.size):
    average = (opens[i] + closes[i])/2
    daily_averages.append(average)

x = np.linspace(0, opens.size, opens.size)
y = daily_averages
pl.plot(x,y)

pl.show()