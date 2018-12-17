# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: main.py
@time: 2018/10/31
"""
from scrapy import cmdline
from Zolo import settings


def main():

    # 将trend表删除
    cursor = settings.conn.cursor()
    cursor.execute(settings.sql_string_truncate_trend)
    settings.conn.commit()

    cmdline.execute('scrapy crawl trends'.split(' '))
    print('------------------------------------------------------1111')


if __name__ == '__main__':
    main()




