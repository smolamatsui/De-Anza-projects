import pandas as pd
import sqlite3
from datetime import datetime

class PresidentDB:
    def __init__(self, db_name='presidents.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def __str__(self):
        return f"SqliteDb(db_name={self.db_name})"

    def __repr__(self): 
        return self.__str__()

    def __eq__(self, other):
        return self.db_name == other.db_name

    def __len__(self):
        cursor = self.execute(f"SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        return cursor.fetchone()[0]
    
    def __del__(self):
        self.conn.close()
        
    def create_table(self):
        try:
            self.cursor.execute("DROP TABLE IF EXISTS presidents")
            
            self.cursor.execute('''
                CREATE TABLE presidents (
                    Presidency INTEGER,
                    President TEXT,
                    Took_office DATE,
                    Left_office DATE,
                    Years_Served REAL
                )
            ''')
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")

    def insert_data(self, df):
        df = dates_to_str(df) 
        
        for _, row in df.iterrows():
            try:
                self.cursor.execute('''
                    INSERT INTO presidents (Presidency, President, Took_office, Left_office, Years_Served) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['Presidency'], row['President'], row['Took office'], row['Left office'], row['Years Served']))
            except sqlite3.Error as e:
                print(f"An error occurred during insertion: {e}")
        self.conn.commit()

    def fetch_pres(self):
        try:
            self.cursor.execute("SELECT President, Years_Served, Took_office, Left_office FROM presidents WHERE Years_Served IS NOT NULL")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while fetching data: {e}")
            return []

def convert_to_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y')
    except ValueError:
        return None

def dates_to_str(df):
    df['Took office'] = df['Took office'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else None)
    df['Left office'] = df['Left office'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else None)
    return df

def calculate_years_served(row):
    if pd.notnull(row['Left office']) and pd.notnull(row['Took office']):
        return round((row['Left office'] - row['Took office']).days / 365.25, 2)
    return 0.0

def load_data(file_path):
    dfs = pd.read_html(file_path)
    df = dfs[0]
    
    df['Took office'] = df['Took office'].apply(convert_to_date)
    df['Left office'] = df['Left office'].apply(convert_to_date)
    
    df['Years Served'] = df.apply(calculate_years_served, axis=1)
    
    return df

def display_pres(pres_data):
    print("Presidents and years servered")
    
    tot_pres = len(pres_data)
    tot_yrs = 0
    
    for president, years_served, took_office, left_office in pres_data:
        tot_yrs += years_served
        took_office_str = took_office if took_office else "Unknown"
        left_office_str = left_office if left_office else "Present"
        
        print(f"{president:<25} served {years_served:>5} years ({took_office_str} to {left_office_str})")
    
    avg_years = tot_yrs / tot_pres if tot_pres > 0 else 0
    print(f"Total Presidents: {tot_pres}")
    print(f"Average Years Served: {avg_years:.2f}")

if __name__ == '__main__':
    try:
        file_path = 'Presidents.html' 
        
        pres_df = load_data(file_path)
        
        president_db = PresidentDB()
        president_db.insert_data(pres_df)
        
        pres_data = president_db.fetch_pres()
        display_pres(pres_data)
        
    except Exception as e:
        print(f"An error occurred: {e}")
