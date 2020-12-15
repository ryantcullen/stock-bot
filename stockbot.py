import yfinance as yf
import pandas as _pd
import numpy as np
import matplotlib.pyplot as plt


flagpole = False
make_flag = False
counter = 0
resistance = []
support = []
xvals = []

def MakeChannel(i, price, length):
    
    resistance = []
    support = []
    xvals = np.linspace(i, i + length - 1, length)
    slope = closes[days-1]/5000

    offset = (price/100)/10
    floor = (price/100) * 1.2

    for n in range(length):
        resistance.append(price - n*slope + offset)

    for n in range(length):
        support.append(price - n*slope - floor + offset)

    return resistance, support, xvals

def BullFlags():
        global flagpole
        global make_flag
        global counter
        global resistance
        global support
        global xvals

        if i < day_range:
            initial_price = prices[0]
            pole_price = prices[0]
        else:
            initial_price = prices[i - day_range]
            pole_price = prices[i - int(day_range/10)]
        
        if flagpole != True:
            runup_difference = price - initial_price
            pole_difference = price - pole_price
            runup = (runup_difference/initial_price)*100
            pole = (pole_difference/pole_price)*100

            if (runup > perc) & (pole > (perc/2)):
                flagpole = True
                make_flag = True

        if flagpole:
            if make_flag:
                resistance, support, xvals = MakeChannel(i, price, channel_range)
                make_flag = False
            

            if price < support[counter]:
                if counter > (channel_range/2):
                    flagpole = False
                    counter = 0
                else:
                    counter += 1
            else: counter += 1

            if counter > channel_range - 1:
                flagpole = False
                counter = 0
                if price > support[counter]:
                    plt.plot(xvals, resistance)
                    plt.plot(xvals, support)
                    print("Found Flag")
                    print(i)

while True:

    ticker = input("Enter ticker: ")
    if ticker == 'exit':
        break
    perc = float(input("Enter prior uptrend percentage: "))
    day_range = int(input("Enter number of trading days: "))
    channel_range = int(input("Enter channel range: "))

    ticker_info = yf.Ticker(ticker)
    price_history = ticker_info.history(start="2015-9-5",  end="2020-12-11")

    opens = price_history['Open']
    closes = price_history['Close']
    days = opens.size
    prices = []
    fig = plt.figure()

    for i in range(days):
        price = (opens[i] + closes[i])/2
        prices.append(price)
        BullFlags()
    
    

    x = np.linspace(0, days, days)
    y = prices
    plt.plot(x,y)

    plt.show()


    


