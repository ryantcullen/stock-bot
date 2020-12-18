import yfinance as yf
import pandas as _pd
import numpy as np
import matplotlib.pyplot as plt


class Portfolio:

    def __init__(self, capital, shares, initial_price):  
        self.capital = capital
        self.shares = shares
        self.initial_price = initial_price
        self.portfolio_value = self.capital + self.shares*self.initial_price

    def Buy(self):
        if(price < self.capital):
            self.shares += 1
            self.capital -= price
            self.portfolio_value = self.capital + self.shares*price
    
    def Sell(self):
        if(self.shares > 0):
            self.shares -= 1
            self.capital += price
            self.portfolio_value = self.capital + self.shares*price


class MovingAverage:
    
    def __init__(self, window):  
        self.price_sum = 0
        self.price_list = []
        self.result = 0
        self.window = window

    def CalculateSum(self):
        if i < self.window:
            self.price_list.append(price)
            self.price_sum += price
        else:
            self.price_list.append(price)
            self.price_sum += price
            self.price_sum -= self.price_list[0]
            self.price_list.pop(0)

    def CalculateAverage(self):
        if i == 0:
            self.result = price
        elif i < self.window:
            self.result = self.price_sum/(i+1)
        else:
            self.result = self.price_sum/self.window


while True:

    ticker = input("Enter ticker: ")
    if ticker == 'exit':
        break

    ticker_info = yf.Ticker(ticker)
    price_history = ticker_info.history(start="2015-9-5",  end="2020-12-11")

    opens = price_history['Open']
    closes = price_history['Close']
    averages = []
    days = opens.size
    prices = []
    price = (opens[0] + closes[0])/2
    fig = plt.figure()

    portfolio = Portfolio(0, 100, price)
    moving_average = MovingAverage(40)

    for i in range(days):
        
        price = (opens[i] + closes[i])/2
        prices.append(price)
        
        moving_average.CalculateSum()
        moving_average.CalculateAverage()
        averages.append(moving_average.result)
    
    print("Original cost of 100 shares: " + str(prices[days - 1] * 100))
    print("Capital: " + str(portfolio.capital))
    print("Shares: " + str(portfolio.shares))
    print("Portfolio value: " + str(portfolio.portfolio_value))

    x = np.linspace(0, days, days)
    plt.plot(x,prices)
    plt.plot(x,averages)

    plt.show()


    


