# -*- coding: utf-8 -*-
import json
import logging
import sys
import datetime
import calendar
import scrapy
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from scrapy.http import JSONRequest
from airbnb_scraper.items_rv import AirbnbScraperItem


# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb_rv'
    allowed_domains = ['www.airbnb.de']
    
    def start_requests(self):

        f = open ('room-ids.txt', 'r')
        fl = f.readlines()

        for room_id in fl:
            room_id = room_id.rstrip()
            url = ('https://www.airbnb.de/api/v2/homes_pdp_reviews?currency=EUR&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=de&listing_id={0}&_format=for_p3&order=language_country')
            url = url.format(room_id)
            yield scrapy.Request(url=url, callback=self.parse, meta={"room_id" : room_id})


    def parse(self, response):
       
        # Fetch and Write the response data
        data = json.loads(response.body)
       
        # Debugging response
        ## Write response to file
        filename = 'rv-data/airbnb_rv_' + response.meta['room_id'] + '.json'
        with open(filename, 'wb') as f:
           f.write(response.body)
        self.log('Saved file %s' % filename)

        listing = AirbnbScraperItem()
        listing['room_id'] = response.meta['room_id']

        reviews = data.get('reviews')

        for review in reviews:
            listing['comments'] = review.get('comments')
            yield listing