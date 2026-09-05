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
                        open FLOAT, close FLOAT, low FLOAT, high FLOAT, volume INT,
                        CONSTRAINT PRIMARY KEY (symbol, date)
                    );
                    """)

# db_path by default with attempt to setup a connection with market_data.db unless specified otherwise
def save_data(symbol: str, db_path = 'market_data.db'):
        
    print("1. Starting download from Yahoo Finance...")
    data = yf.download(symbol, period='1wk', interval='1d').reset_index()
    data.columns = data.columns.to_flat_index()
    print(data.columns)
    
    if data.empty:
        print("2. Download Error. No data has been downloaded.")
        return
    else:
        print("2. Connecting to database and saving...")
        with sqlite3.connect(db_path) as con:
            try:
                table_name = f'{symbol.lower()}_daily_data'                                
                
                current_data = pd.read_sql(f"SELECT * FROM {table_name}", con)
                print(current_data.columns)
                combined = pd.merge(current_data, data, how='outer', left_on="'('Date', '')'", right_on="('Date', '')")               
                combined.to_sql(name=table_name, con=con, index=True, if_exists='replace')
                                
                print(f"3. {table_name} successfully updated!")
            except pd.errors.DatabaseError:
                data.to_sql(name=table_name, con=con, index=True, if_exists='replace')
                print(f"3. {table_name} successfully saved to database!")
        
save_data('AAPL')