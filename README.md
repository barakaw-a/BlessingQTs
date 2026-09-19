# BlessingQTs: A Quantitative Backtesting Engine & Signaler

A Python-based quantitative trading research project that downloads historical market data into a local SQLite database and generates technical trading signals for backtesting.

## What it does
Generates buy/sell signals based on a simple moving average crossover and will eventually simulate portfolios against those signals. Currently, it also creates a local database for storing your stock prices based on user preferences, allowing previously downloaded historical data to be reused locally without requiring Yahoo Finance.

## Usage
Before running the program, you need to initialize the database that will store the stock prices by running the following lines:
```py
import data_loader
data_loader.initialize_db('path')
```
By default, it will initialize a database with the path market_data.db in the current directory; otherwise, it can be specified by passing your desired database path to the method.

---
To download and save data to the database, you'll need to run the command with your choice of ticker; this will insert/replace data from yfinance into the database for that ticker.

```py 
data_loader.save_data('TICKER')
```

---
From there, all that's needed is to create a Strategy object to run on. Example:
```py
algorithm = Strategy('path')

# Example: returning the n-th most recent signals
print(algorithm.moving_average('TICKER').tail(n))
```
Ticker: User-chosen symbol to calculate moving average for

Path: market_data.db by default, or the user's chosen database path

## Setup  
**Requirements**: Python 3.14+

Also ensure to have these libraries installed (Links to installation guides below):
* NumPy: https://numpy.org/install/
* pandas: https://pandas.pydata.org/docs/getting_started/install.html
* yfinance: https://ranaroussi.github.io/yfinance

## Files
| File | Purpose |
|------|---------|
|`data_loader.py`| Stores the method for database initialization and for downloading and cleaning the stock data|
`signaler.py` | Stores the methods involved in signal generation kept separate from the execution logic so strategy has no information on positions|



## Not yet implemented
* Portfolio Simulation
* Performance Metric
* Transaction Costs
* Slippage
* Multiple Indicators (EMA, RSI, etc.)
* More strategies (MACD, Bollinger Bands, etc.)
