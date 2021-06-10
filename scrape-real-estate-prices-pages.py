import requests
import random
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import time

urls = ["https://www.point2homes.com/CA/Real-Estate-Listings/ON/Toronto.html",
        "https://www.point2homes.com/CA/Condos-For-Sale/ON/Toronto.html",
        "https://www.point2homes.com/CA/Real-Estate-Listings/ON/Markham.html",
        "https://www.point2homes.com/CA/Condos-For-Sale/ON/Markham.html",
        "https://www.point2homes.com/CA/Real-Estate-Listings/ON/Mississauga.html",
        "https://www.point2homes.com/CA/Condos-For-Sale/ON/Mississauga.html"]

df = pd.DataFrame(columns = ['Address', 'Price', 'Beds', 'Baths', 'Space'])

# iterate over pages for each city and category
for link in urls:
    i = 0
    # get name of city
    city = link.split('/')[-1][:-5]
    # get type of listings
    listing = link.split('/')[-3]
    # get HTML from request to web page
    resp = requests.get(link)
    # stores HTML page in a BeautifulSoup object
    soup = BeautifulSoup(r.content)
    # get number of pages to parse through
    num = int(str(soup.find_all('h2')[0]).split()[1].replace(",", ""))//24 + 1
    # initialize page of listings
    link = link + "?page=" + str(i)
    while i < num:
        try:
            i += 1
            link = link[:link.index('?')] + "?page=" + str(i)
            print(link)
            print(i)
            # get HTML from request to web page
            r = requests.get(link)
            # stores HTML page in a BeautifulSoup object
            soup = BeautifulSoup(r.content)
            # use html tag with few matches
            for table in soup.find_all('article'):
                # initialize dataframe row entry
                entry = pd.DataFrame(columns = df.columns).to_dict()        
                # remove newline characters and split by return
                info = table.get_text().strip().split('\r')
                # remove newline characters within array items
                info = [i.strip() for i in info]
                info = [item for info in [i.split('\n') for i in info]  for item in info]
                # fill in table entry data
                for text in info:
                    text = text.strip()
                    if city in text:
                        entry['Address'] = text
                    elif '$' in text:
                        entry['Price'] = text
                    elif ('BedBd' in text) or ('BedsBds' in text):
                        entry['Beds'] = text
                    elif ('BathBa' in text) or ('BathsBa' in text):
                        entry['Baths'] = text
                    elif 'SqftSqft' in text:
                        entry['Space'] = text
                df = df.append(pd.DataFrame(entry, index=[0]))
            # give appropriate delay between pages
            time.sleep(random.randrange(10,20)) # ideally between 10-20 seconds
        except:
            pass
    # convert scraped data into flat file
    df.to_csv(city + '-' + listing + '-' + str(date.today()) + '.csv', index=False)