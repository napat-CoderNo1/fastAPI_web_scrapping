from fastapi import FastAPI
import requests
import re
import csv

app = FastAPI()

@app.get("/")
def get_temple_names():
    url = "https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B9%83%E0%B8%99%E0%B8%88%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%A7%E0%B8%B1%E0%B8%94%E0%B8%A5%E0%B8%9E%E0%B8%9A%E0%B8%B8%E0%B8%A3%E0%B8%B5"
    response = requests.get(url)
    content = response.text

    ret = []

    # get all tag in tag div class "mw-parser-output"
    pattern1 = re.compile(r'<div\s+class="mw-parser-output">([\s\S]*?)<\/div>')
    all_tags = re.findall(pattern1, content)
    # print(type(all_tags))
    # print(all_tags[0])

    # get only <ul>
    ul_list = []
    pattern2 = r'<ul>[\s\S]*?<\/ul>'
    for i in all_tags:
        ul_match = re.findall(pattern2, i)
        if ul_match:
            for ul_content in ul_match:
                ul_list.append(ul_content)
    # print(ul_list)
    # print(len(ul_list))

    # get <li> in <ul>
    li_list = []
    pattern3 = r'<li>[\s\S]*?<\/li>'
    for i in ul_list:
        li_match = re.findall(pattern3, i)
        if li_match:
            for li_content in li_match:
                li_list.append(li_content)
    # print(li_list)

    # get <a> in <li>
    a_list = []
    pattern4 = r'<a\s+.*?>[\s\S]*?<\/a>'
    for i in li_list:
        a_match = re.findall(pattern4, i)
        if a_match:
            for a_content in a_match:
                a_list.append(a_content)
    # print(a_list)

    # get <a> that have title "วัด" bnd not follow by "ไทย"
    awat_list = []
    pattern5 = r'<a\s+.*?title=".*?วัด(?!ไทย).*?".*?>[\s\S]*?<\/a>'
    for i in a_list:
        awat_match = re.findall(pattern5, i)
        if awat_match:
            for awat_content in awat_match:
                awat_list.append(awat_content)
    # print(awat_list)

    # get temple name from <a>
    pattern6 = r'title="([^"\s]+)'
    for i in awat_list:
        match = re.search(pattern6, i)
        if match.group(1) not in ret:
            ret.append(match.group(1))
    # print(ret)

    # get <li> that not have a page
    pattern7 = r'<li>(?=\s*วัด)[^<>\n]*<\/li>'
    
    # get name from list start with วัด and end when found whitespace
    pattern8 = r'<li>(?=\s*วัด)([^\s<>\n]*)'
    
    for i in li_list:
        if re.match(pattern7, i):
            match = re.search(pattern8, i)
            if match:
                if match.group(1) not in ret:
                    ret.append(match.group(1))
                

    # Write temple names to CSV file
    with open('temple_names.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Temple Names'])
        writer.writerows([[name] for name in ret])
        
    return {"message": "Data exported to CSV successfully"}

# uvicorn newnew:app --reload