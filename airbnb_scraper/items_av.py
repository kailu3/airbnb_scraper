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
    avail_days = scrapy.Field()
    count_price = scrapy.Field()
    avg_price = scrapy.Field()
    min_price = scrapy.Field()
    max_price = scrapy.Field()
    max_diff_price = scrapy.Field()

    # January_avail_days = scrapy.Field()
    # February_avail_days = scrapy.Field()
    # March_avail_days = scrapy.Field()
    # April_avail_days = scrapy.Field()
    # May_avail_days = scrapy.Field()
    # June_avail_days = scrapy.Field()
    # July_avail_days = scrapy.Field()
    # August_avail_days = scrapy.Field()
    # September_avail_days = scrapy.Field()
    # October_avail_days = scrapy.Field()
    # November_avail_days = scrapy.Field()
    # December_avail_days = scrapy.Field()

    # January_count_price = scrapy.Field()
    # February_count_price = scrapy.Field()
    # March_count_price = scrapy.Field()
    # April_count_price = scrapy.Field()
    # May_count_price = scrapy.Field()
    # June_count_price = scrapy.Field()
    # July_count_price = scrapy.Field()
    # August_count_price = scrapy.Field()
    # September_count_price = scrapy.Field()
    # October_count_price = scrapy.Field()
    # November_count_price = scrapy.Field()
    # December_count_price = scrapy.Field()
    
    # January_avg_price = scrapy.Field()
    # February_avg_price = scrapy.Field()
    # March_avg_price = scrapy.Field()
    # April_avg_price = scrapy.Field()
    # May_avg_price = scrapy.Field()
    # June_avg_price = scrapy.Field()
    # July_avg_price = scrapy.Field()
    # August_avg_price = scrapy.Field()
    # September_avg_price = scrapy.Field()
    # October_avg_price = scrapy.Field()
    # November_avg_price = scrapy.Field()
    # December_avg_price = scrapy.Field()

    # January_min_price = scrapy.Field()
    # February_min_price = scrapy.Field()
    # March_min_price = scrapy.Field()
    # April_min_price = scrapy.Field()
    # May_min_price = scrapy.Field()
    # June_min_price = scrapy.Field()
    # July_min_price = scrapy.Field()
    # August_min_price = scrapy.Field()
    # September_min_price = scrapy.Field()
    # October_min_price = scrapy.Field()
    # November_min_price = scrapy.Field()
    # December_min_price = scrapy.Field()

    # January_max_price = scrapy.Field()
    # February_max_price = scrapy.Field()
    # March_max_price = scrapy.Field()
    # April_max_price = scrapy.Field()
    # May_max_price = scrapy.Field()
    # June_max_price = scrapy.Field()
    # July_max_price = scrapy.Field()
    # August_max_price = scrapy.Field()
    # September_max_price = scrapy.Field()
    # October_max_price = scrapy.Field()
    # November_max_price = scrapy.Field()
    # December_max_price = scrapy.Field()

    # January_max_diff_price = scrapy.Field()
    # February_max_diff_price = scrapy.Field()
    # March_max_diff_price = scrapy.Field()
    # April_max_diff_price = scrapy.Field()
    # May_max_diff_price = scrapy.Field()
    # June_max_diff_price = scrapy.Field()
    # July_max_diff_price = scrapy.Field()
    # August_max_diff_price = scrapy.Field()
    # September_max_diff_price = scrapy.Field()
    # October_max_diff_price = scrapy.Field()
    # November_max_diff_price = scrapy.Field()
    # December_max_diff_price = scrapy.Field()

    # prices = scrapy.Field()

