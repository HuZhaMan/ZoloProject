# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Zolo import settings


class ZoloPipeline(object):
    def process_item(self, item, spider):
        return item


# spider:market_stats的pipeline mysql的
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


# postgresql
class MarketStatsPipeline1(object):

    def process_item(self,item, spider):
        conn = settings.conn

        insert_query = '''
                insert into trend(
                new_listings,homes_sold,average_days_on_market,selling_to_listing_price_ratio,city,"createdDate")
                 values(%s,%s,%s,%s,'%s',now())
        ''' % (item['new_listings'], item['homes_sold'], item['average_days_on_market'],
             item['selling_to_listing_price_ratio'], str(item['city']))
        print(insert_query)
        cursor = conn.cursor()
        cursor.execute(insert_query)
        conn.commit()
        return item

    # 实现close spider方法关闭ssh服务
    def close_spider(self, spider):
        cursor = settings.conn.cursor()
        # 向estate_expect_deal_price_params_data_test 插入基本的数据
        cursor.execute(settings.estate_expect_deal_price_params_data_test)
        settings.conn.commit()

        sql_1 = '''
            SELECT AVG(CAST("citySpLp" AS FLOAT)
            FROM estate_expect_deal_price_params_data_test 
            where "provinceCode"='ON'
        '''
        sql_2 = '''
            SELECT "provinceCode" FROM estate_expect_deal_price_params_data_test
        '''
        sql_3 = '''
            INSERT INTO estate_expect_deal_price_params_data_test("provinceCode","provinceSpLp","soldCount",dom,"createdDate")
            VALUES(1,2,3,4,now())
        '''
        sql_4 = '''
            SELECT AVG(CAST(dom AS FLOAT))
            FROM estate_expect_deal_price_params_data_test 
            where "provinceCode"='ON'
        '''
        sql_5 = '''
            SELECT AVG(CAST("soldCount" AS FLOAT))
            FROM estate_expect_deal_price_params_data_test 
            where "provinceCode"='ON'
        '''
        sql_6 = '''
            SELECT AVG(CAST("provinceSpLp" AS FLOAT))
            FROM estate_expect_deal_price_params_data
            where city=NULL
            AND "provinceCode"!=NULL
        '''
        # 向estate_expect_deal_price_params_data_test 插入省份和国家的平均数据
        settings.server.stop()
        print('------------------------------------------------------finish')






