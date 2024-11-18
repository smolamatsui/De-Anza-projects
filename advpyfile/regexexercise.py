import collections
import re

dwarfs_file = 'Dwarfplanets.html'
html_lines = []

with open(dwarfs_file, 'r') as file:
    for line in file:
        html_lines.append(line.strip()) 

regexlist = []

for line in html_lines:
    pattern = re.compile(r'<td>(.*?)</td>')
    matches = pattern.findall(line)
    if matches:
        regexlist.extend(matches)

DwarfPlanet = collections.namedtuple('DwarfPlanet',['name','distance','period'])

i = 0
named_tuples_list = []

while i < len(regexlist):
    nameoftuple = regexlist[i]
    nameoftuple = DwarfPlanet(regexlist[i], regexlist[i + 1], regexlist[i + 2])
    i += 3
    named_tuples_list.append(nameoftuple)


print(named_tuples_list)
