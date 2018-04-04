# Libraries export
from bs4 import BeautifulSoup
import requests

import pandas as pd

# regex module 
import re

# lbc search
url = 'https://www.leboncoin.fr/motos/offres/provence_alpes_cote_d_azur/?th=1&q=*vespa%20gt*%20OR%20PX%20OR%20LML%20NOT%20solex%20NOT%20ciao%20NOT%20gts%20NOT%20gt-s%20NOT%20200%20NOT%20neuf%20NOT%20trail&parrot=2&ps=4'

# Request content from web page
result = requests.get(url)
c = result.content

# Set as Beautiful Soup Object
soup = BeautifulSoup(c)

# Take all title and price tag
summary = soup.findAll('a', {'class':'list_item clearfix trackable'})

# title
ad_title = summary[0].get('title')

# price
ad_price = soup.find_all('h3', class_='item_price')
ad_price = ad_price[0].get('content')
ad_price

# list id
get_numeric = r'\d+'
listid = re.findall(get_numeric, str(summary[0]))
ad_list_id = listid[0]

# url
ad_url = summary[0].get('href')

# publication date
ad_publication_date = soup.find_all('p', class_='item_supp')
ad_publication_date = ad_publication_date[2].get('content')

# gest last ad_list_id
previous_ad_list_id = pd.read_csv('df_vespa.csv', sep=';')
previous_ad_list_id = previous_ad_list_id.ad_list_id.iloc[-1]
previous_ad_list_id = str(previous_ad_list_id)

# Check if there is a new ad
if previous_ad_list_id != ad_list_id:
    # send new sms
    account = "ACcec09159a0cadfc83fe867a404b8851c"
    token = "4a6031d6d20c98536f6f5acc5e260b2a"
    client = Client(account, token)
    message = client.messages.create(to="+33659241060", 
                                 from_="+33757916182",
                                 body="""
                                         
                                         
                                         Hello Dad! Nouvelle annonce à consulter : """ 
                                         + ad_title 
                                         + ' - ' 
                                         + ad_price 
                                         + ' - ' 
                                         + ad_url 
                                         + ' - Fonce !' )
    
    # add the new ad to the df_vespa.csv
    new_vespa_ad = {'ad_title' : ad_title, 'ad_list_id' : ad_list_id, 'ad_url' : ad_url}
    new_vespa_ad = pd.DataFrame(index=[ad_publication_date], data=new_vespa_ad)
    # append date and retention value to the csv
    new_vespa_ad.to_csv('df_vespa.csv', mode='a', header=False, encoding='UTF-8', sep=';')
    
    # print log
    print('New available ad:')
    print(ad_title)
    print('---')
    print(ad_price)
    print('---')
    print(ad_publication_date)
    print('---')
    print(ad_list_id)
    print('---')
    print(ad_url)
else:
    print('No new Ad')
