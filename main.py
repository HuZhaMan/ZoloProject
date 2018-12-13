# -*- coding:utf-8 _*-  
""" 
@author:Administrator
@file: main.py
@time: 2018/10/31
"""
from scrapy import cmdline
import os
# cmdline.execute('scrapy crawl market_stats'.split(' '))
# os.system('workon scrapy')
# cmdline.execute('scrapy crawl index_page'.split(' '))
# cmdline.execute('scrapy crawl market_stats2'.split(' '))
# cmdline.execute('scrapy crawl crawl_based_on_province'.split(' '))
cmdline.execute('scrapy crawl trends'.split(' '))

# 需要一个存储过程；
sql_string = '''

'''


