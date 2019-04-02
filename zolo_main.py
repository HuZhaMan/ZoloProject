# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: zolo_main.py
@time: 2018/10/31
"""
from scrapy import cmdline
from tools import get_sql_con


def main():
    conn,_ = get_sql_con.get_conn(True)
    sql_string_truncate_trend = '''
            TRUNCATE trend
    '''

    # 将trend表删除
    cursor = conn.cursor()
    cursor.execute(sql_string_truncate_trend)
    conn.commit()

    cmdline.execute('scrapy crawl trends'.split(' '))
    print('------------------------------------------------------1111')
    conn.close()
    _.stop()

if __name__ == '__main__':
    main()




