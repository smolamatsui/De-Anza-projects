#part 1

def FindSubString(s,ss):
    return s.find(ss,0,len(s))

def FindendofSubString(s,ss):
    return (s.find(ss,0,len(s)) + len(ss))

listofproducts = []
xml_file = '/Users/sophia/Desktop/Programming/De Anza python course/Products.xml'

xml_lines = []

with open(xml_file, 'r') as file:
    for line in file:
        xml_lines.append(line.strip()) 

for line in xml_lines:
    x = FindSubString(line, "</Product>")
    if x != -1:
        listofproducts.append(line[FindendofSubString(line, "<Product>") : FindSubString(line, "</Product>")])


print("(Part 1) Here is the list of products achieved through String Processing: ")
print(listofproducts)

#part 2

import re

regexlist = []

for line in xml_lines:
    pattern = re.compile(r'<Product>(.*?)</Product>')
    matches = pattern.findall(line)
    if matches:
        regexlist.extend(matches)


print("(Part 2) Here is the list of products achieved through Regex: ")
print(regexlist)

