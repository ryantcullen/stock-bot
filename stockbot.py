import yfinance as yf
import pandas as _pd
import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import date
from termcolor import colored


class Portfolio:
   
    """ Stock portfolio 
    
    Holds information about current buying power, equity, and overall value.

    Attributes:
        capital: starting cash.
        shares: starting number of shares.
        initial_price: the initial price of the stock.
        portfolio value: the overall value of the stock portfolio in $USD if the owner were to liquidate all assets.
        run: a counter to check if we are on a runup
    """
       
    def __init__(self, capital, shares, initial_price): 
        """ Inits a Portfolio object """

        self.capital = capital
        self.shares = shares
        self.initial_price = initial_price
        self.portfolio_value = self.capital + self.shares*self.initial_price
        self.run = 0
        self.Orders = []


    def Decide(self, f1, f2, f3, window):   
        """ 
            This is where the script decides to Buy, Sell, or Hold.
            return 3: Buy
            return -1: Sell

         """
        # concavity checks
        if(f2.concavity < -0.1):
            if price < f1.averages[i]:
                if price < f3.averages[i]:
                    self.run = 0
                    return 0
        if(f1.concavity < -0.2):
            if price > f3.averages[i]:
                self.run = 0
                return -1

        # TODO: Only sell for a profit? !!!

        if(f1.slope > -0.1):
            self.run += 1
        return self.run



    def Order(self, value, n, date):
        """ 
        Executes a buy order of n shares if value = 0, a sell order of
        n shares if value = -1, a sell max order if value = -2, and a 
        buy max order if value = 3.

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
        if value == 3:
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

        self.Orders.insert(i, dict(Type = value < 0 and "Sell" or (value == 0 or value == 3) and "Buy" or "Hold" , Day = date ))
        
    
    
    

    def PortfolioValue(self):
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

        """ Calculates the value for the moving average over the last (window) days
        
            Attributes:
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
        """ Updates the indicators used for building the algorithm
        
            Attributes:
                window: the interval over which to calculate the indicators.
        
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

def run_algo(ticker, starting_capital, starting_shares, start_date="2017-01-01", end_date="2020-12-24"):
    # get ticker information and price history
    ticker_info = type(ticker) == str and yf.Ticker(ticker) or None
    price_history = ticker_info and ticker_info.history(start=start_date,  end=end_date)
 
    if not ticker_info:
        price_history = ticker

    # assign lists for the open/close prices, the moving-average values, 
    # and the daily average prices.
    opens = price_history['Open']
    closes = price_history['Close']
    prices = []
    # calculates the inital price of the stock, and 
    # the number of days we are looking back in history
    global price
    for close in closes:
        if not math.isnan(close):
            price = close
            break
    days = opens.size

    # initialize figure for plottingexit
    fig, ax = plt.subplots()

    # initialize the portfolio and moving average objects
    entry_price = starting_shares * price
    portfolio = Portfolio(starting_capital, starting_shares, price)

    # objects to track moving averages
    f1 = MovingAverage()
    f2 = MovingAverage()
    f3 = MovingAverage()

    # iterate over the history of the stock
    for j in range(days):
        global i
        i = j
        # create a list of the closing prices
        price = closes[j]
        pricedate = price_history.iloc[j].name
        prices.append(price)
  
        # calculate the current moving averages
        window = 40
        f1.averages.append(f1.CalculateAverage(prices, window))
        f2.averages.append(f2.CalculateAverage(f1.averages, window))
        f3.averages.append(f3.CalculateAverage(f2.averages, window))
        
        # update the functions
        small_window = int(window/2)
        f1.Update(small_window)
        f2.Update(small_window)
        f3.Update(small_window)

        # decide if we buy, sell, or hold
        value = portfolio.Decide(f1, f2, f3, window)
        portfolio.Order(value, 10, pricedate)
    
    
    # did we win?
    control_value = starting_capital + (prices[days - 1] * starting_shares)
    algo_value = portfolio.PortfolioValue()

    return portfolio, entry_price, control_value, algo_value, prices, days

    



"""
Buy/Sell Decisions for today

"""
watchlist = ['BABA', 'IBM', 'PEN', 'GOOG', 'SPCE', 'AMD', 'NIO', 'ARKG', 'PENN', 'MRNA', 'WMT', 'AAPL', 'SBUX', 'NKE', 'SNE', 'ZS', 'FTNT', 'QLYS', 'CRWD', 'MIME'
, 'DIS', 'BA', 'SNAP']

"""
Main Loop

"""

while True:
    starting_capital = 0
    starting_shares = 55
    # input a ticker to track
    ticker = input("Enter ticker: ")
    if ticker == 'exit':
        break
    elif ticker == 'today':
        order_table = {}
        today = date.today()
        last_year = date(today.year-1, today.month, today.day)
        data = yf.download(tickers = watchlist, period = "1y", group_by = 'ticker')
        for ticker in watchlist:
            portfolio, entry_price, control_value, algo_value, prices, days = run_algo(data[ticker], starting_capital, starting_shares,start_date=last_year, end_date=today)
            order_today = portfolio.Orders[days-1]
            highlight_color = order_today['Type'] == "Buy" and 'green' or order_today['Type'] == "Sell" and 'red' or 'white'
            performance = math.floor( (algo_value-entry_price)/entry_price*100 )
            order_table[ticker] = {
                "Type" : order_today['Type'],
                "Day": order_today['Day'],
                "Current performance" : performance
            }
            print(ticker,colored( order_today, highlight_color), "Current performance: "+ (algo_value >= entry_price and "+%" or algo_value < entry_price and "-%")+ str(performance))
            plt.close()
        fig, ax = plt.subplots()
        ax.set_axis_off()
        ax_table = ax.table(
             cellText=[ [v[j] for j in v]  for i, v in order_table.items()],
             rowLabels=[i for i in order_table],
             colLabels=['Type', 'Day', 'Current performance'],
             cellLoc='center',
             loc='upper left',
        )
        plt.show()
           
    else:
        portfolio, entry_price, control_value, algo_value, prices, days = run_algo(ticker, starting_capital, starting_shares)
        print(" ")
        print("Capital: $" + str( math.floor(portfolio.capital)))
        print("Shares: " + str(portfolio.shares))
        print("Starting portfolio value: $" + str(math.floor(entry_price)))
        print("Buy and Hold portfolio value: $" + str(math.floor(control_value)))
        print("Returns: $" + str(math.floor(control_value - entry_price)))
        print("Algorithm portfolio value: $" + str(math.floor(algo_value)))
        print("Returns: $" + str(math.floor(algo_value - entry_price)))
        print(" ")
        #print(portfolio.Orders)
        #legends
        plt.plot([0], [prices[0]], marker='o', markersize=4, color="red", label="Sell Point")
        plt.plot([0], [prices[0]], marker='o', markersize=4, color="limegreen", label="Buy Point")

        # plot the price history and moving average history
        x = list(range(0, days))
        plt.plot(x, prices)
        plt.title(ticker)
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.legend()
        #plt.plot(x, f1.averages)
        #plt.plot(x, f2.averages)
        #plt.plot(x, f3.averages)

        plt.show()
         
       


       
    


    


