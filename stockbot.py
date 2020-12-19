import yfinance as yf
import pandas as _pd
import numpy as np
import matplotlib.pyplot as plt


class Portfolio:
    """ Stock portfolio 
    
    Holds information about current buying power, equity, and overall value.

    Attributes:
        capital: starting cash.
        shares: starting number of shares.
        initial_price: the initial price of the stock.
        portfolio value: the overall value of the stock portfolio in $USD if the owner were to liquidate all assets.
    """

    def __init__(self, capital, shares, initial_price): 
        """Inits a Portfolio object""" 
        self.capital = capital
        self.shares = shares
        self.initial_price = initial_price
        self.portfolio_value = self.capital + self.shares*self.initial_price

    def Order(self, value):
        """ Executes a buy order of n shares if value = 2, a sell order of
            n shares if value = 0, and holds the shares if value = 1.
        """

        # buy
        if value == 2:
            count = 0  
            while self.capital >= price:
                self.capital -= price
                count += 1
            self.shares += count
            plt.plot([i], [price], marker='o', markersize=4, color="limegreen")

        # sell
        elif value == 0:
            self.capital += self.shares*price
            self.shares = 0
            plt.plot([i], [price], marker='o', markersize=4, color="red")
        
        self.portfolio_value = self.capital + (self.shares*price)
    


class MovingAverage:
    """ Moving Average  
    
    Calculates the moving average of a stock proce at a given time.

    Attributes:
        window: the number of days over which to calculate the moving average.
        price_sum: sum of the close prices from the last (window) days.
        price_list: list of the close prices from the last (window) days.
        result: the result of the moving average calculation.
        portfolio: the global portolio for use within the class
        above_average: boolean to check if the stock price has flipped over the moving average line (either up or down)

    """

    def __init__(self, window, portfolio):
        """ Inits a MovingAverage object """  
        self.window = window
        self.price_sum = 0
        self.price_list = []
        self.result = 0
        self.portfolio = portfolio
        self.above_average = True
        self.counter = 0
        
        

    def CalculateAverage(self):
        """ Calculates the value for the moving average over the last (window) days """
        if i < self.window:
            self.price_list.append(price)
            self.price_sum += price
        else:
            self.price_list.append(price)
            self.price_sum += price
            self.price_sum -= self.price_list[0]
            self.price_list.pop(0)
        
        if i == 0:
            self.result = price - 0.1
        elif i < self.window:
            self.result = self.price_sum/(i+1)
        else:
            difference = price - (self.price_sum/self.window)
            self.result = (self.price_sum/self.window)



    def BuySell(self):
        
        offset = averages[i]/200
        difference = abs(price - averages[i])
        perc = (difference/averages[i])
        t = 3
        min_slope = 0.02
        max_slope = 0.06

        if i < t:
            slope_rise = averages[i] - averages[0]
            slope = slope_rise/(i+1)
        else:
            slope_rise = averages[i] - averages[i- t]
            slope = slope_rise/t
        


        if i == 0:
            if price > averages[i]:
                self.above_average = True
            else: self.above_average = False

        if abs(slope) < min_slope:
            if price < (averages[i] - offset):
                return 2
            elif price > (averages[i] + offset):
                if slope < 0:
                    print(price)
                    print(i)
                    print(slope)
                    print("-----------")
                    return 0

        elif abs(slope) > max_slope:
            self.counter += 1
            if (price > (averages[i] - offset)):
                if self.above_average != True:
                    if self.counter > 40:
                        self.above_average = True
                        self.counter = 0
                        return 2
            elif (price < (averages[i] + offset)):
                if self.above_average != False:
                    if self.counter > 40:
                        self.above_average = False
                        self.counter = 0
                        return 0
        



        

"""
Main Loop

"""

while True:
    # input a ticker to track
    ticker = input("Enter ticker: ")
    if ticker == 'exit':
        break

    # get ticker information and price history
    ticker_info = yf.Ticker(ticker)
    price_history = ticker_info.history(start="2017-11-05",  end="2020-12-11")
    # assign lists for the open/close prices, the moving-average values, 
    # and the daily average prices.
    opens = price_history['Open']
    closes = price_history['Close']
    averages = []
    prices = []

    # calculates the inital price of the stock, and 
    # the number of days we are looking back in history
    price = closes[0]
    days = opens.size

    # initialize figure for plottingexit
    fig = plt.figure()

    # initialize the portfolio and moving average objects
    starting_capital = 0
    starting_shares = 100
    entry_price = starting_shares * price
    portfolio = Portfolio(starting_capital, starting_shares, price)
    moving_average = MovingAverage(30, portfolio)

    # iterate over the history of the stock
    for i in range(days):
        
        # calculate the daily average proce and add it to the list of prices
        price = closes[i]
        prices.append(price)
        
        # calculate the current moving average and add it to the list of moving averages
        moving_average.CalculateAverage()
        averages.append(moving_average.result)

        # decide if we buy, sell, or hold
        value = moving_average.BuySell()
        portfolio.Order(value)
    
    control_value = starting_capital + (prices[days - 1] * starting_shares)
    algo_value = portfolio.portfolio_value

    print(" ")
    print("Capital: " + str(portfolio.capital))
    print("Shares: " + str(portfolio.shares))
    print("Buy and Hold portfolio value: " + str(control_value))
    print("Returns: " + str(control_value - entry_price))
    print("Algorithm portfolio value: " + str(algo_value))
    print("Returns: " + str(algo_value - entry_price))
    print(" ")

    # plot the price history and moving average history
    x = list(range(0, days))
    plt.plot(x,prices)
    plt.plot(x,averages)
    plt.show()


    


