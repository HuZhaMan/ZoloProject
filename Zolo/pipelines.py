# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Zolo import settings
# from Zolo.spiders import index_page
import psycopg2
from sshtunnel import SSHTunnelForwarder

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
    def process_item(self, item, spider):
        """
        Notes
            data: data must be include "realtorSearchId","realtorDataId","predictDaysOnMarket"
        """

        _insert_query = '''
                insert into trend(
                new_listings,homes_sold,average_days_on_market,selling_to_listing_price_ratio,city)
                 values(%s,%s,%s,%s,'%s')
        '''%(item['new_listings'],item['homes_sold'],item['average_days_on_market'],item['selling_to_listing_price_ratio']
                ,str(item['city']))
        print(_insert_query)
        self.execute_query(sql=_insert_query, is_select=False)
        return item


    def execute_query(self,sql=None, query_fn=None, is_select=True):
        def _query(conn, _sql=sql, _query_fn=query_fn):
            __data = None
            if query_fn is not None:
                __data = query_fn(conn)
            elif sql is not None:
                try:
                    if is_select:
                        cursor = conn.cursor()
                        cursor.execute(sql)
                        __data = cursor.fetchall()
                        cursor.close()
                        conn.commit()
                    else:
                        cursor = conn.cursor()
                        cursor.execute(sql)
                        __data = cursor.rowcount
                        conn.commit()

                except ZeroDivisionError as e:
                    print(e)
                finally:
                    conn.close()

            return __data

        return self._do_query(query_fn=lambda conn: _query(conn))

    def _do_query(self,query_fn, is_ssh=settings.is_ssh):
        if is_ssh:
            with SSHTunnelForwarder((settings.ssh_host, settings.ssh_port),
                                    ssh_password=settings.ssh_password, ssh_username=settings.ssh_username,
                                    remote_bind_address=(settings.host, settings.port)) as server:

                conn = psycopg2.connect(
                    host='localhost',
                    port=server.local_bind_port,
                    database=settings.database,
                    user=settings.user,
                    password=settings.password
                )
                return query_fn(conn)
        else:
            conn = psycopg2.connect(
                host=settings.host,
                port=settings.port,
                database=settings.database,
                user=settings.user,
                password=settings.password
            )
            return query_fn(conn)



