from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

@app.get("/")
def get_temple_names():
    # Get data from url
    url = "https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%83%E0%B8%99%E0%B8%88%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%A5%E0%B8%B3%E0%B8%9E%E0%B8%B9%E0%B8%99"
    response = requests.get(url)

    # find specific data
    soup = BeautifulSoup(response.text, 'html.parser')
    rare_data = soup.find_all('a')
    
    # add data to list
    temple_names = []
    for temple in rare_data:
        if temple.has_attr('title'):
            # temp = temple.string
            print(temple)
            # if re.match(r'^วัด\w+', temp):
            #     temple_names.append(temp)

    print(temple_names)