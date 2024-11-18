from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import numpy as np
import tkinter as tk

with open('Co2.html', 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

table = soup.find('table')

data_dict = defaultdict(list)

rows = table.find_all('tr')
headers = [header.get_text(strip=True) for header in rows[2].find_all('td')]

for row in rows[3:]:
    cells = row.find_all('td')
    row_data = [cell.get_text(strip=True) or '0' for cell in cells]
    for header, value in zip(headers, row_data):
        data_dict[header].append(value)

df = pd.DataFrame(data_dict)

df['average'] = pd.to_numeric(df['average'], errors='coerce')
annual_data = df.groupby('year')['average'].mean().reset_index() 

def display_yearly_averages():
    root = tk.Tk()
    root.title("CO2 averages by year")

    text_area = tk.Text(root, width=60, height=20)
    text_area.pack(padx=10, pady=10)

    for year, avg in zip(annual_data['year'], annual_data['average']):
        text_area.insert(tk.END, f"Year: {year}, Average CO2:  {avg:.2f}\n")

    text_area.config(state=tk.DISABLED)

    root.mainloop()

display_yearly_averages()
