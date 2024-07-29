import requests
import bs4
import csv
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from random import randint
headers = {"Accept-Language": "en-US,en;q=0.5"}
tabs = np.arange(1,1000,100)
data=[]
for response in tabs:
    response = requests.get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(response)+"&ref_=adv_nxt")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    soup_list= soup.find_all('div', class_="lister-item mode-advanced")
    sleep(randint(2,8))
    l=0
    for x in soup_list:
        Title = x.h3.a.text
        Release = x.h3.find('span', class_='lister-item-year text-muted unbold').text.replace('(', '').replace(')', '').replace('I','').replace('II','').replace('III','')
        Length = x.p.find('span', class_ = 'runtime').text.replace(' min', '')
        Genre = x.p.find('span', class_ = 'genre').text.replace('\n','')
        Rating = x.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n', '')
        info_1 = x.find_all('span',attrs = {'name':'nv'}) 
        Votes = info_1[0].text
        brief = x.find_all('p', class_ = 'text-muted')
        Summary = brief[1].text.replace('\n', '') if len(brief) >1 else '---'
        info_2 = x.find("p", class_ = '')
        info_2 = info_2.text.replace('\n','').split('|')
        info_2 = [a.strip() for a in info_2]
        info_2 = [info_2[i].replace(j,"") for i,j in enumerate(["Director:"])]
        f = [Title,Release,Genre,info_2[0].replace('Directors:',''),Length,Rating,Summary] 
        l+=1
        data.append(f)
        fields = [ 'Title', 'Release','Genre', 'Director', 'Length', 'Rating','Summary'] 
        file = "C:/Users/jashw/Imdb_insights.csv"
        with open(file,'w',newline='',encoding='utf8') as output:
            csvwriter = csv.writer(output)
            csvwriter.writerow(fields)
            csvwriter.writerows(data)    