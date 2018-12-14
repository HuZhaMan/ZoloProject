# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: get_sql_con.py
@time: 2018/12/13
"""
from Zolo import settings
import psycopg2
from sshtunnel import SSHTunnelForwarder


def get_conn(is_ssh):
    if is_ssh:
        server = SSHTunnelForwarder(
            (settings.ssh_host, 22),  # B机器的配置
            ssh_password=settings.ssh_password,
            ssh_username=settings.ssh_username,
            remote_bind_address=(settings.host, settings.port)
        )
        # 开启服务
        server.start()

        conn = psycopg2.connect(host='127.0.0.1',
                                  port=server.local_bind_port,
                                  user=settings.user,
                                  password=settings.password,
                                  database=settings.database)
        # 返回数据库连接和服务（返回服务只要是用于最后的关闭）
        return conn,server

    else:
        conn = psycopg2.connect(
            host=settings.host,
            port=settings.port,
            database=settings.database,
            user=settings.user,
            password=settings.password
        )
        return conn


if __name__ == '__main__':
    conn,server = get_conn(True)
    cursor = conn.cursor()
    sql = '''
        insert into trend(
                new_listings,homes_sold,average_days_on_market,selling_to_listing_price_ratio,city,"createdDate")
                 values(72,30,32,0.96,'East Gwillimbury',now())
    '''
    cursor.execute(sql)
    conn.commit()
    server.stop()