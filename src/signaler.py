import numpy as np
import pandas as pd
import sqlite3
import data_loader

class Strategy:
    def __init__(self, db_path: str = 'market_data.db'):
        self.db_path = db_path
        
    def simple_ma(self, symbol : str, short_term = 50, long_term = 200) -> pd.Series:
        with sqlite3.connect(self.db_path) as con:
            
            short = con.execute("""    
                                SELECT close
                                FROM prices
                                WHERE symbol = ?
                                ORDER BY date DESC
                                LIMIT ?    
                                """, [symbol, short_term])
            
            short_list = pd.DataFrame(short.fetchall())
            short_sma = ((short_list.sum()[0])/short_term)
            
            long = con.execute("""
                                SELECT close
                                FROM prices
                                WHERE symbol = ?
                                ORDER BY date DESC
                                LIMIT ?
                                """, [symbol, long_term])
            long_list = pd.DataFrame(long.fetchall())
            long_sma = ((long_list.sum()[0])/long_term)
            