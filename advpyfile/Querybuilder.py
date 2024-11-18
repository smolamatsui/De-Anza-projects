import sqlite3
import pickle
import unittest

#the SQL query builder class
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


# testing
class TestQueryBuilder(unittest.TestCase):
    def setUp(self):
        self.qBuilder = QueryBuilder()

    def test_select(self):
        query = self.qBuilder.query("exampleTable", "select", "*")
        expected_query = "SELECT * FROM exampleTable"
        self.assertEqual(query, expected_query)

    def test_insert(self):
        fields = "(id, name, photo, html)"
        data = (3, "bobdwarf", "bobdwarf.png", "bobdwarf.html")  
        expected_query = "INSERT INTO exampleTable (id, name, photo, html) VALUES (?, ?, ?, ?)"
        query, query_values = self.qBuilder.query("exampleTable", "insert", fields, data)
        self.assertEqual(query, expected_query)
        self.assertEqual(query_values, (3, "bobdwarf", pickle.dumps("bobdwarf.png"), pickle.dumps("bobdwarf.html")))

    def test_delete(self):
        condition = "id = 1"
        query = self.qBuilder.query("exampleTable", "delete", condition)
        expected_query = "DELETE FROM exampleTable WHERE id = 1"
        self.assertEqual(query, expected_query)

    def test_update(self):
        set_data = {"name": "Updated"}
        condition = "id = 1"
        expected_query = "UPDATE exampleTable SET name = ? WHERE id = 1"
        query, query_values = self.qBuilder.query("exampleTable", "update", set_data, condition)
        self.assertEqual(query, expected_query)
        self.assertEqual(query_values, ("Updated",))

    def test_create_table(self):
        fields = "id INTEGER PRIMARY KEY, name TEXT"
        query = self.qBuilder.query("exampleTable", "create_table", fields)
        expected_query = "CREATE TABLE exampleTable (id INTEGER PRIMARY KEY, name TEXT)"
        self.assertEqual(query, expected_query)

    def test_connect(self):
        result = self.qBuilder.query("", "connect", "test_database.db")
        expected_result = "CONNECT TO DATABASE test_database.db"
        self.assertEqual(result, expected_result)

    def test_search(self):
        search_term = "Sample"
        query, query_values = self.qBuilder.query("exampleTable", "search", search_term)
        expected_query = "SELECT * FROM exampleTable WHERE name LIKE ?"
        expected_values = (f'%{search_term}%',)
        self.assertEqual(query, expected_query)
        self.assertEqual(query_values, expected_values)

    def test_invalid_command(self):
        with self.assertRaises(sqlite3.Error):
            self.qBuilder.query("exampleTable", "invalid_command")


if __name__ == "__main__":
    unittest.main()

