import sqlite3
import pandas as pd
import json
from Querybuilder import QueryBuilder

class SqliteDB:
    def __init__(self, json_file):
        self.db_name = json_file.split('.')[0]  # Database name from JSON file name
        self.table_name = "DwarfPlanets"  # You can change this as needed
        self.conn = sqlite3.connect(f"{self.db_name}.db")
        self.cursor = self.conn.cursor()
        self.query_builder = QueryBuilder()

#step 1 (load json to df function)
    def load_json_to_df(self, json_file): #I was having a lot of trouble loading in json, so there are a lot of excess error statements.
        try:
            with open(json_file, "r", encoding='utf-8') as infile:
                file_content = infile.read()
            data = json.loads(file_content)

            if not isinstance(data, dict):
                raise ValueError("Loaded JSON data is not a dictionary")
            
            # check if the keys exist in the table
            if not all(key in data for key in ['Name', 'Distance', 'Period']):
                print("One of the required keys is missing in the JSON data.")
                return None

            df_data = [
                {
                    'Name': data['Name'][key],
                    'Distance': data['Distance'][key],
                    'Period': data['Period'][key]
                }
                for key in data['Name'].keys()
                if key in data['Distance'] and key in data['Period']
            ]

            return pd.DataFrame(df_data)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def create_table_from_df(self, table_name, df):
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(drop_query)

        columns = ', '.join([f"{col} {self.get_sqlite_type(df[col])}" for col in df.columns])
        create_query = f"CREATE TABLE {table_name} ({columns})"
        
        try:
            self.cursor.execute(create_query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")

    def get_sqlite_type(self, pd_series):
        if pd.api.types.is_integer_dtype(pd_series):
            return "INTEGER"
        elif pd.api.types.is_float_dtype(pd_series):
            return "REAL"
        else:
            return "TEXT"

    def execute(self, query_name, *args):
        actions = {
            "insert": self.insert_row,
            "select": self.select_query,
            # Add other queries here
        }

        action = actions.get(query_name, self.default_action)
        return action(*args)

    def insert_row(self, data):
        columns = f"({', '.join(['Name', 'Distance', 'Period'])})"
        insert_query = f"INSERT INTO {self.table_name} {columns} VALUES (?, ?, ?)"
        self.cursor.execute(insert_query, data)
        self.conn.commit()

    def select_query(self, *args):
        select_query = f"SELECT * FROM {self.table_name}"
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def default_action(self, *args):
        print("Unknown action.")
        return None

    def close(self):
        self.conn.close()

# Example usage
# Example usage
if __name__ == "__main__":
    sqdb = SqliteDB("KeplerBelt.json")  # Use the JSON file here
    
    # Load JSON data into DataFrame
    df = sqdb.load_json_to_df("KeplerBelt.json")
    
    # Check if the DataFrame is loaded successfully
    if df is not None:
        # Create the table from DataFrame
        sqdb.create_table_from_df(sqdb.table_name, df)
        
        # Example: Inserting a row (data as tuple)
        data = ('Ceres', 2.77, 4.61)  # Sample data
        sqdb.execute("insert", data)

    # Query the data
    results = sqdb.execute("select")
    for result in results:
        print(result)

    sqdb.close()
