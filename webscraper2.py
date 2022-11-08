from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import json
import jsonreader

## Request information from user
#ask_site_name = input('Name of site: ')
#website_name = ask_site_name.lower().strip().replace(' ', '-')
ask_site_address = input('Site URL: ')
website = ask_site_address

dict_links = {website:'Not-checked'}

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def getdata(url):
    # add header to prevent being blocked (403 error) by wordpress websites
    r = requests.get(url, headers=headers)
    return r.text



def get_links(website_url, website):
    html_data = getdata(website_url)
    soup = BeautifulSoup(html_data, 'html.parser')
    list_links = []

    for link in soup.find_all('a', href=True):
        # If link starts with provided website url add to list     
        if str(link['href']).startswith(str(website_url)):
            list_links.append(link['href'])
        # If link starts with / then add the web address before putting in list
        if str(link['href']).startswith('/'):
            if link['href'] not in dict_href_links:
                print(link['href'])
                dict_href_links[link['href']] = None
                link_with_www = website + link['href'][1:]
                print('adjusted link =', link_with_www)
                list_links.append(link_with_www)

    # Convert link list to dictionary, define keys as the links and the values
    dict_links = dict.fromkeys(list_links, 'Not-checked')
    return dict_links

# create empty dictionary
dict_href_links = {}

def get_subpage_links(l):
    for link in tqdm(l):
        if l[link] == 'Not-checked':
            # add url to dictionary
            dict_links_subpages = get_links(link, website)
            # add status code to dictionary
            l[link] = requests.get(link, headers=headers).status_code
        else:
            # Create empty dictionary in case every link is checked
            dict_links_subpages = {}
        # Add this dictionary to the old one
        l = {**dict_links_subpages, **l}
    return l

counter, counter2 = None, 0
while counter != 0:
    counter2 += 1
    dict_links2 = get_subpage_links(dict_links)
    # Count number of non-values and set counter to 0 if there are no values within the dictionary equal to the string "Not-checked"
    # https://stackoverflow.com/questions/48371856/count-the-number-of-occurrences-of-a-certain-value-in-a-dictionary-in-python
    counter = sum(value == 'Not-checked' for value in dict_links2.values())
    print('')
    print('LOOP ITERATION NUMBER ', counter2)
    print('LENGTH OF DICTIONARY WITH LINKS = ', len(dict_links2))
    print('NUMBER OF "Not-checked" LINKS = ', counter)
    print('')
    dict_links = dict_links2
    # Save list in json file
    a_file = open('ws-data.json', 'w')
    json.dump(dict_links, a_file)
    a_file.close()

csv_question = input('Generate CSV? (y/n): ')

if csv_question[0:1].lower() == 'y':
    jsonreader.generate_csv()
