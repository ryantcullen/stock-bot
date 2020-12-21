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
        self.run = 0

    def Decide(self, f1, f2, f3):
        
        offset = averages[i]/600

        if(f1.concavity > 0.3):
            if price < triple_averages[i]:
                self.run = 0
                return 10
        if(f1.concavity < -0.3):
            if price > triple_averages[i]:
                self.run = 0
                return -2

        # day trade, when done buy all stock possible
        # TODO: adjust avg slope reqs based on price
        # TODO: Only sell for a profit?

        self.run += 1
        if(f3.avg_slope < 0.02):
            if(f3.concavity) < 0:
                if price > averages[i] + offset:
                    if(f1.avg_slope < 0.05):
                        self.run = 0
                        return -1
            else:
                if price < averages[i] - offset:
                    if(f1.avg_slope > 0):
                        if(f1.concavity > -0.2):
                            self.run = 0
                            return 0
        return self.run



        # peaks / troughs, maybe need to sort by average concavity






            
        


    def Order(self, value, n):
        """ Executes a buy order of n shares if value = 2, a sell order of
            n shares if value = 0, and holds the shares if value = 1.
        """


        # buy n
        if value == 0:
            counter = 0  
            while self.capital >= price:
                self.capital -= price
                counter += 1
                if counter == n:
                    break
            self.shares += counter
            plt.plot([i], [price], marker='o', markersize=4, color="limegreen")

        # sell n
        elif value == -1:
            if self.shares > n:
                self.capital += n*price
                self.shares -= n
            plt.plot([i], [price], marker='o', markersize=4, color="red")

        # buy all
        if value == 10:
            counter = 0  
            while self.capital >= price:
                self.capital -= price
                counter += 1
            self.shares += counter
            plt.plot([i], [price], marker='o', markersize=4, color="limegreen")

        # sell all
        elif value == -2:
            self.capital += self.shares*price
            self.shares = 0
            plt.plot([i], [price], marker='o', markersize=4, color="red")
    
    def PortoflioValue(self):
        self.portfolio_value = self.capital + (self.shares*price)
        return self.portfolio_value


    


class MovingAverage:
    """ Moving Average 
    
    Calculates the moving average of a stock proce at a given time.


    """

    def __init__(self, portfolio):
        """ Inits a MovingAverage object """  
        self.portfolio = portfolio
        self.percent_difference = 0

        self.slope = 0
        self.slope_sum = 0
        self.avg_slope = 0
        self.slopes = []
        self.concavity = 0 
        self.concavity_sum = 0
        self.avg_concavity = 0
        self.concavities = []

        self.above = False
        self.flipped = False
        self.runcrash = False


    def CalculateAverage(self, value_list, window):

        """ Calculates the value for the moving average over the last (window) days """
        
        if i < (window - 1):
            edge = window - (i + 1)
        else: edge = 0
        
        if i == 0:
            value_sum = price
        else:
            value_sum = 0
            for n in range(window - edge):
                value_sum += value_list[i - n]
            
        return value_sum/(window - edge)
    
    def GetInfo(self, function, window):
        """ Gets the slope and concavity information """
        
        # percent deviation from the mean
        difference = price - function[i]
        self.percent_difference = difference/function[i]

        # calculate slope
        if i > 1:
            self.slope = function[i] - function[i - 1]

        # calculate average slope and concavity
        self.slopes.append(self.slope)
        self.slope_sum += abs(self.slope)
        if i < window:
            self.avg_slope = self.slope_sum/(i+1)
            self.concavity = self.slopes[i] - self.slopes[0]
        else:
            self.slope_sum -= abs(self.slopes[0])
            self.slopes.pop(0)
            self.avg_slope = self.slope_sum/window
            self.concavity = self.slopes[window - 1] - self.slopes[0]

        # calculate average concavity
        self.concavities.append(self.concavity)
        self.concavity_sum += self.concavity
        if i < window:
            self.avg_concavity = self.concavity_sum/(i+1)

        else:
            self.concavity_sum -= self.concavities[0]
            self.concavities.pop(0)
            self.avg_concavity = self.concavity_sum/window


        # check if we flip over average line
        if price > function[i]:
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
    price_history = ticker_info.history(start="2010-11-05",  end="2020-12-11")

    # assign lists for the open/close prices, the moving-average values, 
    # and the daily average prices.
    opens = price_history['Open']
    closes = price_history['Close']
    averages = []
    double_averages = []
    triple_averages = []
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

    # object to track moving averages
    moving_average = MovingAverage(portfolio)
    moving_double = MovingAverage(portfolio)
    moving_triple = MovingAverage(portfolio)


    # iterate over the history of the stock
    for i in range(days):
        
        # calculate the daily average proce and add it to the list of prices
        price = closes[i]
        prices.append(price)
        
        # calculate the current moving average and add it to the list of moving averages
        window = 30
        averages.append(moving_average.CalculateAverage(prices, window))
        double_averages.append(moving_double.CalculateAverage(averages, window))
        triple_averages.append(moving_triple.CalculateAverage(double_averages, window))
        
        moving_average.GetInfo(averages, 10)
        moving_double.GetInfo(double_averages, 20)
        moving_triple.GetInfo(triple_averages, 20)

        # decide if we buy, sell, or hold
        value = portfolio.Decide(moving_average, moving_double, moving_triple)
        portfolio.Order(value, 10)
    
    
    # did we win?
    control_value = starting_capital + (prices[days - 1] * starting_shares)
    algo_value = portfolio.PortoflioValue()

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
    plt.plot(x, prices)
    plt.plot(x, averages)
    plt.plot(x, double_averages)
    plt.plot(x, triple_averages)
    plt.show()


    


