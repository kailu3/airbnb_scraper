# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def remove_unicode(value):
    return value.replace(u"\u201c", '').replace(u"\u201d", '').replace(u"\2764", '').replace(u"\ufe0f")

class AirbnbScraperItem(scrapy.Item):

    # Host Fields
    is_superhost = scrapy.Field()
    host_id = scrapy.Field()

    # Room Fields
    url = scrapy.Field()
    room_id = scrapy.Field()
    is_business_travel_ready = scrapy.Field()
    is_fully_refundable = scrapy.Field()
    is_new_listing = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    host_languages = scrapy.Field()
    state = scrapy.Field()
    localized_city = scrapy.Field()
    localized_neighborhood = scrapy.Field()
    listing_name = scrapy.Field(input_processor=MapCompose(remove_unicode))
    person_capacity = scrapy.Field()
    picture_count = scrapy.Field()
    reviews_count = scrapy.Field()
    room_and_property_type = scrapy.Field()
    room_type_category = scrapy.Field()
    property_type_id = scrapy.Field()
    star_rating = scrapy.Field() # Rounded to .5 or .0 Avg Rating
    avg_rating = scrapy.Field()
    can_instant_book = scrapy.Field()
    monthly_price_factor = scrapy.Field()
    rate_type = scrapy.Field()
    weekly_price_factor = scrapy.Field()
    bathrooms = scrapy.Field()
    bedrooms = scrapy.Field()
    num_beds = scrapy.Field()
    accuracy = scrapy.Field()
    communication = scrapy.Field()
    cleanliness = scrapy.Field()
    location = scrapy.Field()
    checkin = scrapy.Field()
    value = scrapy.Field()
    guest_satisfication = scrapy.Field()
    host_reviews = scrapy.Field()
    response_rate = scrapy.Field()
    response_time = scrapy.Field()
