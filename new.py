from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import re
import csv

app = FastAPI()

@app.get("/")
def get_temple_names():
    url = "https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%83%E0%B8%99%E0%B8%88%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%A5%E0%B8%B3%E0%B8%9E%E0%B8%B9%E0%B8%99"
    response = requests.get(url)
    content = response.text

    ret = []
    
    # Find <a>
    pattern = re.compile(r'<a\s+.*?\btitle\s*=\s*(?:"|\')\bวัด(?!ไทย)\S*')
    temple_names = re.findall(pattern, content)
    print("x = ", temple_names)
    
    pattern2 = r'title="([^"\s]+)'
    for name in temple_names:
        match = re.search(pattern2, name)
        ret.append(match.group(1))
        # print(name)
        # print(type(name))
        # print("-------------------")

    # for i in ret:
    #     print(i)
    #     print("----------------------")

    pattern3 = re.compile(r'<li>\s*วัด\S+')
    last_name = re.findall(pattern3, content)
    for i in last_name:
        match = re.search(r'<li>(วัด\S+)', i)
        ret.append(match.group(1))

    # Write temple names to CSV file
    with open('temple_names.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Temple Names'])
        writer.writerows([[name] for name in ret])
    
    return {"message": "Data exported to CSV successfully"}

# uvicorn new:app --reload

# r'<a\s+.*?\btitle\s*=\s*(?:"|\')วัด\S*'