# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Zolo import settings
# from Zolo.spiders import index_page

class ZoloPipeline(object):
    def process_item(self, item, spider):
        return item


# spider:market_stats的pipeline
class MarketStatsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user= settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DBNAME,
            charset='utf8',
        )
        self.cursor = self.connect.cursor()

    def process_item(self,item,spider):
        self.cursor.execute(
            '''
            insert into trend(new_listings,homes_sold,average_days_on_market,selling_to_listing_price_ratio,city) values(%s,%s,%s,%s,%s)
            ''',[item['new_listings'],item['homes_sold'],item['average_days_on_market'],item['selling_to_listing_price_ratio']
                ,item['city']
                 ]
        )
        self.connect.commit()
        return item

