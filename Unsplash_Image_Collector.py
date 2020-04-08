"""

Implementation of the unsplash image collector

Author: Ben Turnbull
"""
from unsplashpy import Unsplash
import requests
from pprint import pprint
import json
import urllib.parse
import os
import shutil
from os import path
import config

#dl_type = 'full'
#dl_type = 'regular'
#dl_type = 'small'
#dl_type = 'thumb'
#number_of_results = 20


def get_with_key(search_text, num_results, image_size):
    print('in key')

    parse_search_term = urllib.parse.quote(search_text)

    url = f"https://unsplash.com/napi/search?query={parse_search_term}&xp=&per_page={num_results}"
    headers = {
        'authorization': f"Client-ID {config.UNSPLASH_API_KEY}"
    }

    response = requests.get(url, headers=headers)
    resp_text = json.loads(response.text)

    pprint(resp_text)

    if 'photos' in resp_text:
        for pgoto in resp_text['photos']['results']:
            if image_size in pgoto['urls']:
                response = requests.get(pgoto['urls'][image_size])
                if response.status_code == 200:
                    if not path.exists(search_text):
                        os.mkdir(search_text)
                    with open(search_text + os.sep + pgoto['id'] + '-' + image_size, 'wb') as f:
                        f.write(response.content)


def get_no_key(search_text, num_pages, image_size='full'):
    u = Unsplash()
    u.search(search_text)
    num_pages = 5 if num_pages == '' else int(num_pages)
    u.download_last_search(num_pages=num_pages, image_size=image_size)


def interactive_input():
    search_text = input('Tell me what are you searching for: ')
    num_results = input('Results to download [10]: ')
    num_results = 10 if num_results == '' else num_results
    num_results = int(num_results)
    image_size = input('Image size to download [regular]: ')
    image_size = 'full' if image_size == '' else image_size
    api_k = ''
    acceptable_resps = ['Y', 'y', 'N', 'n']
    while api_k not in acceptable_resps:
        api_k = input('Use API key Y/N?')
        api_k = api_k.strip()
    if api_k == 'Y' or api_k == 'y':
        get_with_key(search_text, num_results, image_size)
    elif api_k == 'N' or api_k == 'n':
        get_no_key(search_text, num_results, image_size)
    else:
        print('?')


if __name__ == "__main__":
    interactive_input()

