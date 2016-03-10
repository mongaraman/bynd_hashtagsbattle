'''
Module Name: test_crawler.py
Author: "Raman Monga"
Email: "mongaraman@gmail.com"
Description: This module contains code for unit testing for Twitter web crawl.
Date: 10th March 2016
'''

import unittest
import requests
from bs4 import BeautifulSoup
from crawler import crawler, get_page_request_object, crawl, spell_mistakes, WORDS_DICT, TWITTER_URL

class TestWebCrawler(unittest.TestCase):
    ''' Test class for Twitter Crawler. '''
	
    def setUp(self):
        '''Initial setup method.'''

        self.tag1 = 'InspiringWomen'
        self.tag2 = 'PURPOSETOUR'
        self.tag1content = [u"We've seen a lot of #InspiringWomen today. @CatPia wanted to make sure our very own @lynda_thomas was on the list. pic.twitter.com/DxGzO3ks9M", u'No matter what, I got you.\n#InspiringWomen\n@poetryinsunsets\n@smochin\n@Kauaibride\n@FlawdnFaithful', u'Some of our most #InspiringWomen from @koganpage, including @pparsons07 & @RuthDowson. Enjoy #InternationalWomensDay pic.twitter.com/tRiwJs42A3']
        self.tag2content = [u'#PURPOSETOUR STARTS TODAY :) pic.twitter.com/VPdxdOQ1xw', u'Justin Bieber kicked off his world tour in style last night  #PurposeTour pic.twitter.com/d5gh0FpD4c', u'j.rabon: \u201cWe don\u2019t know what we be sayin, we just be yellin out Bonjour\u2026\u201d \n#PurposeTour pic.twitter.com/7ndYZPl5HG', u"What do you buddies think of @justinbieber's styling on the #PURPOSETOUR? We LOVE it  pic.twitter.com/bE23Vjf3n9"]

    def test_spell_mistakes(self):
        self.assertEqual(spell_mistakes(self.tag1content), 11)
        self.assertEqual(spell_mistakes(self.tag2content), 15)

    def test_crawler(self):
        crawl_data = crawler(self.tag1, self.tag2)
        self.assertTrue('tag2_num_tweets' in crawl_data)
        self.assertTrue('tag1_num_tweets' in crawl_data)
        self.assertTrue('tag1_num_spell_errors' in crawl_data)
        self.assertTrue('tag2_num_spell_errors' in crawl_data)
        self.assertTrue('num_spell_winner' in crawl_data)
        self.assertTrue('num_tweet_winner' in crawl_data)


if __name__ == '__main__':
    unittest.main()
   

        
