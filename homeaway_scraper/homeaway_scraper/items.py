# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HomeawayScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Room fields
    listingId = scrapy.Field()
    propertyType = scrapy.Field()
