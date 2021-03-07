import csv
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/Pennsylvania_State_University_Commonwealth_campuses'
table_xpath = '/html/body/div[3]/div[3]/div[5]/div[1]/table[1]'
table_class = 'sortable wikitable'
tag_exclude = 'sup'

header = []
data = []

# cURL get URL and parse with bs4
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table
table = soup.find('table', class_=table_class)

# Append all found headers to list
for th in table.find_all('th'):

    h = th.get_text()
    header.append(h)

# Look for table row and the table data within
for tr in table.find_all('tr'):

    # Check for no subtable
    if tr.find('th') == None:
        campus = {}

        # Iterate through the data within row
        for index, info in enumerate(tr.find_all('td')):
            
            # Check for unwanted tags
            if info(tag_exclude):
                info.find(tag_exclude).decompose()

            campus[ header[index] ] = info.get_text()

        data.append(campus)

print(header, '\n')
print(data, '\n')

# Create a new csv file, write data to it
with open('campus.csv', 'w', newline='') as csvfile:

    writer = csv.DictWriter(csvfile, header)
    writer.writeheader()

    for j in data:
        writer.writerow(j)