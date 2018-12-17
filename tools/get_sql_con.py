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
    # sql = '''
    #     insert into trend(
    #             new_listings,homes_sold,average_days_on_market,selling_to_listing_price_ratio,city,"createdDate")
    #              values(72,30,32,0.96,'East Gwillimbury',now())
    # '''
    # cursor.execute(sql)
    # conn.commit()

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
        '''.format(code,code)
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


    server.stop()
    print('finish')

