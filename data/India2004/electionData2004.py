import time
import csv
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
#driver = webdriver.Chrome("/home/sanit/Desktop/chromedriver")
url = 'https://www.indiavotes.com/pc/info?state=0&eid=14'
##print(url.status_code)

#c = uReq(url, context = ctx)

driver.get(url)

time.sleep(3)

#print(c)

soup = BeautifulSoup(driver.page_source, "html5lib")

my_table = soup.find('table', attrs = {'id' : 'DataTables_Table_0'})
constituencies = my_table.find_all('td', class_='tal sorting_1')

for constituency in constituencies:
    print(constituency.text)
    sub_url = constituency.find('a')['href']
    driver.get(sub_url)
    time.sleep(2)

    sub_soup = BeautifulSoup(driver.page_source, "html5lib")
    sub_table = sub_soup.find('table', attrs = {'id' : 'DataTables_Table_0'})
    
    output_rows = [['x', 'Position', 'Candidate Name', 'Votes', 'Votes %', 'Party', 'AC']]

    for table_row in sub_table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        if output_row != []:
            output_rows.append(output_row)
    
    with open(f"{constituency.text}_2004.csv", 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)


# data.sort()

# print(data)

# with open("electionData2004.json", 'w') as f:

#   json.dump(data, f, indent = 2)