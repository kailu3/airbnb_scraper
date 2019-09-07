# -*- coding: utf-8 -*-
import json
import collections
import re
import numpy as np
import logging
import sys
import scrapy
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
from airbnb_scraper.items import AirbnbScraperItem


# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com']

    '''
    You don't have to override __init__ each time and can simply use self.parameter (See https://bit.ly/2Wxbkd9),
    but I find this way much more readable.
    '''
    def __init__(self, city='',price_lb='', price_ub='', *args,**kwargs):
        super(AirbnbSpider, self).__init__(*args, **kwargs)
        self.city = city
        self.price_lb = price_lb
        self.price_ub = price_ub

    def start_requests(self):
        '''Sends a scrapy request to the designated url price range

        Args:
        Returns:
        '''

        url = ('https://www.airbnb.de/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1'
              '&allow_override%5B%5D=&auto_ib=true&checkin=2019-09-20&checkout=2019-09-22&client_session_id='
              '621cf853-d03e-4108-b717-c14962b6ab8b&currency=EUR&experiences_per_grid=20&fetch_filters=true'
              '&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true'
              '&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18'
              '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&'
              'query={2}'
              '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=QLb9RB7g'
              '&search_type=FILTER_CHANGE&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true'
              '&timezone_offset=120&version=1.5.8'                  
              '&price_min={0}&price_max={1}')
        new_url = url.format(self.price_lb, self.price_ub, self.city)
            

        if (int(self.price_lb)  >= 990):
            url = ('https://www.airbnb.de/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1'
              '&allow_override%5B%5D=&auto_ib=true&checkin=2019-09-20&checkout=2019-09-22&client_session_id='
              '621cf853-d03e-4108-b717-c14962b6ab8b&currency=EUR&experiences_per_grid=20&fetch_filters=true'
              '&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true'
              '&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18'
              '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false&'
              'query={1}'
              '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=QLb9RB7g'
              '&search_type=FILTER_CHANGE&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true'
              '&timezone_offset=120&version=1.5.8'                  
              '&price_min={0}')
              
              
            new_url = url.format(self.price_lb, self.city)

        yield scrapy.Request(url=new_url, callback=self.parse_id, dont_filter=True)


    def parse_id(self, response):
        '''Parses all the URLs/ids/available fields from the initial json object and stores into dictionary

        Args:
            response: Json object from explore_tabs
        Returns:
        '''
        
        # Fetch and Write the response data
        data = json.loads(response.body)

        # Return a List of all homes
        homes = data.get('explore_tabs')[0].get('sections')[1].get('listings')

        if homes is None:
            try: 
                homes = data.get('explore_tabs')[0].get('sections')[3].get('listings')
            except IndexError:
                try: 
                    homes = data.get('explore_tabs')[0].get('sections')[2].get('listings')
                except:
                    raise CloseSpider("No homes available in the city and price parameters")
        
        base_url = 'https://www.airbnb.com/rooms/'
        data_dict = collections.defaultdict(dict) # Create Dictionary to put all currently available fields in

        for home in homes:
            room_id = str(home.get('listing').get('id'))
            url = base_url + str(home.get('listing').get('id'))
            data_dict[room_id]['url'] = url
            data_dict[room_id]['price'] = home.get('pricing_quote').get('rate').get('amount')
            data_dict[room_id]['bathrooms'] = home.get('listing').get('bathrooms')
            data_dict[room_id]['bedrooms'] = home.get('listing').get('bedrooms')
            data_dict[room_id]['host_languages'] = home.get('listing').get('host_languages')
            data_dict[room_id]['is_business_travel_ready'] = home.get('listing').get('is_business_travel_ready')
            data_dict[room_id]['is_fully_refundable'] = home.get('listing').get('is_fully_refundable')
            data_dict[room_id]['is_new_listing'] = home.get('listing').get('is_new_listing')
            data_dict[room_id]['is_superhost'] = home.get('listing').get('is_superhost')
            data_dict[room_id]['lat'] = home.get('listing').get('lat')
            data_dict[room_id]['lng'] = home.get('listing').get('lng')
            data_dict[room_id]['localized_city'] = home.get('listing').get('localized_city')
            data_dict[room_id]['localized_neighborhood'] = home.get('listing').get('localized_neighborhood')
            data_dict[room_id]['listing_name'] = home.get('listing').get('name')
            data_dict[room_id]['person_capacity'] = home.get('listing').get('person_capacity')
            data_dict[room_id]['picture_count'] = home.get('listing').get('picture_count')
            data_dict[room_id]['reviews_count'] = home.get('listing').get('reviews_count')
            data_dict[room_id]['room_type_category'] = home.get('listing').get('room_type_category')
            data_dict[room_id]['star_rating'] = home.get('listing').get('star_rating')
            data_dict[room_id]['host_id'] = home.get('listing').get('user').get('id')
            data_dict[room_id]['avg_rating'] = home.get('listing').get('avg_rating')
            data_dict[room_id]['can_instant_book'] = home.get('pricing_quote').get('can_instant_book')
            data_dict[room_id]['monthly_price_factor'] = home.get('pricing_quote').get('monthly_price_factor')
            data_dict[room_id]['currency'] = home.get('pricing_quote').get('rate').get('currency')
            data_dict[room_id]['amt_w_service'] = home.get('pricing_quote').get('rate_with_service_fee').get('amount')
            data_dict[room_id]['rate_type'] = home.get('pricing_quote').get('rate_type')
            data_dict[room_id]['weekly_price_factor'] = home.get('pricing_quote').get('weekly_price_factor')


        # Iterate through dictionary of URLs in the single page to send a SplashRequest for each
        for room_id in data_dict:
            yield SplashRequest(url=base_url+room_id, callback=self.parse_details,
                                meta=data_dict.get(room_id),
                                endpoint="render.html",
                                args={'wait': '0.5'})

        # After scraping entire listings page, check if more pages
        pagination_metadata = data.get('explore_tabs')[0].get('pagination_metadata')
        if pagination_metadata.get('has_next_page'):

            items_offset = pagination_metadata.get('items_offset')
            section_offset = pagination_metadata.get('section_offset')

            new_url = ('https://www.airbnb.de/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1'
                      '&allow_override%5B%5D=&auto_ib=true&checkin=2019-09-20&checkout=2019-09-22&client_session_id='
                      '621cf853-d03e-4108-b717-c14962b6ab8b&currency=EUR&experiences_per_grid=20'
                      '&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true'
                      '&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18'
                      '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false'
                      '&query={4}'
                      '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=QLb9RB7g'
                      '&satori_version=1.1.9&screen_height=797&screen_size=medium&screen_width=885'
                      '&search_type=FILTER_CHANGE&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true'
                      '&timezone_offset=120&version=1.5.8'
                      '&items_offset={0}&section_offset={1}&price_min={2}&price_max={3}')
            new_url = new_url.format(items_offset, section_offset, self.price_lb, self.price_ub, self.city)
            
            if (int(self.price_lb) >= 990):
                url = ('https://www.airbnb.de/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1'
                      '&allow_override%5B%5D=&auto_ib=true&checkin=2019-09-20&checkout=2019-09-22&client_session_id='
                      '621cf853-d03e-4108-b717-c14962b6ab8b&currency=CAD&experiences_per_grid=20'
                      '&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true'
                      '&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18'
                      '&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&luxury_pre_launch=false&metadata_only=false'
                      '&query={3}'
                      '&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&s_tag=QLb9RB7g'
                      '&satori_version=1.1.9&screen_height=797&screen_size=medium&screen_width=885'
                      '&search_type=FILTER_CHANGE&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true'
                      '&timezone_offset=120&version=1.5.8'
                      '&items_offset={0}&section_offset={1}&price_min={2}')
                new_url = url.format(items_offset, section_offset, self.price_lb, self.city)
            
            # If there is a next page, update url and scrape from next page
            yield scrapy.Request(url=new_url, callback=self.parse_id)

    def parse_details(self, response):
        '''Parses details for a single listing page and stores into AirbnbScraperItem object

        Args:
            response: The response from the page (same as inspecting page source)
        Returns:
            An AirbnbScraperItem object containing the set of fields pertaining to the listing
        '''
        # New Instance
        listing = AirbnbScraperItem()

        # Fill in fields for Instance from initial scrapy call
        listing['is_superhost'] = response.meta['is_superhost']
        listing['host_id'] = str(response.meta['host_id'])
        listing['price'] = response.meta['price']
        listing['url'] = response.meta['url']
        listing['bathrooms'] = response.meta['bathrooms']
        listing['bedrooms'] = response.meta['bedrooms']
        listing['is_business_travel_ready'] = response.meta['is_business_travel_ready']
        listing['is_fully_refundable'] = response.meta['is_fully_refundable']
        listing['is_new_listing'] = response.meta['is_new_listing']
        listing['lat'] = response.meta['lat']
        listing['lng'] = response.meta['lng']
        listing['localized_city'] = response.meta['localized_city']
        listing['localized_neighborhood'] = response.meta['localized_neighborhood']
        listing['listing_name'] = response.meta['listing_name']
        listing['person_capacity'] = response.meta['person_capacity']
        listing['picture_count'] = response.meta['picture_count']
        listing['reviews_count'] = response.meta['reviews_count']
        listing['room_type_category'] = response.meta['room_type_category']
        listing['star_rating'] = response.meta['star_rating']
        listing['avg_rating'] = response.meta['avg_rating']
        listing['can_instant_book'] = response.meta['can_instant_book']
        listing['monthly_price_factor'] = response.meta['monthly_price_factor']
        listing['weekly_price_factor'] = response.meta['weekly_price_factor']
        listing['currency'] = response.meta['currency']
        listing['amt_w_service'] = response.meta['amt_w_service']
        listing['rate_type'] = response.meta['rate_type']

        # Other fields scraped from html response.text using regex (some might fail hence try/catch)
        try:
            listing['num_beds'] = int((re.search('"bed_label":"(.).*","bedroom_label"', response.text)).group(1))
        except:
            listing['num_beds'] = 0

        try:
            listing['host_reviews'] = int((re.search(r'"badges":\[{"count":(.*?),"id":"reviews"',
                                      response.text)).group(1))
        except:
            listing['host_reviews'] = 0

        # Main six rating metrics + overall_guest_satisfication
        try:
            listing['accuracy'] = int((re.search('"accuracy_rating":(.*?),"', response.text)).group(1))
            listing['checkin'] = int((re.search('"checkin_rating":(.*?),"', response.text)).group(1))
            listing['cleanliness'] = int((re.search('"cleanliness_rating":(.*?),"', response.text)).group(1))
            listing['communication'] = int((re.search('"communication_rating":(.*?),"', response.text)).group(1))
            listing['value'] = int((re.search('"value_rating":(.*?),"', response.text)).group(1))
            listing['location'] = int((re.search('"location_rating":(.*?),"', response.text)).group(1))
            listing['guest_satisfication'] = int((re.search('"guest_satisfaction_overall":(.*?),"',
                                             response.text)).group(1))
        except:
            listing['accuracy'] = 0
            listing['checkin'] = 0
            listing['cleanliness'] = 0
            listing['communication'] = 0
            listing['value'] = 0
            listing['location'] = 0
            listing['guest_satisfication'] = 0

        # Extra Host Fields
        try:
            listing['response_rate'] = int((re.search('"response_rate_without_na":"(.*?)%",', response.text)).group(1))
            listing['response_time'] = (re.search('"response_time_without_na":"(.*?)",', response.text)).group(1)
        except:
            listing['response_rate'] = 0
            listing['response_time'] = ''

        # Finally return the object
        yield listing
