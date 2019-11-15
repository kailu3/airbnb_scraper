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
from airbnb_scraper.items_pr import AirbnbScraperItem


# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb_pr'
    allowed_domains = ['www.airbnb.de']
    
    def start_requests(self):

        #f = open ('room-ids-all.txt', 'r')
        f = open ('room-ids.txt', 'r')
        fl = f.readlines()

        for room_id in fl:
            room_id = room_id.rstrip()
            url = ('https://www.airbnb.de/api/v2/homes_pdp_availability_calendar?currency=EUR&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=de&listing_id={0}&month=11&year=2019&count=12')
            url = url.format(room_id)
            yield scrapy.Request(url=url, callback=self.parse, meta={"room_id" : room_id})


    def parse(self, response):
       
        # Fetch and Write the response data
        data = json.loads(response.body)
       
        # Debugging response
        ## Write response to file
        #filename = 'airbnb_av-debug' + response.meta['room_id'] + '.json'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)

        months = data.get('calendar_months')        

        for month in months:            
            first_av_day_found = False
            days_count = 0
            nights_count = 0
            checkin_day = ''
            checkout_day = ''
            min_nights = 0

            month_idx = month.get('month')
            month_name = calendar.month_name[month_idx]

            url = ('https://www.airbnb.de/api/v2/pdp_listing_booking_details?_format=for_web_with_date&'
                '_intents=p3_book_it&_interaction_type=pageload&_p3_impression_id=p3_1573730384_JCTS15pwa9INrly2&'
                '_parent_request_uuid=6f97489a-5f30-4d2d-9398-44ae7e4be427&'
                'check_in={0}&check_out={1}&currency=EUR&'
                'force_boost_unc_priority_message_type=&guests=1&'
                'key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id={2}&'
                'locale=de&number_of_adults=1&number_of_children=0&number_of_infants=0&show_smart_promotion=0')

            days = month.get('days')
            
            for day in days:                
                if day.get('available'):
                    days_count = days_count + 1
                    if first_av_day_found == False:
                        first_av_day_found = True
                        checkin_day = day.get('date')                        
                        min_nights = day.get('min_nights')
                        nights_count = 0
                    else:
                        nights_count = nights_count + 1
                        if nights_count == min_nights:
                            checkout_day = day.get('date')
                            url = url.format (checkin_day, checkout_day, response.meta['room_id'])
                            yield JSONRequest(url=url, callback=self.parse_booking_details, meta={"room_id" : response.meta['room_id'], "month" : month_name, "min_nights" : min_nights, "checkin_day" : checkin_day, "checkout_day" : checkout_day})
                            break
 
          #prices.append(float(day.get('price').get('local_price_formatted').replace("€","")))
         

        # prices = get('price')#.get('local_price_formatted').replace("€","")

        # date = datetime.datetime(year, month, 1)
        # listing[month_name + '_avail_days'] = days_count
        # listing[month_name + '_count_price'] = int(len(prices))
        # listing[month_name + '_avg_price'] = "{:5.2f}".format(sum(prices) / len(prices)).replace(".",",")
        # listing[month_name + '_min_price'] = "{:5.2f}".format(min(prices)).replace(".",",")
        # listing[month_name + '_max_price'] = "{:5.2f}".format(max(prices)).replace(".",",")
        # listing[month_name + '_max_diff_price'] = "{:5.2f}".format(max(prices) - min(prices)).replace(".",",")




        
        
    def parse_booking_details(self, response):
        # Fetch and Write the response data
        data = json.loads(response.body)
        prices = {}
       
        # Debugging response
        ## Write response to file
        # filename = 'airbnb_av-debug' + response.meta['room_id'] + '.json'
        # with open(filename, 'wb') as f:
        #    f.write(response.body)
        # self.log('Saved file %s' % filename)

        listing = AirbnbScraperItem()
        booking_details = data.get('pdp_listing_booking_details')[0]

        prices = []
        price = {}
        
        price['type'] = 'average_rate_without_tax_usd'
        price['localized_title'] = 'N/A'
        price['amount'] = booking_details.get('average_rate_without_tax_usd')
        prices.append(dict(price))

        price['type'] = 'extra_guest_fee'
        price['localized_title'] = 'N/A'
        price['amount'] = booking_details.get('extra_guest_fee').get('amount')
        prices.append(dict(price))

        price['type'] = 'nightly_rate'
        price['localized_title'] = 'N/A'
        price['amount'] = booking_details.get('rate_with_service_fee').get('amount')
        prices.append(dict(price))
        

        #display_prices = booking_details.get('bar_price').get('display_prices')
        #for d in display_prices:
        #    prices['dp:' + d.get('display_rate_type')] = d.get('price_string').replace("€","").rstrip()
        
        price_items = booking_details.get('price').get('price_items')
        for i in price_items:            
            price['type'] = i.get('type')
            price['localized_title'] = i.get('localized_title')
            price['amount'] = i.get('total').get('amount')
            prices.append(dict(price))
        
        

        for p in prices:
            listing['room_id'] = response.meta['room_id']
            listing['month'] = response.meta['month']
            listing['price_type'] = p.get('type')
            listing['price_localized_title'] = p.get('localized_title')      
            listing['price_amount'] = "{:5.2f}".format(p.get('amount')).replace(".",",")     
            yield listing

        

        #listing['room_id'] = response.meta['room_id']
        #listing['month'] = response.meta['month']
        #listing['min_nights'] = response.meta['min_nights']
        #listing['checkin_day'] = response.meta['checkin_day']
        #listing['checkout_day'] = response.meta['checkout_day']
        
