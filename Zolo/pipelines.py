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

        '''
        this function is to solve final insertion process
        1:完成基本字段的插入
        2：
        :param spider:
        :return: None
        '''
        conn = settings.conn
        cursor = conn.cursor()
        # 向estate_expect_deal_price_params_data_test 插入基本的数据
        # 执行基本的插入
        cursor.execute(settings.estate_expect_deal_price_params_data_test_insert_base)
        conn.commit()
        # 插入省份数据
        province_code_list = []
        cursor.execute(settings.get_province_code)
        for province_code in cursor.fetchall():
            # print(province_code[0])
            province_code_list.append(province_code[0])
        conn.commit()
        province_code_set = set(province_code_list)
        for code in province_code_set:
            print(code)
            insert_province_sql = '''
            INSERT INTO estate_expect_deal_price_params_data_test("provinceCode","provinceSpLp","listingCount","soldCount",dom,"createdDate")
            (
            select
            '{0}',
            CAST(sum(CAST("citySpLp" as FLOAT)*CAST("soldCount" AS FLOAT))/sum(CAST("soldCount" as FLOAT)) AS DECIMAL(10,2)) AS "provinceSpLp" ,
            0,
            sum("soldCount") AS "soldCount",
            cast(AVG(CAST(dom AS FLOAT)) AS decimal(10,0)) AS dom,
            date(now())


            FROM estate_expect_deal_price_params_data_test
            where city !=''
            AND city IS NOT NULL
            AND "createdDate"=date(now())
            AND "provinceCode"='{1}')
            '''.format(code, code)
            print(insert_province_sql)
            cursor.execute(insert_province_sql)
            conn.commit()

        # 插入国家数据
        insert_country_sql = '''
            INSERT INTO estate_expect_deal_price_params_data_test("soldCount",dom,"createdDate",country,"countrySpLp","floatingValue")
            (SELECT 
            SUM("soldCount") AS "soldCount",
            CAST(AVG(dom) AS decimal(10,0)) as dom,
            date(now()) as "createdDate",
            'Canada' AS country,
            CAST(AVG(CAST("provinceSpLp" AS FLOAT)) AS DECIMAL(10,2))AS "countrySpLp",
            3

            FROM estate_expect_deal_price_params_data_test
            where city IS NULL
            AND "createdDate"=date(now())
            )
        '''
        cursor.execute(insert_country_sql)
        conn.commit()
        # conn.close()


        # 向estate_expect_deal_price_params_data_test 插入省份和国家的平均数据
        settings.server.stop()
        print('------------------------------------------------------finish')






