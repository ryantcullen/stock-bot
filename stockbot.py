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
            self.capital += int(self.shares/2)*price
            self.shares -= int(self.shares/2)
            plt.plot([i], [price], marker='o', markersize=4, color="red")
        
        self.portfolio_value = self.capital + (self.shares*price)
    


class MovingAverage:
    """ Moving Average 
    
    Calculates the moving average of a stock proce at a given time.


    """

    def __init__(self, window, portfolio):
        """ Inits a MovingAverage object """  
        self.window = window
        self.portfolio = portfolio
        
        self.price_sum = 0
        self.price_list = []

        self.average = 0
        self.avg_sum = 0
        self.avg_list = []   
        self.double_average = 0
        self.percent_difference = 0

        self.slope = 0
        self.slope_sum = 0
        self.avg_slope = 0
        self.slopes = []
        self.avg_slopes = []
        self.concavity = 0 

        self.above = False
        self.flipped = False

        
        

    def CalculateAverage(self, value, window):

        """ Calculates the value for the moving average over the last (window) days """

        value_list.append(value)
        value_sum += value

        if i < self.window:
            average = self.value_sum/(i+1)
            value_list.append(value)
        else:
            self.value_sum -= self.value_list[0]
            self.value_list.pop(0)
            self.average = self. value_sum/window
    
    def GetInfo(self):
        """ Gets the slope and concavity information """

        # calculate slope
        if i > 1:
            self.slope = averages[i] - averages[i - 1]
        self.slopes.append(self.slope)
        self.slope_sum += self.slope
        
        # percent deviation from the mean
        difference = price - averages[i]
        self.percent_difference = difference/averages[i]

        # calculate average slope and concavity
        if i < self.window:
            self.avg_slope = self.slope_sum/(i+1)
            self.avg_slopes.append(self.avg_slope)
            self.concavity = self.avg_slopes[i] - self.avg_slopes[0]
        else:
            self.slope_sum -= self.slopes[0]
            self.slopes.pop(0)
            self.avg_slope = self.slope_sum/self.window
            self.avg_slopes.append(self.avg_slope)
            self.avg_slopes.pop(0)
            self.concavity = self.avg_slopes[self.window - 1] - self.avg_slopes[int(self.window/4)]


        # check if we flip over average line
        if price > averages[i]:
            if self.above == False: 
                self.above = True
                self.flipped = True
            else: self.flipped = False
        else:
            if self.above:
                self.above = False
                self.flipped = True
            else: self.flipped = False
 
        

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
    averages2 = []
    averages = []
    double_averages = []
    double_averages2 = []
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
    moving_average2 = MovingAverage(10, portfolio)


    # iterate over the history of the stock
    for i in range(days):
        
        # calculate the daily average proce and add it to the list of prices
        price = closes[i]
        prices.append(price)
        
        # calculate the current moving average and add it to the list of moving averages
        moving_average.CalculateAverages()
        moving_average2.CalculateAverages()

        averages.append(moving_average.average)
        averages2.append(moving_average2.average)

        double_averages.append(moving_average.double_average)
        double_averages2.append(moving_average2.double_average)

        moving_average.GetInfo()

        # decide if we buy, sell, or hold
        # moving_average.BuySell()
        # portfolio.Order(value)
    
    
    # did we win?
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
    plt.plot(x, averages)
    plt.plot(x, double_averages)
    plt.plot(x, double_averages2)
    plt.show()


    


