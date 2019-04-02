# -*- coding: utf-8 -*-
import time

import re
import scrapy


from Zolo.items import MarketSTATSItem
from Zolo.settings import CITY_LIST
from tools.process_city_list import realize_capitalize


class TrendsSpider(scrapy.Spider):
    name = 'trends'
    allowed_domains = ['zolo.ca']
    start_urls = [url for url in CITY_LIST]

    def parse(self, response):


        # 对数据的解析：获取

        # 根据url获取city
        url = response.url
        city = re.findall(r'https://www.zolo.ca/(.*)-real-estate/trends',url)
        if len(city)== 0:
            city = None
        else:
            city = city[0]
        #
        # # 获取Housing Prices 的数据
        # housing_price = response.xpath("//h2[contains(text(),'Housing Prices')]/..")
        # housing_price_carts = housing_price.css('.card-value::text').extract()
        # avg_sold_price = housing_price_carts[0]
        # monthly_change = housing_price_carts[1]
        # quarterly_change = housing_price_carts[2]
        # yearly_changev = housing_price_carts[3]


        # 获取Housing Inventory的数据
        housing_inventory = response.xpath("//h2[contains(text(),'Housing Inventory')]/..")
        housing_inventory_carts = housing_inventory.css('.card-value::text').extract()

        new_listings = int(housing_inventory_carts[0].replace(',','').strip())
        homes_sold = int(housing_inventory_carts[1].replace(',','').strip())
        average_days_on_market = int(housing_inventory_carts[2].replace(',','').strip())
        selling_to_listing_price_ratio = housing_inventory_carts[3].strip()
        # 处理%号
        selling_to_listing_price_ratio_value = re.search(r'\d+',selling_to_listing_price_ratio)
        # 获取值
        if selling_to_listing_price_ratio_value == None:
            selling_to_listing_price_ratio_value =0
        else:
            selling_to_listing_price_ratio_value = selling_to_listing_price_ratio_value.group()
        # 表示符号
        # selling_to_listing_price_ratio_expression_method = re.search(r'%',selling_to_listing_price_ratio).group()




        # 获取Rankings
        # ranking = response.xpath("//h2[contains(text(),'Rankings')]/..")
        # if ranking:
        #     ranking_carts = ranking.css('.card-value::text').extract()
        #     most_expensive = ranking_carts[0]
        #
        #     fastest_Growing = [1]
        #
        #     fastest_Selling = [2]
        #
        #     highest_Turnover = [3]
        # else:
        #     most_expensive = None
        #
        #     fastest_Growing = None
        #
        #     fastest_Selling = None
        #
        #     highest_Turnover = None

        # 保存到item中
        market_stats_item = MarketSTATSItem()
        market_stats_item['new_listings'] = new_listings
        market_stats_item['homes_sold'] = homes_sold
        market_stats_item['average_days_on_market'] = average_days_on_market
        city = ''.join(list(map(realize_capitalize,city.split(' '))))
        market_stats_item['city'] = ' '.join(list(map(realize_capitalize,city.split('-'))))

        market_stats_item['selling_to_listing_price_ratio'] = int(selling_to_listing_price_ratio_value)/100


        if market_stats_item['new_listings'] != -1:
            yield market_stats_item



