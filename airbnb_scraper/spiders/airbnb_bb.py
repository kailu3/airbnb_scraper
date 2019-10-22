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
from scrapy.http import JSONRequest
from airbnb_scraper.items_bb import AirbnbScraperItem


# ********************************************************************************************
# Important: Run -> docker run -p 8050:8050 scrapinghub/splash in background before crawling *
# ********************************************************************************************


# *********************************************************************************************
# Run crawler with -> scrapy crawl airbnb -o 21to25.json -a price_lb='' -a price_ub=''        *
# *********************************************************************************************

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb_bb'
    allowed_domains = ['www.airbnb.de']

    '''
    You don't have to override __init__ each time and can simply use self.parameter (See https://bit.ly/2Wxbkd9),
    but I find this way much more readable.
    '''
    def __init__(self, city='', ne_lat='', ne_lng='', sw_lat='', sw_lng='',  *args,**kwargs):
        super(AirbnbSpider, self).__init__(*args, **kwargs)
        self.ne_lat = ne_lat
        self.ne_lng = ne_lng
        self.sw_lat = sw_lat
        self.sw_lng = sw_lng
        
        
        
        

    def start_requests(self):
        '''Sends a scrapy request to the designated url price range

        Args:
        Returns:
        '''

        # url = ('https://www.airbnb.de/s/Luxemburg/homes?refinement_paths[]=%2Fhomes&current_tab_id=home_tab&'
        #       'selected_tab_id=home_tab&allow_override[]=&_set_bev_on_new_domain=1565902499_ug%2BhExThvhjjvWm4&'
        #       'screen_size=large&search_type=unknown&'
        #       'ne_lat={0}&ne_lng={1}&sw_lat=·{2}&sw_lng={3}&'
        #       'zoom=10&search_by_map=false&hide_dates_and_guests_filters=false')
        
        url = ('https://www.airbnb.de/api/v2/explore_tabs?_format=for_explore_search_web&'
               '_set_bev_on_new_domain=1565902499_ug+hExThvhjjvWm4&allow_override[]=&auto_ib=true&'
               'client_session_id=c7798e46-033b-4d87-b742-79b11a1d412c&currency=EUR&current_tab_id=home_tab&'
               'experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&'
               'hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&'
               'is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=de&'
               'metadata_only=false&ne_lat={0}&ne_lng={1}&'
               'place_id=ChIJRyEhyrlFlUcR75LTAvZg22Q&query=Luxemburg&'
               'query_understanding_enabled=true&refinement_paths[]=/homes&satori_version=1.1.9&'
               'screen_height=639&screen_size=large&screen_width=1366&search_by_map=false&search_type=filter_change&'
               'selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&'
               'sw_lat={2}&sw_lng={3}&timezone_offset=120&version=1.6.2&zoom=10')
                                            
        new_url = url.format(self.ne_lat, self.ne_lng, self.sw_lat, self.sw_lng)

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
        homes = data.get('explore_tabs')[0].get('sections')[0].get('listings')

        if homes is None:
            try: 
                homes = data.get('explore_tabs')[0].get('sections')[1].get('listings')
            except IndexError:
                try: 
                    homes = data.get('explore_tabs')[0].get('sections')[2].get('listings')
                except IndexError:
                    try: 
                        homes = data.get('explore_tabs')[0].get('sections')[3].get('listings')
                    except:
                        raise CloseSpider("No homes available in the city and price parameters")
        
        base_url = 'https://www.airbnb.de/rooms/'
        pgtd_url = 'https://www.airbnb.de/api/v2/paid_growth_tracking_datas?_format=for_p3&currency=EUR&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=de'

        data_dict = collections.defaultdict(dict) # Create Dictionary to put all currently available fields in

        for home in homes:
            room_id = str(home.get('listing').get('id'))
            url = base_url + str(home.get('listing').get('id'))
            data_dict[room_id]['url'] = url
            data_dict[room_id]['room_id'] = room_id
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
            data_dict[room_id]['room_and_property_type'] = home.get('listing').get('room_and_property_type')
            data_dict[room_id]['property_type_id'] = home.get('listing').get('property_type_id')
            data_dict[room_id]['star_rating'] = home.get('listing').get('star_rating')
            data_dict[room_id]['host_id'] = home.get('listing').get('user').get('id')
            data_dict[room_id]['avg_rating'] = home.get('listing').get('avg_rating')
            data_dict[room_id]['can_instant_book'] = home.get('pricing_quote').get('can_instant_book')
            data_dict[room_id]['weekly_price_factor'] = home.get('pricing_quote').get('weekly_price_factor')
            data_dict[room_id]['monthly_price_factor'] = home.get('pricing_quote').get('monthly_price_factor')
            data_dict[room_id]['rate_type'] = home.get('pricing_quote').get('rate_type')


        # Iterate through dictionary of URLs in the single page to send a SplashRequest for each
        for room_id in data_dict:                              
            pgtd_data = {
                'checkin_date': '2019-11-21',
                'checkout_date': '2019-11-23',
                'listing_id': room_id,
                'num_adults': 1,
                'num_children':	0,
                'num_infants': 0
            }
            yield JSONRequest(url=pgtd_url, data=pgtd_data, callback=self.parse_pgdt, meta=data_dict.get(room_id))

        # After scraping entire listings page, check if more pages
        pagination_metadata = data.get('explore_tabs')[0].get('pagination_metadata')
        if pagination_metadata.get('has_next_page'):
            print ('has_next_page = true')

            items_offset = pagination_metadata.get('items_offset')
            section_offset = pagination_metadata.get('section_offset')

            url = ('https://www.airbnb.de/api/v2/explore_tabs?_format=for_explore_search_web&'
                   '_set_bev_on_new_domain=1565902499_ug+hExThvhjjvWm4&allow_override[]=&auto_ib=true&'
                   'client_session_id=c7798e46-033b-4d87-b742-79b11a1d412c&currency=EUR&current_tab_id=home_tab&'
                   'experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&'
                   'hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&'
                   'is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=de&'
                   'metadata_only=false&ne_lat={0}&ne_lng={1}&'
                   'place_id=ChIJRyEhyrlFlUcR75LTAvZg22Q&query=Luxemburg&'
                   'query_understanding_enabled=true&refinement_paths[]=/homes&satori_version=1.1.9&'
                   'screen_height=639&screen_size=large&screen_width=1366&search_by_map=false&search_type=filter_change&'
                   'selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&'
                   'sw_lat={2}&sw_lng={3}&timezone_offset=120&version=1.6.2&zoom=10&items_offset={4}&section_offset={5}')
               
            new_url = url.format(self.ne_lat, self.ne_lng, self.sw_lat, self.sw_lng, items_offset, section_offset)
            
            # If there is a next page, update url and scrape from next page
            yield scrapy.Request(url=new_url, callback=self.parse_id)

    def parse_pgdt(self, response):
        '''Parses city, state and country from https://www.airbnb.de/api/v2/paid_growth_tracking_datas
        '''
        
        base_url = 'https://www.airbnb.de/rooms/'
        
        # Fetch and Write the response data
        data = json.loads(response.body)        
        
        response.meta['city'] = data.get('paid_growth_tracking_data').get('city')
        response.meta['country'] = data.get('paid_growth_tracking_data').get('country')
        response.meta['state'] = data.get('paid_growth_tracking_data').get('state')
        
        yield SplashRequest(url=base_url+response.meta['room_id'], callback=self.parse_details,
                    meta=response.meta,
                    endpoint="render.html",
                    args={'wait': '0.5'})
        
        
    def parse_details(self, response):
        '''Parses details for a single listing page and stores into AirbnbScraperItem object

        Args:
            response: The response from the page (same as inspecting page source)
        Returns:
            An AirbnbScraperItem object containing the set of fields pertaining to the listing
        '''
        
        seperator = ', '
        
        # New Instance
        listing = AirbnbScraperItem()        
        
        # Fill in fields for Instance from initial scrapy call
        listing['room_id'] = str(response.meta['room_id'])
        listing['url'] = response.meta['url']
        listing['listing_name'] = response.meta['listing_name']        
        listing['is_superhost'] = response.meta['is_superhost']
        listing['host_id'] = str(response.meta['host_id'])
        listing['host_languages'] = seperator.join(response.meta['host_languages'])        
        # Fill in fields for Instance from paid_growth_tracking_datas (pgtd) scrapy call
        listing['city'] = response.meta['city']
        listing['localized_city'] = response.meta['localized_city']
        listing['localized_neighborhood'] = response.meta['localized_neighborhood']        
        listing['country'] = response.meta['country']
        listing['state'] = response.meta['state']
        listing['lat'] = response.meta['lat']
        listing['lng'] = response.meta['lng']
        listing['room_type_category'] = response.meta['room_type_category']
        listing['room_and_property_type'] = response.meta['room_and_property_type']        
        listing['property_type_id'] = response.meta['property_type_id']        
        listing['person_capacity'] = response.meta['person_capacity']        
        listing['bathrooms'] = response.meta['bathrooms']
        listing['bedrooms'] = response.meta['bedrooms']
        listing['is_business_travel_ready'] = response.meta['is_business_travel_ready']
        listing['rate_type'] = response.meta['rate_type']
        listing['is_fully_refundable'] = response.meta['is_fully_refundable']
        listing['can_instant_book'] = response.meta['can_instant_book']
        listing['monthly_price_factor'] = response.meta['monthly_price_factor']
        listing['weekly_price_factor'] = response.meta['weekly_price_factor']
        listing['is_new_listing'] = response.meta['is_new_listing']
        listing['picture_count'] = response.meta['picture_count']
        listing['reviews_count'] = response.meta['reviews_count']
        listing['star_rating'] = response.meta['star_rating']
        listing['avg_rating'] = response.meta['avg_rating']
        
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
        
