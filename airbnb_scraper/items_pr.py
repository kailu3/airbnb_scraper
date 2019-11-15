# _*_ coding: utf_8 _*_

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
    month = scrapy.Field()
    price_type = scrapy.Field()
    price_localized_title = scrapy.Field()
    price_amount = scrapy.Field()