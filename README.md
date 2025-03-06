Author:  Ryan Cullen
# StockBot

StockBot is a Python application for designing and testing your own daily stock trading algorithms.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install matplotlib and yfinance from your command line.

```bash
pip install matplotlib
pip install yfinance
```

## Usage
You will be asked to enter a ticker for the stock that you want to test the algorithm on.

## Designing Your Own Algorithm
If you want to modify the algorithm and design your own, you only need to change the Decide() function so that the followig parameters are updated based on your algorithm logic:
```
prob_profit = 0.501                             # probability of profit (eg, 50.1%)
expected_return = 1.2                           # expected return (eg. 120%)
modifier = 0.2                                  # value from 0-1; higher values = more aggressive bet
```
The Decide() function also takes three inputs, which correspond to moving averages of the stock over various tine frames. These may be useful when designing your algorithm. 

## Example Output
Here are a couple images depicting the output from an algorithm I developed. 

![PEN](https://github.com/ryantcullen/stock-bot/blob/master/Example%20Pictures/B4myQ0t.png?raw=true)

![BABA](https://github.com/ryantcullen/stock-bot/blob/master/Example%20Pictures/TwOShiK.png?raw=true)

![IBM](https://github.com/ryantcullen/stock-bot/blob/master/Example%20Pictures/lhWY5yX.png?raw=true)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

The goal for this script is of course for it to be as robust and generalized as possible in terms of the data available for the user to use to design an algorithm. Add features according to whatever that means to you and submit a pull request to the feature-test branch. If if adds value to the project it will be accepted and merged. 

Please make sure to update tests as appropriate.

Thanks!  :)


