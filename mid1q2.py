import tkinter as tk
from tkinter import ttk, messagebox
import csv
from Querybuilder import QueryBuilder  

class QueryDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Query Display")
        self.root.geometry("600x400") 

        self.qb = QueryBuilder()

        self.mock_data = self.read_mock_data() #the file of data i chose was a csv file

        #creating buttons + text more visible:
        style = ttk.Style()
        style.configure("TButton", foreground="black")

        self.frame_top = ttk.Frame(self.root)
        self.frame_top.pack(pady=10)

        self.query_label = ttk.Label(self.frame_top, text="Select Query Type:", foreground="black")
        self.query_label.grid(row=0, column=0, padx=10)

        self.query_type_var = tk.StringVar(value="select")
        self.query_type = ttk.Combobox(self.frame_top, textvariable=self.query_type_var, foreground="black")
        self.query_type['values'] = ['select', 'insert', 'update', 'delete', 'create_table', 'search']
        self.query_type.grid(row=0, column=1)

        self.execute_btn = ttk.Button(self.frame_top, text="Execute Query", style="TButton", command=self.execute_query)
        self.execute_btn.grid(row=0, column=2, padx=10)

        # displaying the query results
        self.tree = ttk.Treeview(self.root, columns=("QueryType", "Fields", "Values"), show='headings', height=15)
        self.tree.heading('QueryType', text="Type of Query")
        self.tree.heading('Fields', text="Field Headers")
        self.tree.heading('Values', text="Data Values")
        self.tree.column('QueryType', anchor='center', width=100)
        self.tree.column('Fields', anchor='center', width=200)
        self.tree.column('Values', anchor='center', width=300)
        self.tree.pack(pady=20, padx=10)

        style.configure("Treeview.Heading", foreground="black")

    def read_mock_data(self):
        try:
            with open("MOCK_DATA.csv", newline='') as csvfile: # edit the file read, in order to read from the query you want.
                reader = csv.DictReader(csvfile)
                return [row for row in reader]
        except FileNotFoundError:
            messagebox.showerror("Error", "MOCK_DATA.csv not found.")
            return []

    def execute_query(self):
        query_type = self.query_type_var.get().lower()

        if query_type == "select":
            query = self.qb.select("MOCK_DATA", "*", "")
            self.display_all_data(query_type)

        elif query_type == "insert":
            if self.mock_data:  
                for data in self.mock_data:  
                    query, values = self.qb.insert("MOCK_DATA", "(id, first_name, last_name, email)", 
                                                    (data['id'], data['first_name'], data['last_name'], data['email']))
                    self.display_query(query_type, "(id, first_name, last_name, email)", values)

        elif query_type == "update":
            query, values = self.qb.update("MOCK_DATA", {"first_name": "Jane"}, "id = 1")
            self.display_query(query_type, "(first_name = ?)", values)

        elif query_type == "delete":
            query = self.qb.delete("MOCK_DATA", "id = 1")
            self.display_query(query_type, "*", "id = 1")

        elif query_type == "create_table":
            query = self.qb.create_table("MOCK_DATA", "id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT")
            self.display_query(query_type, "id, first_name, last_name, email", "")

        elif query_type == "search":
            query, values = self.qb.search("MOCK_DATA", "John")
            self.display_query(query_type, "*", values)

        else:
            messagebox.showerror("Error", "Invalid Query Type")

    def display_query(self, query_type, fields, values):
        self.tree.delete(*self.tree.get_children())  # Clear previous results
        if not values:
            values = "Default Value"
        self.tree.insert('', 'end', values=(query_type, fields, values))

    def display_all_data(self, query_type):
        # Clear previous results
        self.tree.delete(*self.tree.get_children())
        for data in self.mock_data:
            values = (data['id'], data['first_name'], data['last_name'], data['email'])
            self.tree.insert('', 'end', values=(query_type, "(id, first_name, last_name, email)", values))

if __name__ == "__main__":
    root = tk.Tk()
    app = QueryDisplayApp(root)
    root.mainloop()
