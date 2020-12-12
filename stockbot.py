import yfinance as yf
import pandas as _pd
import numpy as np
import pylab as pl


ticker = ' '
priorUps = 0


while True:
    ticker = input("Enter ticker: ")
    if ticker == 'exit':
        break
    perc = float(input("Enter percentage: "))
    day_range = int(input("Enter number of trading days: "))
    trading_start = input("Enter start date (y-m-d): ")
    trading_end = input("Enter start date (y-m-d): ")

    ticker_info = yf.Ticker(ticker)
    price_history = ticker_info.history(start=trading_start,  end=trading_end)

    opens = price_history['Open']
    closes = price_history['Close']
    old_price = (opens[0] + closes[0])/2
    prices = []

    days = opens.size
    for i in range(days):
        price = (opens[i] + closes[i])/2
        prices.append(price)

        if (i % day_range) == 0:
            difference = price - old_price
            percent_change = (difference/old_price)*100
            if percent_change > perc:
                print(i)
                priorUps += 1
            old_price = price

    x = np.linspace(0, days, days)
    y = prices
    pl.plot(x,y)

    print(priorUps)
    pl.show()
    
    priorUps = 0


