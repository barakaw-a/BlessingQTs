import numpy as np
import pandas as pd
import sqlite3
import data_loader

class Strategy:
    def __init__(self, db_path : str = 'market_data.db'):
        self.db_path = db_path
    
    # Retrive all stock price data for a given symbol
    # Newest entries at the bottom
    def price_fetching(self, symbol: str):
        with sqlite3.connect(self.db_path) as con:
            
            price_data = con.execute("""
                                        SELECT close, date
                                        FROM prices
                                        WHERE symbol = ?
                                        ORDER BY DATE ASC
                                    """, [symbol]).fetchall()
            
        
        df_price = pd.DataFrame(price_data)
        df_price.rename(columns = {0: 'price', 1: 'date'}, inplace = True)
        
        df_price['date'] = pd.to_datetime(df_price['date'])
        df_price.set_index('date', inplace = True)
            
        return df_price    
            
    # Implemented a simple moving average with a short-term of 10 days and long-term of 50 days
    # Returns a Series of positions based on crossovers    
    def moving_average(self, symbol : str, short_term = 10, long_term = 50):
        
        df_price = self.price_fetching(symbol)
        
        df_price['short_sma'] = (df_price['price'].rolling(window = short_term).mean())
        df_price['long_sma'] = (df_price['price'].rolling(window = long_term).mean())
            
        df_price['signals'] = pd.Series(pd.NA, index = df_price.index, dtype = 'string')
          
        valid = df_price['long_sma'].notna()
            
        df_price.loc[valid, 'signals'] = np.where(df_price.loc[valid, 'short_sma'] > df_price.loc[valid, 'long_sma'], 'Bullish', 'Bearish')
            
        return(df_price['signals'])
        
    def exp_moving_average(self, symbol: str, short_term = 10, long_term = 50):
        
        # TBC
        
        return 0
    
    @staticmethod
    def calculate_ema(price_data, period):
        
        multiplier = (2 / (period + 1))
        ema = []
        
        # Compute the first value for our EMA
        inital_ema = sum(price_data[:period]) / period
        ema.append(inital_ema)
        
        for price in price_data[period:]:
            new_ema = (price * multiplier) + ((1 - multiplier) * ema[-1])
            ema.append(new_ema)
            
        return ema