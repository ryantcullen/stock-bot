# StockBot

StockBot is a Python script for designing and testing your own daily stock trading algorithms.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install matplotlib and yfinance from your command line.

```bash
pip install matplotlib
pip install yfinance
```

## Usage
You will be asked to enter a ticker for the stock that you want to test the algorithm on.

## Results
The aglorithm's success is judged by comparing the returns to a simple Buy-and-Hold strategy. Here are some results based on the last 3 years fo close prices:

![BABA](https://imgur.com/TwOShiK)
Buy-and-Hold Returns: +$17140.42
Algorithm Returns: +$19274.65

![PEN](https://imgur.com/B4myQ0t)
Buy-and-Hold Returns: +$11,794.99
Algorithm Returns: +$13,176.74

![GOOG](https://imgur.com/wl01kRr)
Buy-and-Hold Returns: +$94,486.99
Algorithm Returns: +$82,392.37

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
