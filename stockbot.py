import yfinance as yf
import pandas as _pd
import numpy as np
import matplotlib.pyplot as plt


def MakeChannel(i, price, length, n):
    
    resistance = []
    support = []
    xvals = np.linspace(i, i + length - 1, length)
    slope = n*closes[days-1]/5000

    offset = (price/100)/10
    floor = (price/100) * 1.2

    for n in range(length):
        resistance.append(price - n*slope + offset)

    for n in range(length):
        support.append(price - n*slope - floor + offset)

    return resistance, support, xvals

class BullFlag:
    
    flagpole = False
    make_flag = False
    counter = 0
    resistance = []
    support = []
    xvals = []

    def BullFlags(self):

        if i < day_range:
            old_price = prices[0]
            pole_price = prices[0]
        else:
            old_price = prices[i - day_range]
            pole_price = prices[i - int(day_range/10)]
        
        if self.flagpole != True:
            runup_difference = price - old_price
            pole_difference = price - pole_price
            runup = (runup_difference/old_price)*100
            pole = (pole_difference/pole_price)*100

            if (runup > perc) & (pole > (perc/2)):
                self.flagpole = True
                self.make_flag = True

        if self.flagpole:
            if self.make_flag:
                self.resistance, self.support, self.xvals = MakeChannel(i, price, channel_range, 1)
                self.make_flag = False

            if self.counter > channel_range - 1:
                self.flagpole = False
                self.counter = 0
                #maybe average proces for this comparison
                if price > self.support[self.counter]:
                    # plt.plot(self.xvals, self.resistance)
                    # plt.plot(self.xvals, self.support)
                    plt.plot([i], [price], marker='o', markersize=4, color="limegreen")
                    # print("Found Flag")
                    # print(i)         

            if price < self.support[self.counter]:
                if self.counter > (channel_range/2):
                    self.flagpole = False
                    self.counter = 0
                else:
                    self.counter += 1
            else: self.counter += 1



class BullBearRuns:

    up_weeks = []
    down_weeks = []
    bull_run = False
    bear_run = True
    old_price = 0
    

    def RunCheck(self):

        if i % 5 == 0:
            if i < day_range:
                self.old_price = prices[0]
            else:
                self.old_price = prices[i - 6]


            if price > self.old_price:
                #change based on stock price
                if len(self.up_weeks) > 5:
                    self.up_weeks.append(1)
                    self.down_weeks.append(0)
                    self.up_weeks.pop(0)
                    self.down_weeks.pop(0)
                else:
                    self.up_weeks.append(1)
                    self.down_weeks.append(0)
            else:
                #change based on stock price
                if len(self.up_weeks) > 5:
                    self.up_weeks.append(0)
                    self.down_weeks.append(1)
                    self.up_weeks.pop(0)
                    self.down_weeks.pop(0)
                else:
                    self.up_weeks.append(0)
                    self.down_weeks.append(1)

            

        #tweak this (should they start at 0?)
        ups = 0.5
        downs = 0.5

        #this can be optimized by only adding the next num and subtracting the first and then re calc average
        for x in range(len(self.up_weeks)):
            ups += self.up_weeks[x]
            downs += self.down_weeks[x]

        if i % 200 == 0:
            for x in range(len(self.up_weeks)):
                self.up_weeks[x] = 0
                self.down_weeks[x] = 0
        
        updown_ratio = ups/downs
        print(updown_ratio)
        if (updown_ratio > 7):
            self.bull_run = True
            self.bear_run = False
            plt.plot([i], [price], marker='o', markersize=4, color="red")
        
        if (updown_ratio < 0.5):
            self.bull_run = False
            self.bear_run = True
            plt.plot([i], [price], marker='o', markersize=4, color="limegreen")


bullflag_detector = BullFlag()
run_detector = BullBearRuns()

while True:

    ticker = input("Enter ticker: ")
    if ticker == 'exit':
        break
    perc = float(input("Enter prior uptrend percentage: "))
    day_range = int(input("Enter number of trading days: "))
    channel_range = int(input("Enter channel range: "))

    ticker_info = yf.Ticker(ticker)
    price_history = ticker_info.history(start="2010-9-5",  end="2020-12-11")

    opens = price_history['Open']
    closes = price_history['Close']
    days = opens.size
    prices = []
    fig = plt.figure()

    for i in range(days):
        price = (opens[i] + closes[i])/2
        prices.append(price)
        bullflag_detector.BullFlags()
        run_detector.RunCheck()
    

    x = np.linspace(0, days, days)
    y = prices
    plt.plot(x,y)

    plt.show()


    


