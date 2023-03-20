from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import re
import csv

app = FastAPI()

@app.get("/")
def get_temple_names():
    # Get data from url
    url = "https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%83%E0%B8%99%E0%B8%88%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%A5%E0%B8%B3%E0%B8%9E%E0%B8%B9%E0%B8%99"
    response = requests.get(url)

    # find specific data
    soup = BeautifulSoup(response.text, 'html.parser')
    rare_data = soup.find_all('a', attrs={'title': re.compile(r'^วัด(?!ไทย)')})

    # add data to list
    temple_names = []
    for temple in rare_data:
        # print(temple.text)
        temple_names.append(temple.text)

    # find temple names in simple list
    simple_lists = soup.find_all('ul')
    print(simple_lists.text)
    for simple_list in simple_lists:
        if not simple_list.find_all(True, recursive=False):  # check if there are no nested tags
            items = simple_list.find_all('li', recursive=False)  # find all direct children li tags
            # print(items)
            for item in items:
                match = re.search(r'^วัด(?!ไทย)', item.text.strip())
                if match:
                    temple_names.append(match.group(0))
    
    # print(temple_names)

    # temple_names = list(set(temple_names))

    # write to CSV file
    # with open('temple_names.csv', mode='w', encoding='utf-8', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['Temple Names'])
    #     for name in temple_names:
    #         writer.writerow([name])

    # return {'message': 'Temple names exported to CSV file.'}