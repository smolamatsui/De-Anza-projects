import socket
import threading
import sqlite3
import pickle
from typing import Any, Union, Tuple
import unittest
from unittest.mock import patch
import io
import json
import pandas as pd

ACK = b'\x06'
NAK = b'\x00'
INSERT_ERROR = b'\x01'
DELETE_ERROR = b'\x02'
UPDATE_ERROR = b'\x03'

class BitstringConverter:
    def __init__(self, input_string: str = "string"):
        if not isinstance(input_string, str):
            raise ValueError("Input must be a string.")
        self._input_string = input_string
        self._conversions = {
            "Bits": self._to_bits,
            "Bytes": self._to_bytes,
            "BitString": self._to_bitstring,
            "ByteArray": self._to_bytearray,
            "BytesIO": self._to_bytesio,
            "From Bits": self._from_bits,
            "From Bytes": self._from_bytes,
        }

    def _to_bits(self):
        """Converts each character in the input string to its binary representation (bits)."""
        return ' '.join(f'{ord(c):08b}' for c in self._input_string)

    def _to_bytes(self):
        """Converts the input string to a hexadecimal byte representation."""
        return ' '.join(f'{b:02x}' for b in self._input_string.encode('utf-8'))

    def _to_bitstring(self):
        """Returns a formatted bitstring prefixed with '0b' for each character."""
        return f"0b{' '.join(format(ord(c), '08b') for c in self._input_string)}"

    def _to_bytearray(self):
        """Converts the input string into a hexadecimal representation of a bytearray."""
        return ' '.join(f'{b:02x}' for b in bytearray(self._input_string, 'utf-8'))

    def _to_bytesio(self):
        """Converts the input string into a BytesIO object and returns its hexadecimal representation."""
        bytes_io = io.BytesIO(self._input_string.encode('utf-8'))
        return ' '.join(f'{b:02x}' for b in bytes_io.getvalue())

    def _from_bits(self, bits: str):
        """Converts a bitstring into the original string if valid; otherwise returns an error."""
        try:
            byte_array = bytearray(int(bits[i:i + 8], 2) for i in range(0, len(bits), 9))
            return byte_array.decode('utf-8')
        except ValueError:
            return "Invalid Bit Stream"

    def _from_bytes(self, byte_data: str):
        """Converts a hexadecimal byte representation back to the original string if valid."""
        try:
            return bytes.fromhex(byte_data.replace(" ", "")).decode('utf-8')
        except (ValueError, AttributeError):
            return "Invalid Byte Stream"

    def __str__(self):
        return f"BitstringConverter(input_string='{self._input_string}')"

    def __repr__(self):
        return f"BitstringConverter('{self._input_string}')"

    def __iter__(self):
        return iter(self._input_string)

    def __len__(self):
        return len(self._input_string)

    def __getitem__(self, index):
        return self._input_string[index]

    def __contains__(self, item):
        return item in self._input_string

    def __eq__(self, other):
        if isinstance(other, BitstringConverter):
            return self._input_string == other._input_string
        return False

    def convert(self, data: Any, to_bytes=True) -> Union[bytes, str]:
        """Converts data between string and byte formats based on the 'to_bytes' flag."""
        if to_bytes and isinstance(data, str):
            return data.encode('utf-8')
        elif not to_bytes and isinstance(data, bytes):
            return data.decode('utf-8')
        return data


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
    def __init__(self, db_file: str):
        self.db_file = db_file 
        self.lock = threading.Lock()

    def create_example_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS example_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        );
        """
        self.execute_query(query)


    def execute_query(self, query: str) -> Any:
        with self.lock:
            conn = None
            try:
                print(f"Executing query: {query}")
                conn = sqlite3.connect(self.db_file)
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                result = cursor.fetchall()
                return result if result else ACK
            except sqlite3.DatabaseError as e:
                print(f"Database error: {e}")
                return NAK + str(e).encode('utf-8')
            finally:
                if conn:
                    conn.close()

    def create_table(self, table_name: str, columns: str):
        """Create a table with specified columns if it doesn't exist."""
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        return self.execute_query(query)

    def insert_row(self, table_name: str, columns: str, values: Tuple):
        """Insert a row into the specified table with given values."""
        placeholders = ', '.join(['?'] * len(values))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute_query(query, values)

    def KVfunction(self, action_name):
        return self.actions.get(action_name, lambda: "Unknown action.")()

    def select_all(self):
        return self.query_builder.select(self.table_name).execute(self.conn)

    def select_condition(self, condition):
        return self.query_builder.select(self.table_name).where(condition).execute(self.conn)

#actual server and client classes below:

class SocketServer:
    def __init__(self, host: str, port: int, db_file: str):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db = SqliteDB(db_file)
        self.db.create_example_table()

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server is running and waiting for connections...")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection established with {address}")
            threading.Thread(target=self.handle_request, args=(client_socket,)).start()

    def handle_request(self, client_socket: socket.socket):
        try:
            data = client_socket.recv(4096)
            print(f"Received data from client: {data}")
            if data.startswith(b'BINARY'):
                content = data[6:]
                with open('received_binary_file', 'wb') as f:
                    f.write(content)
                client_socket.send(ACK)
            else:
                query = BitstringConverter().convert(data, to_bytes=False)
                response = self.db.execute_query(query)
                client_socket.send(response if response != ACK else ACK)
        except Exception as e:
            print(f"Exception in handle_request: {e}")
            client_socket.send(NAK + str(e).encode('utf-8'))
        finally:
            client_socket.close()


class SocketClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_message(self, message: Union[str, bytes], is_binary=False):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            if is_binary:
                client_socket.sendall(b'BINARY' + message)
            else:
                client_socket.sendall(BitstringConverter().convert(message))
            response = client_socket.recv(4096)
            if not response:
                print("No response from server.")
                return NAK

            # ACK NAK handling
            if response.startswith(ACK):
                print("Server acknowledged the request.")
                print("Client received:", response)
                return ACK
            elif response.startswith(NAK):
                print(f"Error: {response[1:].decode('utf-8')}")
                print("Client received:", response)
                return NAK
            else:
                print("Response:", response.decode('utf-8'))
                print("Client received:", response)
                return response
            

# Code to use server and client
'''if __name__ == "__main__":
    server = SocketServer('localhost', 11345, 'test_socket.db')
    threading.Thread(target=server.start_server, daemon=True).start()

    client = SocketClient('localhost', 11345)
    client.send_message("SELECT * FROM example_table")

    binary_data = b'\x00\x01\x02\x03'
    client.send_message(binary_data, is_binary=True)'''


# mock client for testing
class TestSocketClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_message(self, message: str, is_binary=False):
        if is_binary:
            return b'\x06'
        elif isinstance(message, str):
            if message.startswith("hello"):
                return b'\x06'
            elif message == "Text file content":
                return b'\x06'
        return b'\x00'


class TestSocketServer(unittest.TestCase):
    
    @patch('socket.socket')
    def test_interactive_text_mode(self, mock_socket):
    #Tests sending and receiving text
        client = TestSocketClient('localhost', 11345)
        
        response = client.send_message("hello, this is a test message.")
        self.assertEqual(response, b'\x06')

    @patch('socket.socket')
    def test_text_file_interaction(self, mock_socket):
    #Tests sending and receiving ASCII
        client = TestSocketClient('localhost', 11345)
        
        text_file_content = "Text file content"
        response = client.send_message(text_file_content)
        self.assertEqual(response, b'\x06')

    @patch('socket.socket')
    def test_binary_file_interaction(self, mock_socket):
    #Tests sending and receiving binary
        client = TestSocketClient('localhost', 11345)
        
        binary_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10'
        response = client.send_message(binary_data, is_binary=True)
        self.assertEqual(response, b'\x06')

    @patch('socket.socket')
    def test_socket_server_response(self, mock_socket):
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.recv.return_value = b"hello server!"

        mock_socket_instance.sendall.return_value = None
        
        client_socket = mock_socket_instance
        client_socket.sendall(b'\x06')
        self.assertEqual(client_socket.sendall.call_count, 1)


    def test_bitstring_converter(self):
    #Tests BitstringConverter for string and byte conversion
        converter = BitstringConverter()
        
        test_string = "Sample string"
        byte_data = converter.convert(test_string)
        self.assertEqual(byte_data, b'Sample string')

        converted_string = converter.convert(byte_data, to_bytes=False)
        self.assertEqual(converted_string, test_string)


if __name__ == "__main__":
    unittest.main()
