'''
Module Name: crawler.py
Author: "Raman Monga"
Email: "mongaraman@gmail.com"
Purpose: Twitter hash tags crawler.
Description: This module contains code for creating a console application
to consume a webpage, process some data and present it.
Date: 16th Feb 2016

Example Output json will be:
    {'num_tweet_winner': 'PURPOSETOUR', 'tag2_num_tweets': '21',
     'tag2_num_spell_errors': '68', 'tag1_num_spell_errors': '82',
     'tag1_num_tweets': '19', 'num_spell_winner': 'PURPOSETOUR'}

Assumptions:
1. Twitter posts class will always be under paragraph tag with class name as
   TweetTextSize
'''

import requests
import json
from bs4 import BeautifulSoup
import enchant
from requests.exceptions import HTTPError
import re

WORDS_DICT = enchant.Dict("en_GB")  
TWITTER_URL =  'https://twitter.com/hashtag/'

def get_page_request_object(url):
    ''' Method used to get webpage request object for passed page url.
    Params:
	    None
    Output:
	    Returns a requests object for passed page url or None.
	    Raises requests.exceptions.HTTPError as exception if status code
	    is not 200.
    '''

    try:
        req_obj = requests.get(url)
        req_obj.raise_for_status()
    except HTTPError as req_err:
	    return None
    return req_obj

def crawl(tag):
    ''' Method used to crawl twiter page for specified hash tag.
    Params:
        tag <string> tag name
    Output:
        Returns extracted text from twitter page.
    '''

    try:
        url = TWITTER_URL + tag
        req_obj = get_page_request_object(url)
        req_obj.raise_for_status()
    except HTTPError as req_err:
        return None

    tweet_text = []
    if req_obj:
        xtracted_html = BeautifulSoup(req_obj.text, 'html.parser')
        tweet_text = xtracted_html.select('p.TweetTextSize')
        tweet_text = [text.getText() for text in tweet_text]
    return tweet_text

def spell_mistakes(content):
    ''' Method used to check spelling mistakes from passed content list.
    Params:
        content <list> contatining posts text
    Returns:
        int - len of list containing misspelled words
    '''

    mistakes = []
    for post in content:
        # clean up string by removing special chars
        wrds = re.sub('[!@#$/\:,.\n]', '', post).split()
        for wrd in wrds:
            #encode word to handle special chars
            wrd = wrd.encode('ascii', 'ignore')
            if wrd:
                if not WORDS_DICT.check(wrd): # check spelling mistake
                    mistakes.append(wrd)
    return len(mistakes)

def crawler(tag1, tag2):
    ''' Method used to crawl for different pass hashtag pages and return result.
    Params:
        tag1 <str> string first hash tag name
        tag2 <str> string second hash tag name
    Returns:
        result dict containing tags stats.
        e.g {'num_tweet_winner': 'PURPOSETOUR', 'tag2_num_tweets': '21',
             'tag2_num_spell_errors': '68', 'tag1_num_spell_errors': '82',
             'tag1_num_tweets': '19', 'num_spell_winner': 'PURPOSETOUR'}
    '''
    res = {}
    content1=crawl(tag1)
    content2=crawl(tag2)
    sp_mistakes1 = spell_mistakes(content1)
    sp_mistakes2 = spell_mistakes(content2)
    cnt_based = tag1 if len(content1) > len(content2) else tag2
    spell_based = tag1 if sp_mistakes2 > sp_mistakes1 else tag2
    res['tag1_num_tweets'] = str(len(content1))
    res['tag2_num_tweets'] = str(len(content2))
    res['tag1_num_spell_errors'] = str(sp_mistakes1)
    res['tag2_num_spell_errors'] = str(sp_mistakes2)
    res['num_tweet_winner'] = str(cnt_based)
    res['num_spell_winner'] = str(spell_based)
    return res

