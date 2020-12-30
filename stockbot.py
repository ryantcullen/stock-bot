import yfinance as yf
import pandas as _pd
import numpy as np
import enum 
import matplotlib.pyplot as plt

"""
        Author: Ryan Cullen
"""

class Decisions(enum.Enum):
    sell = -1
    hold = 0
    buy = 1
    

class Portfolio:
   
    """ Stock portfolio 
    
    Holds information about current buying power, equity, and overall value.

    Attributes:
        capital: starting cash
        shares: starting number of shares
        portfolio value: the overall value of the stock portfolio in $USD if the owner were to liquidate all assets

    Funtions:
        Decide(): This is where the logic of when to buy, sell, or hold should go
        Order(): Used to execute a buy or sell order
        
    """
       
    def __init__(self, capital, shares): 
        """ Inits a Portfolio object """

        self.capital = capital
        self.shares = shares
        self.portfolio_value = self.capital + self.shares*price


    def Decide(self, f1, f2, f3, f4):   
        """ This is where the script decides to Buy, Sell, or Hold; Desgin your algorithm logic here. 
        
            Arguments (keep these or design your own):
                f1: 10 day moving average
                f2: 50 day moving average
                f3: 100 day moving average
                f3: 200 day moving average    
        """

        
        # here is the skeleton of an algorithm; fill in the logic for calculating the probability of profit and expected return

        prob_profit = 0
        expected_return = 0
        modifier = 0.5
        
        
       #                ~~~~   fill in code here   ~~~~


        position = self.OptimalPosition(expected_return, prob_profit, modifier)
        shares = abs(int(position/price))
        
        if position > 0:
            self.Order(Decisions.buy, shares)
        else:
            self.Order(Decisions.sell, shares)



    def Order(self, decision, n = -1):
        """ Executes a buy/sell order of n shares, or a buy/sell max order if no input for n.

            Arguments:
                decision: an element from the Decisions class
                n: number of shares to order
        
        """

        counter = 0

        # buy n
        if decision == Decisions.buy:
            counter = 0  
            while self.capital >= price:
                self.capital -= price
                self.shares += 1
                counter += 1
                if counter == n:
                    break
            
        # sell n
        elif decision == Decisions.sell:
            counter = 0  
            while self.shares > 0:
                self.capital += price
                self.shares -= 1
                counter += 1
                if counter == n:
                    break

        # plot a dot for buy or sell
        if counter > 0:
            if decision.value > 0:
                plt.plot([i], [price], marker='o', markersize=4, color="limegreen")
            elif decision.value < 0:
                plt.plot([i], [price], marker='o', markersize=4, color="red")

    
    
    def OptimalPosition(self, expected_return, prob_win, modifier):
        """ Uses the Kelly Criterion to calculate the optimal position size for a given play.

            Arguments:
                expected return: a float representing your percent gain (eg. 1.1 if you think you will gain 10%)
                prob_win: the fractional probability that we will get our expected return
                modifier: a value between 0 and 1; higher values make for a more aggressive bet
        """
        prob_lose = 1 - prob_win
        fraction = ((expected_return * prob_win) - prob_lose) / expected_return
        optimal_position = (self.capital * fraction) * modifier

        return optimal_position

    

    def PortfolioValue(self):
        """ Returns the current total monetary value of the portfolio """
        self.portfolio_value = self.capital + (self.shares*price)
        return self.portfolio_value


    


class MovingAverage:
    """ Moving Average 
    
    An object used to represent a moving average function.

    Attributes:
        averages: the list of average values at each point
        percent_difference: the percent difference between the price and the current point
        slope: the slope at the current point
        slope_sum: the sum of the slopes over the interval (window)
        avg_slope: the average slope over the interval (window)
        slopes: a list to hold the slopes
        concavity: the value for the concavity (2nd derivative) at the current point
        concavity_sum: the sum of the concavities over the interval (window)
        avg_concavity: the average concavity over the interval (window)
        concavities: a list to hold the concavities
        above: a bool to tell whether the proce is above or below the current point
        flipped: a bool that is True for one day after the price flips over the function
        edge: variable to account for the beginning of the dataset

    """

    def __init__(self):
        """ Inits a MovingAverage object """  
        
        self.averages = []
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
        self.edge =  0


    def CalculateAverage(self, value_list, window):

        """ Calculates the value for the moving average over the last (window) days.
        
            Arguments:
                value_list: the list of values of which the average will be calculated
                window: the interval over which to calculate the average value

         """
        
        # account for the beginning of the dataset
        if i < (window - 1):
            self.edge = window - (i + 1)
        else: self.edge = 0
        
        # calculate the average value over the interval
        if i == 0:
            value_sum = price
        else:
            value_sum = 0
            for n in range(window - self.edge):
                value_sum += value_list[i - n]
            
        return value_sum/(window - self.edge)
    


    def Update(self, window):
        """ Updates the indicators used for building the algorithm.
        
            Arguments:
                window: the interval over which to calculate the indicators
        
        """
        # percent deviation from the mean
        difference = price - self.averages[i]
        self.percent_difference = difference/self.averages[i]

        # calculate slope
        if i > 1:
            self.slope = self.averages[i] - self.averages[i - 1]

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
        if price > self.averages[i]:
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
    price_history = ticker_info.history(start="2015-01-01",  end="2020-12-20")

    # assign lists for the open/close prices, the moving-average values, 
    # and the daily average prices.
    opens = price_history['Open']
    closes = price_history['Close']
    prices = []

    # calculates the inital price of the stock, and 
    # the number of days we are looking back in history
    price = closes[0]
    days = opens.size

    # initialize the portfolio and moving average objects
    starting_capital = 0
    starting_shares = 100
    entry_price = starting_shares * price
    portfolio = Portfolio(starting_capital, starting_shares)

    # objects to track moving averages
    f1 = MovingAverage()
    f2 = MovingAverage()
    f3 = MovingAverage()
    f4 = MovingAverage()

    max_slope = 0

    # iterate over the history of the stock
    for i in range(days):
        
        # create a list of the closing prices
        price = closes[i]
        prices.append(price)
        
        # calculate the current moving averages
        f1.averages.append(f1.CalculateAverage(prices, 10))
        f2.averages.append(f2.CalculateAverage(prices, 50))
        f3.averages.append(f3.CalculateAverage(prices, 100))
        f4.averages.append(f4.CalculateAverage(prices, 200))
        
        # update the functions
        f1.Update(10)
        f2.Update(50)
        f3.Update(100)
        f4.Update(200)

        # decide if we buy, sell, or hold
        portfolio.Decide(f1, f2, f3, f4)
    
    
    # did we win?
    control_value = starting_capital + (prices[days - 1] * starting_shares)
    algo_value = portfolio.PortfolioValue()

    print(" ")
    print(f"Capital: {portfolio.capital:,.2f}")
    print(f"Shares: {portfolio.shares:,.2f}")
    print(f"Buy and Hold portfolio value: {control_value:,.2f}")
    print(f"Returns: {(control_value - entry_price):,.2f}")
    print(f"Algorithm portfolio value:  {algo_value:,.2f}")
    print(f"Returns: {(algo_value - entry_price):,.2f}")
    print(" ")

    # plot the price history and moving average history
    plot1 = plt.figure(1)
    x = list(range(0, days))
    plt.plot(x, prices)
    plt.title(ticker)
    plt.xlabel("Days")
    plt.ylabel("Price")
    
    plt.plot(x, f1.averages)
    plt.plot(x, f2.averages)
    plt.plot(x, f3.averages)
    plt.plot(x, f4.averages)

    plt.show()
