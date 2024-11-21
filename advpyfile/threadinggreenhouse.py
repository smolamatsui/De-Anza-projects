import threading
import queue
from queue import Queue
import sqlite3
from tkinter import Tk, ttk
import tkinter as tk
from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest

# 1. WebScraper Class
class WebScraper:
    def __init__(self, url: str):
        self.url = url

    def scrape_table_2(self):
        try:
            response = urlopen(self.url)
        except Exception as e:
            print(f"Error accessing the URL: {e}")
            return []
        try:
            soup = BeautifulSoup(response, 'html.parser')
        except Exception as e:
            print(f"Error parsing HTML content: {e}")
            return []
        tables = soup.select('table')
        if not tables:
            print("No tables found on the webpage.")
            return []
        try:
            emissionstable2_data = tables[-1]
            rows = emissionstable2_data.find_all('tr')
        except Exception as e:
            print(f"Error extracting data from table: {e}")
            return []

        data = []
        for row in rows:
            headers = row.find_all('th')
            cells = row.find_all('td')

            if headers:
                continue
            if cells:
                try:
                    year = int(cells[0].text.strip())
                    gas_data = [
                        float(cells[i].text.strip().replace(',', '')) if cells[i].text.strip() else 0.0
                        for i in range(1, 7)
                    ]
                    data.append([year] + gas_data)
                except ValueError as e:
                    print(f"Error converting cell data: {e}")
                    continue
        return data


# 2. SqliteDB Class
class SqliteDB:
    def __init__(self, db_name):
        try:
            self.db_name = db_name
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")
            raise

    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS greenhouse_data (
                                    year INTEGER PRIMARY KEY,
                                    CO2 REAL,
                                    CH4 REAL,
                                    N2O REAL,
                                    CFCs REAL,
                                    HCFCs REAL,
                                    HFCs REAL
                                )''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            raise

    def insert_data(self, data):
        try:
            for row in data:
                self.cursor.execute('''INSERT OR REPLACE INTO greenhouse_data 
                                        (year, CO2, CH4, N2O, CFCs, HCFCs, HFCs)
                                        VALUES (?, ?, ?, ?, ?, ?, ?)''', row)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data into the database: {e}")

    def get_year_data(self, year):
        try:
            self.cursor.execute('SELECT CO2, CH4, N2O, CFCs, HCFCs, HFCs FROM greenhouse_data WHERE year = ?', (year,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving data for year {year}: {e}")
            return None
        
    def select_all(self):
        return self.query_builder.select(self.table_name).execute(self.conn)

    def select_condition(self, condition):
        return self.query_builder.select(self.table_name).where(condition).execute(self.conn)

    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")


# 3. Server Class
class Server:
    def __init__(self, db: SqliteDB):
        self.db = db
        self.lock = threading.Lock()

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server is running and waiting for connections...")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection established with {address}")
            threading.Thread(target=self.handle_request, args=(client_socket,)).start()

    def handle_request(self, year):
        with self.lock:
            try:
                return self.db.get_year_data(year)
            except Exception as e:
                print(f"Error handling request for year {year}: {e}")
                return None


# 4. Client Class
class Client(threading.Thread):
    def __init__(self, server, gas_index, result_queue, start_year=1979, end_year=2022):
        super().__init__()
        self.server = server
        self.gas_index = gas_index
        self.result_queue = result_queue
        self.start_year = start_year
        self.end_year = end_year

    def run(self):
        print(f"Client {self.gas_index} started...")
        for year in range(self.start_year, self.end_year + 1):
            try:
                data = self.server.handle_request(year)
                if data:
                    self.result_queue.put((year, self.gas_index, data[self.gas_index]))
            except Exception as e:
                print(f"Error in client {self.gas_index} for year {year}: {e}")
        print(f"Client {self.gas_index} finished.")


# 5. GreenhouseUI Class
class GreenhouseUI:
    def __init__(self, root, result_queue, gases):
        self.root = root
        self.result_queue = result_queue
        self.gases = gases
        self.tabs = {}
        self.setup_ui()
        self.poll_queue()

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        for gas in self.gases:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=gas)
            self.tabs[gas] = {"frame": tab, "data": {}}

    def poll_queue(self):
        while not self.result_queue.empty():
            try:
                year, gas_index, value = self.result_queue.get_nowait()
                gas_name = self.gases[gas_index]
                tab_info = self.tabs[gas_name]

                if year not in tab_info["data"]:
                    tab_info["data"][year] = value
                    self.update_tab(tab_info["frame"], tab_info["data"])
            except queue.Empty:
                pass

        self.root.after(100, self.poll_queue)

    def update_tab(self, tab, data):
        for widget in tab.winfo_children():
            widget.destroy()

        sorted_data = sorted(data.items())
        for i, (year, value) in enumerate(sorted_data):
            tk.Label(tab, text=f"{year}", fg="black").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            tk.Label(tab, text=f"{value:.3f}", fg="black").grid(row=i, column=1, padx=5, pady=2, sticky="w")


def main():
    url = "https://gml.noaa.gov/aggi/aggi.html"
    scraper = WebScraper(url)
    data = scraper.scrape_table_2()

    db_name = "greenhouse.db"
    sqlite_db = SqliteDB(db_name)
    sqlite_db.insert_data(data)

    server = Server(sqlite_db)
    result_queue = queue.Queue()

    clients = [Client(server, gas_index, result_queue) for gas_index in range(6)]
    for client in clients:
        client.start()

    root = Tk()
    root.title("Greenhouse Gas Data")

    app = GreenhouseUI(root, result_queue, ["CO2", "CH4", "N2O", "CFCs", "HCFCs", "HFCs"])
    root.mainloop()

    for client in clients:
        client.join()

if __name__ == "__main__":
    main()




#Unit test
class TestGreenhouseSystem(unittest.TestCase):
    def setUp(self):
        self.url = "https://gml.noaa.gov/aggi/aggi.html"
        self.scraper = WebScraper(self.url)
        self.db_name = "test_greenhouse.db"
        self.sqlite_db = SqliteDB(self.db_name)
        data = self.scraper.scrape_table_2()
        self.sqlite_db.insert_data(data)

        self.server = Server(self.sqlite_db)
        self.result_queue = Queue()

    def tearDown(self):
        self.sqlite_db.close()

    def test_data_scraping(self):
        data = self.scraper.scrape_table_2()
        self.assertTrue(len(data) > 0, "Scraped data should not be empty.")

    def test_database_insertion(self):
        year = 1979
        data = self.sqlite_db.get_year_data(year)
        self.assertIsNotNone(data, f"Data for year {year} should not be None.")

    def test_thread_safety(self):
        def client_thread(gas_index, queue):
            for year in range(1979, 1981):  
                data = self.server.handle_request(year)
                if data:
                    queue.put((year, gas_index, data[gas_index]))

        threads = []
        for gas_index in range(6):
            t = threading.Thread(target=client_thread, args=(gas_index, self.result_queue))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.assertFalse(self.result_queue.empty(), "Result queue should not be empty after thread execution.")

if __name__ == "__main__":
    unittest.main()
