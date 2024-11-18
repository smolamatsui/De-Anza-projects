from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions_per_capita'
response = urlopen(url)
soup = BeautifulSoup(response, 'html.parser')

def findTag(wpage, tag):
    return wpage.select(tag)

tables = findTag(soup, 'table')

emmisionstable_data = [] # stores data for the emissions per capita table

for table in tables:
    caption = table.select_one('caption')
    if caption and 'emissions per capita' in caption.text.lower():
        rows = table.select('tr') 
        for row in rows:
            headers = row.select('th') 
            cells = row.select('td')
            if headers:
                emmisionstable_data.append([header.text.strip() for header in headers])
            if cells:
                emmisionstable_data.append([cell.text.strip() for cell in cells])
        break  

print("Here are the contents of the emissions per capita table. \n")
print(emmisionstable_data)

tables = findTag(soup, 'table')

tag_dict = defaultdict(lambda: "there is no such table") #dict for all tables + their contents

for i, table in enumerate(tables):
    key = f'table{i}'  
    rows = table.select('tr') 
    table_content = [] 
    for row in rows:
        headers = row.select('th')  
        cells = row.select('td') 
        if headers:
            table_content.append([header.text.strip() for header in headers])
        if cells:
            table_content.append([cell.text.strip() for cell in cells])
    tag_dict[key] = table_content

print("\n\n\n Here is dictionary of all the contents in each table\n")
print(tag_dict)
