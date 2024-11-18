import json
import pandas as pd
import sqlite3
import pickle
import os
import unittest

class QueryBuilder:
    def __init__(self):
        self.command_map = {
            "select": self.select,
            "insert": self.insert,
            "delete": self.delete,
            "update": self.update,
            "create_table": self.create_table,
            "connect": self.connect,
            "search": self.search
        }

    def query(self, table, command_type, *args):
        command_type = command_type.lower()
        try:
            return self.command_map[command_type](table, *args)
        except KeyError:
            raise sqlite3.Error(f"The command: {command_type} was not found.")
        except Exception as e:
            raise sqlite3.Error(f"An error occurred: {e}")

    def select(self, table, fields='*', condition=''):
        self.validate_table_and_fields(table, fields)
        query = f"SELECT {fields} FROM {table}"
        query += f" WHERE {condition}" if condition else ""
        return query

    def insert(self, table, fields, values):
        self.validate_table_fields_values(table, fields, values)
        pickled_values = list(values)
        if len(values) >= 3:
            pickled_values[2] = pickle.dumps(values[2]) 
        if len(values) >= 4:
            pickled_values[3] = pickle.dumps(values[3]) 

        placeholders = ', '.join(['?'] * len(pickled_values))
        query = f"INSERT INTO {table} {fields} VALUES ({placeholders})"
        return query, tuple(pickled_values)

    def delete(self, table, condition):
        self.validate_table_and_condition(table, condition)
        query = f"DELETE FROM {table} WHERE {condition}"
        return query

    def update(self, table, set_data, condition):
        self.validate_table_set_data_condition(table, set_data, condition)
        set_clause = ', '.join([f"{key} = ?" for key in set_data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        return query, tuple(set_data.values())

    def create_table(self, table, fields):
        self.validate_table_and_fields(table, fields)
        query = f"CREATE TABLE {table} ({fields})"
        return query

    def connect(self, _, database_name):
        assert database_name, "Database name cannot be empty."
        return f"CONNECT TO DATABASE {database_name}"

    def search(self, table, search_term):
        self.validate_table_and_fields(table, search_term)
        query = f"SELECT * FROM {table} WHERE name LIKE ?"
        return query, (f'%{search_term}%',)

    def validate_table_and_fields(self, table, fields):
        assert table and fields, "Table name and fields cannot be empty."

    def validate_table_fields_values(self, table, fields, values):
        assert table and fields and values, "Table name, fields, and values cannot be empty."

    def validate_table_and_condition(self, table, condition):
        assert table and condition, "Table name and condition cannot be empty."

    def validate_table_set_data_condition(self, table, set_data, condition):
        assert table and set_data and condition, "Table name, set data, and condition cannot be empty."

class SqliteDB:
    def __init__(self, json_file, table_name):
        self.json_file = json_file
        self.table_name = table_name
        self.db_name = json_file.replace('.json', '.db')
        self.load_data()
        self.create_table()
        self.insert_dataframe()  

    def load_data(self):
        with open(self.json_file) as f:
            raw_data = json.load(f)
            #print("Raw content from JSON file:", raw_data)
            self.df = pd.DataFrame(raw_data)
            self.df.rename(columns={"Name": "Dwarf"}, inplace=True)
            #print("DataFrame created:\n", self.df)

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            self.conn = conn
            self.df.to_sql(self.table_name, conn, if_exists='replace', index_label='id')
            #print("DataFrame inserted into the database.")

    def insert_row_column(self, row_data):
        with self.conn:
            self.conn.execute(
                f"INSERT INTO {self.table_name} (Dwarf, Distance, Period) VALUES (?, ?, ?)",
                (row_data['Dwarf'], row_data['Distance'], row_data['Period'])
            )
            #print(f"Row inserted into the database: {row_data}")

    def KVfunction(self, action_name):
        return self.actions.get(action_name, lambda: "Unknown action.")()

    def select_all(self):
        return self.query_builder.select(self.table_name).execute(self.conn)

    def select_condition(self, condition):
        return self.query_builder.select(self.table_name).where(condition).execute(self.conn)


class TestSqliteDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_json_file = 'test_data.json'
        cls.test_data = {
            "Name": {
                "dwarf0": "Ceres",
                "dwarf1": "Pluto",
                "dwarf2": "Haumea",
                "dwarf3": "Makemake",
                "dwarf4": "Eris"
            },
            "Distance": {
                "dwarf0": 2.77,
                "dwarf1": 39.5,
                "dwarf2": 43.19,
                "dwarf3": 45.48,
                "dwarf4": 67.84
            },
            "Period": {
                "dwarf0": 4.61,
                "dwarf1": 247.69,
                "dwarf2": 283.84,
                "dwarf3": 306.17,
                "dwarf4": 558.77
            }
        }
        with open(cls.test_json_file, 'w') as f:
            json.dump(cls.test_data, f)

        cls.table_name = 'DwarfPlanets'
        cls.db = SqliteDB(cls.test_json_file, cls.table_name)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db.db_name):
            os.remove(cls.db.db_name)
        if os.path.exists(cls.test_json_file):
            os.remove(cls.test_json_file)

    def test_dataframe_creation(self):
        expected_columns = {'Dwarf', 'Distance', 'Period'}
        self.assertSetEqual(set(self.db.df.columns), expected_columns)
        self.assertEqual(len(self.db.df), 5)  

    def test_insert_dataframe(self):
        initial_count = self.db.conn.execute(f"SELECT COUNT(*) FROM {self.db.table_name}").fetchone()[0]
        self.db.insert_dataframe()
        final_count = self.db.conn.execute(f"SELECT COUNT(*) FROM {self.db.table_name}").fetchone()[0]
        self.assertEqual(final_count, initial_count + 5)

    def test_insert_row_column(self):
        new_data = {'Dwarf': 'Orcus', 'Distance': 39.22, 'Period': 245.62}
        self.db.insert_row_column(new_data)

        count = self.db.conn.execute(f"SELECT COUNT(*) FROM {self.db.table_name}").fetchone()[0]
        self.assertEqual(count, 6) 

        row = self.db.conn.execute(f"SELECT * FROM {self.db.table_name} WHERE Dwarf = 'Orcus'").fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], 'Orcus')
        self.assertEqual(row[1], 39.22)    
        self.assertEqual(row[2], 245.62)   

    def test_select_all(self):
        results = self.db.KVfunction("select_all")
        self.assertEqual(len(results), 5)

    def test_select_condition(self):
        results = self.db.KVfunction("select_condition")("Distance > 10")
        self.assertGreater(len(results), 0) 

    def test_unknown_action(self):
        result = self.db.KVfunction("unknown_action")
        self.assertEqual(result, "Unknown action.")

if __name__ == '__main__':
    unittest.main()
