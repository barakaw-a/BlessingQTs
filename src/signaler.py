import numpy as np
import pandas as pd
import sqlite3
import data_loader

class Strategy:
    def __init__(self, db_path : str = 'market_data.db'):
        self.db_path = db_path
    
    # Implemented a simple moving average with a short-term of 10 days and long-term of 50 days
    # Returns a Series of orders based on crossovers
    def moving_average(self, symbol : str, short_term = 10, long_term = 50):
        with sqlite3.connect(self.db_path) as con:
             
            date_price = con.execute("""
                                        SELECT close, date
                                        FROM prices
                                        WHERE symbol = ?
                                        ORDER BY DATE ASC
                                    """, [symbol]).fetchall()
                        
            df_date_price = pd.DataFrame(date_price)
            df_date_price.rename(columns = {0: 'price', 1: 'date'}, inplace = True)
            
            df_date_price['date'] = pd.to_datetime(df_date_price['date'])
            df_date_price.set_index('date', inplace = True)
            
            
            df_date_price['short_sma'] = (df_date_price['price'].rolling(window = short_term).mean())
            df_date_price['long_sma'] = (df_date_price['price'].rolling(window = long_term).mean())
            
            df_date_price['signals'] = pd.Series(pd.NA, index = df_date_price.index, dtype = 'string')
            
            valid = df_date_price['long_sma'].notna()
            
            df_date_price.loc[valid, 'signals'] = np.where(df_date_price.loc[valid, 'short_sma'] > df_date_price.loc[valid, 'long_sma'], 'Buy', 'Sell')
            
            return(df_date_price['signals'])
