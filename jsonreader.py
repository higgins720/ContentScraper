from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import json
import csv

# Tags we don't want
black_list = ['script', 'style', 'iframe']

# What we want
white_list = ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4']

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

# Open JSON file
f = open('ws-data.json')
# return JSON object as a dictionary
url_dict = json.load(f)
f.close

def getdata(url):
    # add header to prevent being blocked (403 error) by wordpress websites
    r = requests.get(url, headers=headers)
    return r.text

# Parse & clean all HTML tags
def make_soup(url):
    # get entire dom in variable
    soup = BeautifulSoup(url, 'html.parser')
    for tag in soup.find_all(black_list):
        tag.decompose()
    return soup

# Pick the first title to appear
def get_title(soup):
    title = soup.find('h1')
    if (title != None):
        site_titles.append(title)
    else:
        site_titles.append('No Title')

def get_body(soup):
    for tag in soup.find_all(white_list):
        tag.attrs = {}
        site_content.append(tag)

site_titles = []
site_content = []

# Visit each page, make soup, split into separate lists
def parse_dict(p):
    for post in tqdm(p.keys()):
        soup = make_soup(getdata(post))
        get_title(soup)
        get_body(soup)

# Create/Update csv file, add data line by line
def generate_csv():
    print('Generating CSV...')
    parse_dict(url_dict)
    with open('website-content.csv', 'w', newline='', encoding='utf-8') as csvfile:
        listwriter = csv.writer(csvfile, dialect='unix')
        for x in range(len(site_titles)):
            listwriter.writerow([site_titles[x], site_content[x]])
    print('CSV creation complete')

generate_csv()