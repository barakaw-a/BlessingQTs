import yfinance as yf
import numpy as np
import pandas as pd
import sqlite3

def initialize_db(db_path='market_data.db'):
    with sqlite3.connect(db_path) as con:
        con.execute("""
                    CREATE TABLE IF NOT EXISTS prices (
                        symbol VARCHAR NOT NULL,
                        date DATETIME NOT NULL,
                        open FLOAT, high FLOAT, low FLOAT, close FLOAT, volume INT,
                        PRIMARY KEY (symbol, date)
                    );
                    """)

# db_path by default with attempt to setup a connection with market_data.db unless specified otherwise
def save_data(symbol: str, db_path = 'market_data.db'):
        
    print("1. Starting download from Yahoo Finance...")
    data = yf.download(symbol.upper(), period='3y', interval='1d').reset_index()
    data['symbol'] = symbol.upper()
    
    # Isolating OHLCV Headers from downloaded data
    data.columns = data.columns.to_flat_index()
    data.columns = data.columns.map(lambda x : '_'.join(map(str, x)))
    data.columns = data.columns.str.split('_').str[0]
    
    listed_info = []
    
    for idx, row in data.iterrows():
        listed_info += [row.to_list()]
        
        
    if data.empty:
        print("2. Download Error. No data has been downloaded.")
        return
    else:
        print("2. Connecting to database and saving...")
        with sqlite3.connect(db_path) as con:            
            for idx, entry in enumerate(listed_info):
                entry[0] = entry[0].to_pydatetime()
                print(entry)
                con.execute(""" INSERT OR REPLACE INTO prices (date, close, high, low, open, volume, symbol)
                                VALUES(?, ?, ?, ?, ?, ?, ?)
                                """, entry)
                                
            print(f"3. Prices successfully updated!")
            