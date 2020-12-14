import yfinance as yf
import pandas as _pd
import numpy as np
import matplotlib.pyplot as plt


def make_functions(i, price, length, slope):
    
    resistance = []
    support = []
    xvals = np.linspace(i, i + length - 1, length)

    #THESE NEED TO BE ADJUSTED ACCORDING TO STOCK TO IMPROVE ALGORITHM
    offset = (price/100)/10
    floor = (price/100) * 1.2

    for n in range(length):
        resistance.append(price - n*slope + offset)

    for n in range(length):
        support.append(price - n*slope - floor + offset)

    return resistance, support, xvals

while True:
    ticker = input("Enter ticker: ")
    if ticker == 'exit':
        break
    perc = float(input("Enter prior uptrend percentage: "))
    day_range = int(input("Enter number of trading days: "))
    channel_range = int(input("Enter channel range: "))


    flagpole = False
    counter = 0
    makeFuncs = False

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
        slope = closes[days-1]/5000
        

        if flagpole:
            if makeFuncs:
                resistance, support, xvals = make_functions(i, price, channel_range, slope)
                makeFuncs = False
            

            if price > resistance[counter]:
                if counter > (channel_range/5):
                    flagpole = False
                    counter = channel_range
                else:
                    flagpole = False
                    counter = 0
            elif price < support[counter]:
                if counter > (channel_range/5):
                    flagpole = False
                    counter = 0
                else:
                    counter += 1
            else: counter += 1
                

            if counter > channel_range - 1:
                flagpole = False
                counter = 0
                plt.plot(xvals, resistance)
                plt.plot(xvals, support)
                print("Found Flag")
                print(i)
        
        if i < day_range:
            initial_price = prices[0]
            pole_price = prices[0]
        else:
            initial_price = prices[i - day_range]
            pole_price = prices[i - int(day_range/10)]
        
        runup_difference = price - initial_price
        pole_difference = price - pole_price
        runup = (runup_difference/initial_price)*100
        pole = (pole_difference/pole_price)*100
        
        if (runup > perc) & (pole > (perc/2)):
            if flagpole != True:
                flagpole = True
                makeFuncs = True


    x = np.linspace(0, days, days)
    y = prices
    plt.plot(x,y)

    plt.show()


    


