# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import calendar
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def remove_unicode(value):
    return value.replace(u"\u201c", ).replace(u"\u201d", ).replace(u"\2764", ).replace(u"\ufe0f")

class AirbnbScraperItem(scrapy.Item):

    # Host Fields
    room_id = scrapy.Field()
    year = scrapy.Field()
    month_num = scrapy.Field()
    days_availabe = scrapy.Field()
    January = scrapy.Field()
    February = scrapy.Field()
    March = scrapy.Field()
    April = scrapy.Field()
    May = scrapy.Field()
    June = scrapy.Field()
    July = scrapy.Field()
    August = scrapy.Field()
    September = scrapy.Field()
    October = scrapy.Field()
    November = scrapy.Field()
    December = scrapy.Field()

