import yfinance as yf
import pandas as _pd
import numpy as np
import matplotlib.pyplot as plt


def make_functions(i, price, channel):
    
    resistance = []
    support = []
    xvals = np.linspace(i, i + channel - 1, channel)

    #THESE NEED TO BE ADJUSTED ACCORDING TO STOCK TO IMPROVE ALGORITHM
    offset = (price/100)/20
    floor = (price/100)
    slope = 0.02

    for n in range(channel):
        resistance.append(price - n*slope + offset)

    for n in range(channel):
        support.append(price - n*slope - floor + offset)

    return resistance, support, xvals

while True:
    ticker = input("Enter ticker: ")
    if ticker == 'exit':
        break
    perc = float(input("Enter prior uptrend percentage: "))
    day_range = int(input("Enter number of trading days: "))
    channel_range = int(input("Enter channel range: "))
    # trading_start = input("Enter start date (y-m-d): ")
    # trading_end = input("Enter start date (y-m-d): ")

    flagpole = False
    counter = 0
    makeFuncs = False
    resistance = []
    support = []
    xvals = []

    ticker_info = yf.Ticker(ticker)
    price_history = ticker_info.history(start="2015-9-5",  end="2020-12-11")

    opens = price_history['Open']
    closes = price_history['Close']
    days = opens.size
    prices = []

    fig = plt.figure()
    
    #MAKE SEPARATE FUNCTION
    for i in range(days):
        
        price = (opens[i] + closes[i])/2
        prices.append(price)
        

        if flagpole:
            if makeFuncs:
                resistance, support, xvals = make_functions(i, price, channel_range)
                makeFuncs = False
            

            if price > resistance[counter]:
                if counter > (channel_range/2):
                    flagpole = False
                    counter = channel_range
                else:
                    flagpole = False
                    counter = 0
            elif price < support[counter]:
                flagpole = False
                counter = 0
            else: counter += 1
                


            if counter > channel_range - 1:
                flagpole = False
                counter = 0
                plt.plot(xvals, resistance)
                plt.plot(xvals, support)
                print("Found Flag")
                print(i)
        
        if i < day_range:
            old_price = prices[0]
        else:
            old_price = prices[i - day_range]
        
        difference = price - old_price
        percent_change = (difference/old_price)*100
        
        if percent_change > perc:
            if flagpole != True:
                flagpole = True
                makeFuncs = True


    x = np.linspace(0, days, days)
    y = prices
    plt.plot(x,y)

    plt.show()


    


