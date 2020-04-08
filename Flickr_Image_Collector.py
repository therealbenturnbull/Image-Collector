#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## run
## > python flickr_GetUrl.py tag number_of_images_to_attempt_to_download
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import json
import requests
from os import path
import os

from flickrapi import FlickrAPI
import config


def flickr_image_collect(search_text, max_count):
    flickr = FlickrAPI(config.FLICKR_API_KEY, config.FLICKR_API_SECRET, format='parsed-json')
    #extras = 'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o,license,title,user_id'
    extras = 'url_o,license,title,user_id'
    photo_search = flickr.photos.search(text=search_text,
                                        per_page=max_count,
                                        extras=extras,
                                        license=4,
                                        format='json',
                                        sort='relevant')

    photo_search_outcome = json.loads(photo_search)

    for photo in photo_search_outcome['photos']['photo']:
        print(photo)
        if 'url_o':
            response = requests.get(photo['url_o'])
            if response.status_code == 200:
                if not path.exists(search_text):
                    os.mkdir(search_text)
                with open(search_text + os.sep + photo['id'] + '-full.jpg', 'wb') as f:
                    f.write(response.content)


def interactive_input():
    search_text = input('Tell me what are you searching for: ')
    num_results = input('Results to download [10]: ')
    num_results = 10 if num_results == '' else num_results
    num_results = int(num_results)
    flickr_image_collect(search_text, num_results)


if __name__ == "__main__":

    interactive_input()
    #flickr_image_collect("kittens", 20)
    #search_text = 'egg bacon'
    #MAX_COUNT = 20

