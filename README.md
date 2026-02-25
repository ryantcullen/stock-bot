# StockBot

An open-source Python backtesting engine for designing and evaluating daily stock trading algorithms against real historical market data.

## Features

- Fetches up to 10 years of historical price data via the Yahoo Finance API
- Computes 10, 50, 100, and 200-day moving averages with derived indicators (slope, concavity, crossover detection)
- Position sizing via the [Kelly Criterion](https://en.wikipedia.org/wiki/Kelly_criterion)
- Compares algorithm performance against a buy-and-hold baseline
- Visualizes results with matplotlib (price chart, moving average overlays, buy/sell markers)

## Installation

```bash
git clone https://github.com/ryantcullen/stock-bot.git
cd stock-bot
pip install -r requirements.txt
```

## Usage

```bash
python stockbot.py
```

Enter any stock ticker (e.g. `AAPL`, `TSLA`, `IBM`) to run the backtest. Type `exit` or `Ctrl+C` to quit.

### Example Output

```
Capital: $1,247.83
Shares: 42
Buy and Hold portfolio value: $15,230.00
Buy and Hold returns: $5,230.00
Algorithm portfolio value: $16,012.49
Algorithm returns: $6,012.49
```

![PEN](https://github.com/ryantcullen/stock-bot/blob/master/Example%20Pictures/B4myQ0t.png?raw=true)

![BABA](https://github.com/ryantcullen/stock-bot/blob/master/Example%20Pictures/TwOShiK.png?raw=true)

![IBM](https://github.com/ryantcullen/stock-bot/blob/master/Example%20Pictures/lhWY5yX.png?raw=true)

## Designing Your Own Algorithm

All trading logic lives in the `Decide()` method of the `Portfolio` class. To implement your own strategy, modify three parameters based on the moving average data:

```python
prob_profit = 0.501         # probability of profit (e.g. 50.1%)
expected_return = 1.2       # expected return multiplier (e.g. 1.2 = 120%)
modifier = 0.2              # aggressiveness (0-1); higher = larger positions
```

The method receives four `MovingAverage` objects (`f1` through `f4`), each with attributes you can use to build your logic:

| Attribute | Description |
|-----------|-------------|
| `percent_difference` | How far the current price deviates from the moving average |
| `slope` | First derivative — momentum / direction of the trend |
| `avg_slope` | Average slope over the window |
| `concavity` | Second derivative — whether the trend is accelerating or decelerating |
| `avg_concavity` | Average concavity over the window |
| `above` | Whether the price is currently above the moving average |
| `flipped` | `True` on the day the price crosses over the moving average |

## Architecture

| Class | Responsibility |
|-------|---------------|
| `Portfolio` | Manages capital, share count, order execution, and Kelly Criterion position sizing |
| `MovingAverage` | Computes rolling averages and derived technical indicators over a configurable window |
| `Decisions` | Enum for buy/sell/hold actions |

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

## Author

Ryan Cullen
