# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZoloItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MarketSTATSItem(scrapy.Item):
    city = scrapy.Field()
    new_listings = scrapy.Field()
    homes_sold = scrapy.Field()
    average_days_on_market = scrapy.Field()
    selling_to_listing_price_ratio = scrapy.Field()



