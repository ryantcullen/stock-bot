import yfinance as yf
import enum
import datetime
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
        portfolio_value: the overall value of the stock portfolio in $USD if the owner were to liquidate all assets

    Functions:
        Decide(): This is where the logic of when to buy, sell, or hold should go
        Order(): Used to execute a buy or sell order
    """

    def __init__(self, capital, shares, price):
        """ Inits a Portfolio object """

        self.capital = capital
        self.shares = shares
        self.portfolio_value = self.capital + self.shares * price


    def Decide(self, f1, f2, f3, f4, price):
        """ This is where the script decides to Buy, Sell, or Hold; Design your algorithm logic here.

            Arguments (keep these or design your own):
                f1, f2, f3, f4: moving averages of the stock price over different time periods
                price: the current stock price

        """

        #       ~~~~   Modify code below to implement your own trading Algorithm   ~~~~

        #TODO: design an algorithm that modifies these values based on the price data
        prob_profit = 0.501                             # probability of profit (eg, 50.1%)
        expected_return = 1.2                           # expected return (eg. 120%)
        modifier = 0.2                                  # value from 0-1; higher values make a more aggressive bet

        # Calculates the optimal position (and subsequent number of shares) based on the above parameters
        position = self.OptimalPosition(expected_return, prob_profit, modifier)
        shares = abs(int(position / price))

        # Buy or Sell shares based on the results of the algorithm
        if position > 0:
            self.Order(Decisions.buy, price, shares)
        else:
            self.Order(Decisions.sell, price, shares)

       #                        ~~~~  End of trading algorithm   ~~~~

    def Order(self, decision, price, n=-1, day=None):
        """ Executes a buy/sell order of n shares, or a buy/sell max order if no input for n.

            Arguments:
                decision: an element from the Decisions class
                price: the current stock price
                n: number of shares to order
                day: the day index for plotting

        """

        counter = 0

        # buy n shares
        if decision == Decisions.buy:
            counter = 0
            while self.capital >= price:
                self.capital -= price
                self.shares += 1
                counter += 1
                if counter == n:
                    break

        # sell n shares
        elif decision == Decisions.sell:
            counter = 0
            while self.shares > 0:
                self.capital += price
                self.shares -= 1
                counter += 1
                if counter == n:
                    break

        # plot a dot for buy or sell points
        if counter > 0 and day is not None:
            if decision.value > 0:
                plt.plot([day], [price], marker='o', markersize=4, color="limegreen")
            elif decision.value < 0:
                plt.plot([day], [price], marker='o', markersize=4, color="red")



    def OptimalPosition(self, expected_return, prob_win, modifier):
        """ Uses the Kelly Criterion to calculate the optimal position size for a given play.

            Arguments:
                expected_return: a float representing your percent gain (eg. 1.1 if you think you will gain 10%)
                prob_win: the fractional probability that we will get our expected return
                modifier: a value between 0 and 1; higher values make for a more aggressive bet
        """
        prob_lose = 1 - prob_win
        fraction = ((expected_return * prob_win) - prob_lose) / expected_return
        optimal_position = (self.capital * fraction) * modifier

        return optimal_position



    def PortfolioValue(self, price):
        """ Returns the current total monetary value of the portfolio """
        self.portfolio_value = self.capital + (self.shares * price)
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
        above: a bool to tell whether the price is above or below the current point
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


    def CalculateAverage(self, value_list, window, i, price):

        """ Calculates the value for the moving average over the last (window) days.

            Arguments:
                value_list: the list of values of which the average will be calculated
                window: the interval over which to calculate the average value
                i: the current day index
                price: the current stock price

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



    def Update(self, window, i, price):
        """ Updates the indicators used for building the algorithm.

            Arguments:
                window: the interval over which to calculate the indicators
                i: the current day index
                price: the current stock price

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

def main():
    while True:

        # input a ticker to track
        try:
            ticker = input("Enter ticker (or 'exit' to quit): ")
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if ticker.strip().lower() == 'exit':
            break

        # get ticker information and price history
        try:
            ticker_info = yf.Ticker(ticker)
            today = datetime.date.today().strftime("%Y-%m-%d")
            price_history = ticker_info.history(start="2015-01-01", end=today)
        except Exception as e:
            print(f"Error fetching data: {e}")
            continue

        if price_history.empty:
            print(f"No data found for ticker '{ticker}'. Please check the symbol and try again.")
            continue

        # assign lists for the open/close prices, the moving-average values,
        # and the daily average prices.
        opens = price_history['Open']
        closes = price_history['Close']
        prices = []

        # calculates the initial price of the stock, and
        # the number of days we are looking back in history
        price = closes.iloc[0]
        days = opens.size

        # initialize the portfolio and moving average objects
        starting_capital = 0
        starting_shares = 100
        entry_price = starting_shares * price
        portfolio = Portfolio(starting_capital, starting_shares, price)

        # objects to track moving averages
        f1 = MovingAverage()
        f2 = MovingAverage()
        f3 = MovingAverage()
        f4 = MovingAverage()

        # set the windows for the moving averages
        f1_window = 10
        f2_window = 50
        f3_window = 100
        f4_window = 200

        # iterate over the history of the stock
        for i in range(days):

            # create a list of the closing prices
            price = closes.iloc[i]
            prices.append(price)

            # calculate the moving averages
            f1.averages.append(f1.CalculateAverage(prices, f1_window, i, price))
            f2.averages.append(f2.CalculateAverage(prices, f2_window, i, price))
            f3.averages.append(f3.CalculateAverage(prices, f3_window, i, price))
            f4.averages.append(f4.CalculateAverage(prices, f4_window, i, price))

            # update the functions
            f1.Update(f1_window, i, price)
            f2.Update(f2_window, i, price)
            f3.Update(f3_window, i, price)
            f4.Update(f4_window, i, price)

            # decide if we buy, sell, or hold
            portfolio.Decide(f1, f2, f3, f4, price)


        # did we win?
        control_value = starting_capital + (prices[days - 1] * starting_shares)
        algo_value = portfolio.PortfolioValue(price)

        # print our portfolio information
        print()
        print(f"Capital: ${portfolio.capital:,.2f}")
        print(f"Shares: {portfolio.shares}")
        print(f"Buy and Hold portfolio value: ${control_value:,.2f}")
        print(f"Buy and Hold returns: ${control_value - entry_price:,.2f}")
        print(f"Algorithm portfolio value: ${algo_value:,.2f}")
        print(f"Algorithm returns: ${algo_value - entry_price:,.2f}")
        print()

        # plot the price history
        plt.figure()
        x = list(range(0, days))
        plt.plot(x, prices, label="Price")
        plt.title(ticker.upper())
        plt.xlabel("Days")
        plt.ylabel("Price ($)")

        # plot the moving averages
        plt.plot(x, f1.averages, label=f"{f1_window}-day MA")
        plt.plot(x, f2.averages, label=f"{f2_window}-day MA")
        plt.plot(x, f3.averages, label=f"{f3_window}-day MA")
        plt.plot(x, f4.averages, label=f"{f4_window}-day MA")

        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
