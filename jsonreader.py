from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import json
import csv

# Blacklist tags
black_list = ['script', 'style']

# Title tags
title_list = ['title', 'h1', 'h2', 'h3', 'h4']

# Body tags
body_list = ['p', 'div', 'span']

# Combined white list
white_list = title_list + body_list

post_titles = []
post_content = []

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def getdata(url):
    # add header to prevent being blocked (403 error) by wordpress websites
    r = requests.get(url, headers=headers)
    return r.text

# Parse & clean all HTML tags
def soupify(url):
    # get entire dom in variable
    soup = BeautifulSoup(url, 'html.parser')
    for tag in soup.find_all(white_list):
        # todo: clean up child tags of each whitelisted tag
        tag.attrs = {}
    return soup
    # extract p-tags
    # for tag in soup.find_all():
    #     if tag.name.lower() in black_list:
    #         tag.decompose()
    #     elif tag.name.lower() in white_list:
    #         tag.attrs = []
    #         print('tag found')
    #     else: 
    #         tag.name = "span"
    #         tag.attrs = []
    #     clean_soup = soup
    #return clean_soup

# Pick the first title to appear
def search_for_title(data):
    for tag in data:
        if tag.name in title_list:
            title = tag
            break
        else:
            title = 'No Title'
        return title

# Split content page by page
def get_all_content(p):
    # Loop through each page
    for post in tqdm(p.keys()):
        post_data = soupify(getdata(post))
        post_title = search_for_title(post_data)
        post_titles.append(post_title)
        p_tags = post_data.find_all('p')
        post_content.append(p_tags)

# Opening JSON file
f = open('ws-data.json')
# returns JSON object as a dictionary
url_dict = json.load(f)
f.close

# Create/Update csv file, add data line by line
def generate_csv():
    print('Generating CSV...')
    get_all_content(url_dict)
    with open('website-content.csv', 'w', newline='', encoding='utf-8') as csvfile:
        listwriter = csv.writer(csvfile, dialect='unix')
        for x in range(len(post_content)):
            listwriter.writerow([post_titles[x], post_content[x]])
    print('CSV creation complete')

generate_csv()