import os
import re
import tkinter as tk
from tkinter import Listbox, Text, Scrollbar

class Pyifelse:
    def __init__(self, root):
        self.root = root
        self.root.title(".py file if/else")
        self.root.geometry("600x400")
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)       
        self.listbox = Listbox(self.frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)       
        self.scrollbar = Scrollbar(self.frame, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)      
        self.listbox.config(yscrollcommand=self.scrollbar.set)     
        self.open_button = tk.Button(self.root, text="Select Directory", command=self.load_current_directory)
        self.open_button.pack(side=tk.TOP, pady=5)    
        self.textbox = Text(self.root)
        self.textbox.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)    
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
    
    def currentDir(self):
        return os.getcwd()

    def load_current_directory(self):
        directory = self.currentDir()
        if directory:
            self.listbox.delete(0, tk.END)
            self.load_files(directory)
    
    def load_files(self, directory):
        for file in os.listdir(directory):
            if file.endswith(".py"):
                self.listbox.insert(tk.END, os.path.join(directory, file))
                
    def on_select(self, event):
        selected_file = self.listbox.get(self.listbox.curselection())
        self.process_file(selected_file)
        
    def process_file(self, filepath):
        with open(filepath, 'r') as file:
            content = file.readlines()
        
        if_statements = self.extract_if_statements(content)
        self.display_if_statements(if_statements)
    
    def extract_if_statements(self, content):
        if_statements = []
        pattern = re.compile(r'^\s*(if|elif|else).*:\s*$')
        for line in content:
            if pattern.match(line):
                if_statements.append(line.strip())
        return if_statements
    
    def display_if_statements(self, if_statements):
        self.textbox.delete(1.0, tk.END)
        for stmt in if_statements:
            self.textbox.insert(tk.END, stmt + "\n")

root = tk.Tk()
app = Pyifelse(root)
root.mainloop()
