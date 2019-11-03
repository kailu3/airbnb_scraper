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
from airbnb_scraper.items_av import AirbnbScraperItem


# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb_av'
    allowed_domains = ['www.airbnb.de']
    
    def start_requests(self):

        f = open ('room-ids.txt', 'r')
        fl = f.readlines()

        for room_id in fl:
            url = ('https://www.airbnb.de/api/v2/homes_pdp_availability_calendar?currency=EUR&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=de&listing_id={0}&month=11&year=2019&count=12')
            url = url.format(room_id)
            yield scrapy.Request(url=url, callback=self.parse, meta={"room_id" : room_id})


    def parse(self, response):
       
        # Fetch and Write the response data
        data = json.loads(response.body)
       
        # Debugging response
        ## Write response to file
        # filename = 'airbnb_av-debug.json'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        months = data.get('calendar_months')

        listing = AirbnbScraperItem()

        listing['room_id'] = response.meta['room_id'].rstrip()

        for month in months:
            days = month.get('days')
            days_count = 0
            for day in days:
                if day.get('available'):
                    days_count = days_count + 1
            month_idx = month.get('month')
            month_name = calendar.month_name[month_idx]
            #date = datetime.datetime(year, month, 1)
            listing[month_name] = days_count

        
        yield listing
